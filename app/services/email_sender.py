import smtplib
from email.mime.text import MIMEText
from core.config import mail_settings

def send_email_with_attachment(
    recipient: str,
    subject: str, 
    body: str,
    # file_content: bytes = None, file_name: str = None
):
    try:
        msg = MIMEText(body,"html")
        msg["Subject"] = subject
        msg["From"] = mail_settings.FROM_EMAIL
        msg["To"] = recipient

        with smtplib.SMTP(host=mail_settings.SMTP_SERVER, port=mail_settings.SMTP_PORT) as server:
            server.starttls()
            server.login(user=mail_settings.SMTP_USERNAME,password=mail_settings.SMTP_PASSWORD)
            server.sendmail(mail_settings.FROM_EMAIL, recipient, msg.as_string())

        print(f"Email sent to {recipient}")

    except Exception as e:
        print(f"Error sending Email: {e}")