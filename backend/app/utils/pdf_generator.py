import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from app.utils.chart_generator import generate_score_chart, generate_severity_pie

class PDFReportGenerator:
    def __init__(self, filename: str):
        self.filename = filename
        self.styles = getSampleStyleSheet()
        self.elements = []
        
        # Custom styles
        self.styles.add(ParagraphStyle(name='TitleStyle', fontSize=24, textColor=colors.HexColor('#0F172A'), spaceAfter=12))
        self.styles.add(ParagraphStyle(name='HeadingStyle', fontSize=18, textColor=colors.HexColor('#6366F1'), spaceAfter=10, spaceBefore=20))
        self.styles.add(ParagraphStyle(name='NormalStyle', fontSize=11, textColor=colors.HexColor('#334155'), spaceAfter=8))
        
    def add_title(self, target_url: str, overall_score: int):
        self.elements.append(Paragraph("Synapsbranch Analysis Report", self.styles['TitleStyle']))
        self.elements.append(Paragraph(f"Target: {target_url}", self.styles['NormalStyle']))
        self.elements.append(Paragraph(f"Overall Score: {overall_score}/100", self.styles['HeadingStyle']))
        self.elements.append(Spacer(1, 20))
        
    def add_executive_summary(self, summary_text: str):
        self.elements.append(Paragraph("Executive Summary (AI Analysis)", self.styles['HeadingStyle']))
        self.elements.append(Paragraph(summary_text, self.styles['NormalStyle']))
        self.elements.append(Spacer(1, 20))
        
    def add_charts(self, module_scores: dict, severities: dict):
        self.elements.append(Paragraph("Performance & Risks Overview", self.styles['HeadingStyle']))
        
        # Add score chart
        score_buf = generate_score_chart(module_scores)
        score_img = Image(score_buf, width=400, height=260)
        self.elements.append(score_img)
        self.elements.append(Spacer(1, 10))
        
        # Add severity pie chart if available
        severity_buf = generate_severity_pie(severities)
        if severity_buf:
            self.elements.append(Paragraph("Issues by Severity", self.styles['NormalStyle']))
            sev_img = Image(severity_buf, width=300, height=300)
            self.elements.append(sev_img)
            self.elements.append(Spacer(1, 10))
            
    def add_issues_table(self, issues: list[dict]):
        if not issues:
            self.elements.append(Paragraph("No critical issues detected. Great job!", self.styles['NormalStyle']))
            return
            
        self.elements.append(Paragraph("Detected Issues", self.styles['HeadingStyle']))
        
        data = [["Severity", "Module", "Title"]]
        for issue in issues:
            data.append([issue.get('severity', 'info'), issue.get('module', 'unknown'), issue.get('title', 'Unknown Issue')])
            
        t = Table(data, colWidths=[80, 100, 300])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F8FAFC')),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#E2E8F0'))
        ]))
        
        self.elements.append(t)
        self.elements.append(Spacer(1, 20))
        
    def generate(self):
        doc = SimpleDocTemplate(self.filename, pagesize=letter)
        doc.build(self.elements)
        return self.filename
