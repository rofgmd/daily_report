from utils import email_sender
from fetchers.stock import get_mainland_china_index_info, get_hk_index_info, get_us_index_info, get_global_index_info
from template.daily_email import render_email_content

if __name__ == "__main__":
    subject = "每日早报测试"
    html_content = render_email_content(
        get_mainland_china_index_info(),
        get_hk_index_info(),
        get_us_index_info(),
        get_global_index_info()
    )

    try:
        email_sender.send_email(subject, html_content)
        print("✅ 邮件发送成功")
    except Exception as e:
        print(f"❌ 邮件发送失败：{e}")