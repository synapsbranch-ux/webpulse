import os
from pathlib import Path
import logging
from typing import Any
import resend
from jinja2 import Environment, FileSystemLoader

from app.config import settings

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        resend.api_key = settings.RESEND_API_KEY
        self.from_email = settings.EMAIL_FROM
        
        # Setup Jinja2 Environment
        template_dir = Path(__file__).parent.parent / "templates"
        self.jinja_env = Environment(loader=FileSystemLoader(str(template_dir)))
        
    def _render_template(self, template_name: str, **kwargs: Any) -> str:
        template = self.jinja_env.get_template(template_name)
        return template.render(**kwargs)

    async def send_verification_email(self, email: str, token: str) -> None:
        """Sends an email verification link to a new user."""
        try:
            # In production, use your actual frontend URL config
            verification_link = f"http://localhost:3000/verify-email?token={token}"
            html_content = self._render_template("email_verify.html", verification_link=verification_link)
            
            params = {
                "from": self.from_email,
                "to": [email],
                "subject": "Vérifiez votre adresse email sur synapsbranch",
                "html": html_content
            }
            
            resend.Emails.send(params)
            logger.info(f"Verification email sent to {email}")
        except Exception as e:
            logger.error(f"Failed to send verification email to {email}: {e}")

    async def send_reset_email(self, email: str, token: str) -> None:
        """Sends a password reset link."""
        try:
            reset_link = f"http://localhost:3000/reset-password?token={token}"
            html_content = self._render_template("email_reset.html", reset_link=reset_link)
            
            params = {
                "from": self.from_email,
                "to": [email],
                "subject": "Réinitialisation de votre mot de passe",
                "html": html_content
            }
            
            resend.Emails.send(params)
            logger.info(f"Reset email sent to {email}")
        except Exception as e:
            logger.error(f"Failed to send reset email to {email}: {e}")

    async def send_report_email(self, email: str, user_name: str, scan_url: str, score: int, pdf_path: str) -> None:
        """Sends the final report PDF to the user."""
        try:
            html_content = self._render_template(
                "email_report.html", 
                user_name=user_name, 
                scan_url=scan_url, 
                score=score
            )
            
            # Read PDF file
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
                
            params = {
                "from": self.from_email,
                "to": [email],
                "subject": f"Rapport d'analyse terminé - {scan_url}",
                "html": html_content,
                "attachments": [
                    {
                        "filename": f"synapsbranch_report_{score}_100.pdf",
                        "content": list(pdf_bytes) # Resend requires list of bytes or base64
                    }
                ]
            }
            
            resend.Emails.send(params)
            logger.info(f"Report email sent to {email}")
        except Exception as e:
            logger.error(f"Failed to send report email to {email}: {e}")
