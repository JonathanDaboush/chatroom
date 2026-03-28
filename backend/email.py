import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import os

def send_html_email(
    to_email: str,
    subject: str,
    context: Optional[dict[str, str]] = None,
    template_type: str = "new_user",
    template_path: Optional[str] = None
):
    """
    Send an HTML email using a template type (new_user, forgot_password, delete_account) or a custom template_path.
    context: Optional[dict[str, str]] - values to fill in the template using str.format(**context)
    """
    if template_path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        templates = {
            "new_user": os.path.join(base_dir, "emailTemplates", "newUser.html"),
            "forgot_password": os.path.join(base_dir, "emailTemplates", "forgotPassword.html"),
            "delete_account": os.path.join(base_dir, "emailTemplates", "deleteAccount.html"),
        }
        template_path = templates.get(template_type)
        if template_path is None:
            raise ValueError(f"Unknown template_type: {template_type}")
    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()
    if context:
        html = html.format(**context)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = os.environ.get('EMAIL_FROM', 'noreply@example.com')
    msg['To'] = to_email
    part = MIMEText(html, 'html')
    msg.attach(part)
    # Example SMTP config (customize for your environment)
    smtp_host = os.environ.get('SMTP_HOST', 'localhost')
    smtp_port = int(os.environ.get('SMTP_PORT', 25))
    smtp_user = os.environ.get('SMTP_USER')
    smtp_pass = os.environ.get('SMTP_PASS')
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        if smtp_user and smtp_pass:
            server.starttls()
            server.login(smtp_user, smtp_pass)
        server.sendmail(msg['From'], [to_email], msg.as_string())
