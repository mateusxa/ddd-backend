import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SMTPService:
    def __init__(self, smtp_server, smtp_port, smtp_username, smtp_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password

    def send_html_email(self, to_address, subject, body):
        msg = MIMEMultipart()
        msg['From'] = self.smtp_username
        msg['To'] = to_address
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
            server.login(self.smtp_username, self.smtp_password)
            server.send_message(msg)
