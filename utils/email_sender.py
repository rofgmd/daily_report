import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
import config

def send_email(subject, html_content):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = config.EMAIL_USER
    msg['To'] = ", ".join(config.EMAIL_RECEIVERS)

    msg.attach(MIMEText(html_content, 'html'))

    with smtplib.SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT) as smtp:
        smtp.login(config.EMAIL_USER, config.EMAIL_PASS)
        smtp.sendmail(config.EMAIL_USER, config.EMAIL_RECEIVERS, msg.as_string())