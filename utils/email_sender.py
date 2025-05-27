import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
from conf.env_config import ENV_CONFIG

def send_email(subject, html_content):
    msg = MIMEMultipart()
    env_config = ENV_CONFIG()
    msg['Subject'] = subject
    msg['From'] = env_config.EMAIL_USER
    msg['To'] = ", ".join(env_config.EMAIL_RECEIVERS)

    msg.attach(MIMEText(html_content, 'html'))

    try:
        smtp = smtplib.SMTP_SSL(env_config.SMTP_SERVER, env_config.SMTP_PORT)
        smtp.login(env_config.EMAIL_USER, env_config.EMAIL_PASS)
        smtp.sendmail(env_config.EMAIL_USER, env_config.EMAIL_RECEIVERS, msg.as_string())
        smtp.quit()
        # print("邮件发送成功")
    except Exception as e:
        print("邮件发送失败", e)

if __name__ == "__main__":
    subject = "测试日报：来自 send_email 实际发送"
    html_content = """
    <html>
        <body>
            <h2>这是一封测试邮件</h2>
            <p>该邮件由 <strong>send_email</strong> 函数真实发送。</p>
        </body>
    </html>
    """

    send_email(subject, html_content)