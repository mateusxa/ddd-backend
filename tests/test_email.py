import os
from dotenv import load_dotenv
from infrastructure.email.email import EmailService

load_dotenv()


def test_send_email():
    EmailService.send_email(os.environ["TARGET_EMAIL"], "teste", "teste")
