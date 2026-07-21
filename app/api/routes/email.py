import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from fastapi import APIRouter, HTTPException
from jinja2 import Environment, FileSystemLoader

from app.core.config import settings
from app.schemas import ContactFormRequest

router = APIRouter(prefix="/mail", tags=["mail"])

# Set up Jinja2 environment
TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates" / "email"
jinja_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


def render_email_template(template_name: str, context: dict) -> str:
    """Render a Jinja2 email template with the given context."""
    template = jinja_env.get_template(template_name)
    return template.render(**context)


def send_html_email(subject: str, html_body: str, to_email: str) -> None:
    """Send an HTML email with a plain text fallback."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = "kickoffteam2@gmail.com"
    msg["To"] = to_email

    # Plain text fallback
    plain_text = "New contact form submission received. Please view this email in an HTML-compatible client."
    part1 = MIMEText(plain_text, "plain")
    part2 = MIMEText(html_body, "html")

    msg.attach(part1)
    msg.attach(part2)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("kickoffteam2@gmail.com", settings.APP_PASSWORD)
        server.send_message(msg, from_addr="kickoffteam2@gmail.com", to_addrs=to_email)


@router.post("/")
def send_mail(form_data: ContactFormRequest):
    """Handle contact form submission and send notification email."""
    timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    context = {
        "firstName": form_data.firstName,
        "lastName": form_data.lastName,
        "address": form_data.address,
        "phone": form_data.phone,
        "email": form_data.email,
        "timestamp": timestamp,
    }

    try:
        html_content = render_email_template("contact_notification.html", context)
        send_html_email(
            subject="New Contact Form Submission - Phillips Family Enterprises",
            html_body=html_content,
            to_email="robcampbell26042604@gmail.com",
        )
    except smtplib.SMTPException as e:
        raise HTTPException(status_code=502, detail=f"Failed to send email: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

    return {"success": True, "message": "Your inquiry has been submitted successfully."}
