"""
Email Service
Handles sending approval emails using SMTP
"""

import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()


class EmailService:
    """Service for sending emails via SMTP"""
    
    def __init__(
        self,
        smtp_host: Optional[str] = None,
        smtp_port: Optional[int] = None,
        smtp_user: Optional[str] = None,
        smtp_password: Optional[str] = None
    ):
        """
        Initialize email service
        
        Args:
            smtp_host: SMTP server hostname
            smtp_port: SMTP server port
            smtp_user: SMTP username
            smtp_password: SMTP password
        """
        self.smtp_host = smtp_host or os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = smtp_port or int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = smtp_user or os.getenv("SMTP_USER", "")
        self.smtp_password = smtp_password or os.getenv("SMTP_PASSWORD", "")
        
        # Check if credentials are configured
        self.is_configured = bool(self.smtp_user and self.smtp_password)
        
        if not self.is_configured:
            print("⚠️ Email service not configured. Set SMTP_USER and SMTP_PASSWORD in .env")
    
    async def send_approval_email(
        self,
        recipient_email: str,
        survey_title: str,
        form_url: str,
        approver_name: str,
        custom_message: Optional[str] = None
    ) -> bool:
        """
        Send an approval email with the form link
        
        Args:
            recipient_email: Email address of the recipient
            survey_title: Title of the survey
            form_url: URL of the Google Form
            approver_name: Name of the person who approved
            custom_message: Optional custom message to include
        
        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.is_configured:
            print("⚠️ Cannot send email: SMTP not configured")
            print(f"📧 Would have sent email to: {recipient_email}")
            print(f"📝 Survey: {survey_title}")
            print(f"🔗 Form URL: {form_url}")
            return False
        
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = f"Survey Approved: {survey_title}"
            message["From"] = self.smtp_user
            message["To"] = recipient_email
            
            # Create email body
            text_body = self._create_text_email_body(
                survey_title, form_url, approver_name, custom_message
            )
            html_body = self._create_html_email_body(
                survey_title, form_url, approver_name, custom_message
            )
            
            # Attach both plain text and HTML versions
            part1 = MIMEText(text_body, "plain")
            part2 = MIMEText(html_body, "html")
            message.attach(part1)
            message.attach(part2)
            
            # Send email
            await aiosmtplib.send(
                message,
                hostname=self.smtp_host,
                port=self.smtp_port,
                username=self.smtp_user,
                password=self.smtp_password,
                start_tls=True
            )
            
            print(f"✅ Email sent successfully to {recipient_email}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False
    
    def _create_text_email_body(
        self,
        survey_title: str,
        form_url: str,
        approver_name: str,
        custom_message: Optional[str] = None
    ) -> str:
        """Create plain text email body"""
        body = f"""
Survey Approval Notification

Hello,

The survey "{survey_title}" has been approved by {approver_name}.

You can now access and share the survey using the following link:
{form_url}

"""
        if custom_message:
            body += f"""
Message from the approver:
{custom_message}

"""
        
        body += """
Thank you for using SurveyForge!

---
This is an automated message from the Survey Creation & Review System.
"""
        return body
    
    def _create_html_email_body(
        self,
        survey_title: str,
        form_url: str,
        approver_name: str,
        custom_message: Optional[str] = None
    ) -> str:
        """Create HTML email body"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 8px 8px 0 0;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .content {{
            background: #ffffff;
            padding: 30px;
            border: 1px solid #e5e7eb;
            border-top: none;
        }}
        .survey-title {{
            font-size: 20px;
            font-weight: 600;
            color: #667eea;
            margin: 20px 0;
        }}
        .button {{
            display: inline-block;
            padding: 12px 30px;
            background: #667eea;
            color: white !important;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
            margin: 20px 0;
        }}
        .button:hover {{
            background: #5568d3;
        }}
        .custom-message {{
            background: #f9fafb;
            border-left: 4px solid #667eea;
            padding: 15px;
            margin: 20px 0;
            font-style: italic;
        }}
        .footer {{
            background: #f9fafb;
            padding: 20px;
            border-radius: 0 0 8px 8px;
            text-align: center;
            font-size: 12px;
            color: #6b7280;
            border: 1px solid #e5e7eb;
            border-top: none;
        }}
        .approved-by {{
            color: #059669;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>✅ Survey Approved</h1>
    </div>
    
    <div class="content">
        <p>Hello,</p>
        
        <p>Great news! The survey has been approved and is ready to share.</p>
        
        <div class="survey-title">"{survey_title}"</div>
        
        <p>Approved by: <span class="approved-by">{approver_name}</span></p>
"""
        
        if custom_message:
            html += f"""
        <div class="custom-message">
            <strong>Message from the approver:</strong><br>
            {custom_message}
        </div>
"""
        
        html += f"""
        <p>Click the button below to access the survey:</p>
        
        <center>
            <a href="{form_url}" class="button">Open Survey Form</a>
        </center>
        
        <p style="font-size: 12px; color: #6b7280; margin-top: 20px;">
            Or copy this link: <a href="{form_url}">{form_url}</a>
        </p>
    </div>
    
    <div class="footer">
        <p>This is an automated message from <strong>SurveyForge</strong></p>
        <p>Survey Creation & Review System</p>
    </div>
</body>
</html>
"""
        return html
    
    async def send_notification_email(
        self,
        recipient_email: str,
        subject: str,
        message: str
    ) -> bool:
        """
        Send a generic notification email
        
        Args:
            recipient_email: Email address of the recipient
            subject: Email subject
            message: Email message
        
        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.is_configured:
            print("⚠️ Cannot send email: SMTP not configured")
            return False
        
        try:
            # Create message
            email_message = MIMEText(message, "plain")
            email_message["Subject"] = subject
            email_message["From"] = self.smtp_user
            email_message["To"] = recipient_email
            
            # Send email
            await aiosmtplib.send(
                email_message,
                hostname=self.smtp_host,
                port=self.smtp_port,
                username=self.smtp_user,
                password=self.smtp_password,
                start_tls=True
            )
            
            print(f"✅ Notification email sent to {recipient_email}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending notification email: {e}")
            return False


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def test_email():
        service = EmailService()
        
        success = await service.send_approval_email(
            recipient_email="test@example.com",
            survey_title="Customer Satisfaction Survey",
            form_url="https://forms.google.com/example",
            approver_name="John Doe",
            custom_message="Please share this survey with all customers."
        )
        
        if success:
            print("✅ Test email sent successfully")
        else:
            print("❌ Test email failed")
    
    asyncio.run(test_email())
