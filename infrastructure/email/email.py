import os
from infrastructure.email.smtp import SMTPService


class EmailService():
    

    @staticmethod
    def send_email(to_address, subject, body):
        email_service = SMTPService(
            smtp_server='smtp.gmail.com',
            smtp_port=465,
            smtp_username=os.environ["EMAIL_USER"],
            smtp_password=os.environ["EMAIL_PASSWORD"]
        )
        return email_service.send_html_email(to_address, subject, body)

