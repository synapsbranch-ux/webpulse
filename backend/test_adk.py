import asyncio
from typing import List, Dict
from pydantic import BaseModel, Field
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_GEMINI_KEY", "")
os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_GEMINI_KEY", "")

class Issue(BaseModel):
    module: str
    title: str
    severity: str
    recommendation: str

class Recommendation(BaseModel):
    title: str
    impact: str
    effort: str

class ReportAnalysisOutput(BaseModel):
    executive_summary: str = Field(description="2-3 paragraphs for C-level overview")
    critical_issues: List[Issue]
    recommendations: List[Recommendation]

async def test_adk():
    agent = LlmAgent(
        model="gemini-3-flash-preview",
        name="report_analyzer",
        instruction="""Analyze the following web scan results and provide a structured JSON response.
        Return ONLY valid JSON with this exact structure, no markdown blocks.
        """,
        output_schema=ReportAnalysisOutput
    )

    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name="test", user_id="user1", session_id="ses1")
    runner = Runner(agent=agent, app_name="test", session_service=session_service)

    scan_data = {"test": "data"}
    prompt = f"Scan Data:\n{scan_data}"
    content = types.Content(role='user', parts=[types.Part(text=prompt)])

    print("Running agent...")
    async for event in runner.run_async(user_id="user1", session_id="ses1", new_message=content):
        if event.is_final_response() and event.content:
            final_answer = event.content.parts[0].text.strip()
            print("Response:", final_answer)

if __name__ == "__main__":
    asyncio.run(test_adk())
