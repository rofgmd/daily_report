from utils import email_sender

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

    try:
        email_sender.send_email(subject, html_content)
        print("✅ 邮件发送成功")
    except Exception as e:
        print(f"❌ 邮件发送失败：{e}")