import os
import json
import logging
from uuid import UUID
from datetime import datetime, timezone
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from pydantic import BaseModel, Field
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.config import settings
from app.models.scan import Scan, ScanStatus
from app.models.scan_result import ScanResult
from app.models.report import Report
from app.models.user import User
from app.utils.pdf_generator import PDFReportGenerator
from app.services.email_service import EmailService

logger = logging.getLogger(__name__)

# Initialize the Gemini credentials globally from dotenv config just in case
if 'GOOGLE_API_KEY' not in os.environ and settings.GOOGLE_GEMINI_KEY:
    os.environ['GOOGLE_API_KEY'] = settings.GOOGLE_GEMINI_KEY
if 'GEMINI_API_KEY' not in os.environ and settings.GOOGLE_GEMINI_KEY:
    os.environ['GEMINI_API_KEY'] = settings.GOOGLE_GEMINI_KEY

# Pydantic Schemas for ADK structured output
class IssueItem(BaseModel):
    module: str
    title: str
    severity: str
    recommendation: str

class RecommendationItem(BaseModel):
    title: str
    impact: str
    effort: str

class ReportAnalysisOutput(BaseModel):
    executive_summary: str = Field(description="2-3 paragraphs for C-level overview")
    critical_issues: List[IssueItem]
    recommendations: List[RecommendationItem]

class ReportService:
    """
    Handles talking to Claude API to generate a JSON analysis, 
    compiling it into a PDF, and saving it.
    """
    def __init__(self, db: AsyncSession):
        self.db = db
        self.agent = LlmAgent(
            model="gemini-3-flash-preview",
            name="report_analyzer",
            instruction="Analyze the following web scan results and provide a structured JSON response.",
            output_schema=ReportAnalysisOutput
        )
        self.session_service = InMemorySessionService()

    async def _fetch_scan_data(self, scan_id: str) -> dict:
        """Fetch scan and results from DB and serialize to dict for the LLM."""
        scan = await self.db.get(Scan, UUID(scan_id))
        if not scan:
            raise ValueError(f"Scan {scan_id} not found")
        
        statement = select(ScanResult).where(ScanResult.scan_id == scan.id)
        results = await self.db.execute(statement)
        scan_results = results.scalars().all()
        
        data = {
            "url": scan.url,
            "duration": scan.duration_seconds,
            "overall_score": scan.overall_score,
            "modules": {}
        }
        
        for r in scan_results:
            data["modules"][r.module] = {
                "score": r.score,
                "grade": r.grade,
                "issues": {"critical": r.issues_critical, "high": r.issues_high, "medium": r.issues_medium, "low": r.issues_low},
                "raw_data_summary": str(r.data)[:500] # Pass a snippet of raw data to avoid token limits
            }
            
        return data

    async def _call_gemini_api(self, scan_data: dict) -> dict:
        """Call Amazon Gemini via Google ADK to generate insights based on scan data."""
        prompt = f"Scan Data:\n{json.dumps(scan_data, indent=2)}\nReturn ONLY valid JSON with the exact structure, no markdown blocks."
        content = types.Content(role='user', parts=[types.Part(text=prompt)])
        
        try:
            session = await self.session_service.create_session(
                app_name="report_service", user_id="system", session_id=f"rep_{datetime.now().timestamp()}"
            )
            runner = Runner(agent=self.agent, app_name="report_service", session_service=self.session_service)
            
            final_answer = "{}"
            async for event in runner.run_async(user_id="system", session_id=session.id, new_message=content):
                if event.is_final_response() and event.content:
                    final_answer = event.content.parts[0].text.strip()
            
            # Very basic cleanup in case it added markdown block limits
            if final_answer.startswith("```json"):
                final_answer = final_answer.split("```json")[1]
            if final_answer.endswith("```"):
                final_answer = final_answer.rsplit("```", 1)[0]
                
            return json.loads(final_answer.strip())
        except Exception as e:
            logger.error(f"Failed to parse Gemini JSON: {e}")
            return {"executive_summary": "Analysis failed to parse.", "critical_issues": [], "recommendations": []}

    async def generate_report(self, scan_id: str) -> None:
        """Main flow: Gather data -> Call LLM -> Generate PDF -> Save DB -> Email"""
        try:
            logger.info(f"Starting report generation for scan {scan_id}")
            scan_data = await self._fetch_scan_data(scan_id)
            
            # 1. Ask AI for analysis
            ai_analysis = await self._call_gemini_api(scan_data)
            
            # 2. Generate PDF
            os.makedirs("static/reports", exist_ok=True)
            pdf_path = f"static/reports/{scan_id}.pdf"
            
            generator = PDFReportGenerator(pdf_path)
            generator.add_title(scan_data['url'], scan_data['overall_score'])
            generator.add_executive_summary(ai_analysis.get('executive_summary', 'No summary generated.'))
            
            # Extract scores and severities for charts
            module_scores = {mod: data['score'] for mod, data in scan_data['modules'].items()}
            
            total_severities = {"critical": 0, "high": 0, "medium": 0, "low": 0}
            for mod in scan_data['modules'].values():
                for sev, count in mod['issues'].items():
                    if sev in total_severities:
                        total_severities[sev] += count
                        
            generator.add_charts(module_scores, total_severities)
            generator.add_issues_table(ai_analysis.get('critical_issues', []))
            
            generator.generate()
            
            # 3. Save to DB
            scan = await self.db.get(Scan, UUID(scan_id))
            report = Report(
                scan_id=scan.id,
                ai_analysis=ai_analysis,
                pdf_path=pdf_path
            )
            self.db.add(report)
            await self.db.commit()
            
            logger.info(f"Report generated successfully for scan {scan_id}")
            
            # 4. Trigger email
            user = await self.db.get(User, scan.user_id)
            if user and user.email:
                email_service = EmailService()
                await email_service.send_report_email(
                    email=user.email,
                    user_name=user.name or "Utilisateur",
                    scan_url=scan.url,
                    score=scan.overall_score or 0,
                    pdf_path=pdf_path
                )
                report.email_sent = True
                report.email_sent_at = datetime.now(timezone.utc)
                self.db.add(report)
                await self.db.commit()
            
        except Exception as e:
            logger.error(f"Report generation failed for scan {scan_id}: {e}", exc_info=True)
