from flask_mail import Message
from flask import render_template
from dotenv import load_dotenv
from extensions import mail
import os

load_dotenv()

def send_email(subjet, body, recipient):
    msg = Message(
        subject=subjet,
        recipients=[recipient],
        sender=os.environ.get('MAIL_DEFAULT_SENDER'),
        body=body
    )

    mail.send(msg)