from utils import email_sender
from fetchers.stock import get_mainland_china_index_info, get_mainland_china_stock_watchlist, get_hk_index_info, get_hk_stock_watchlist, get_us_index_info, get_us_stock_watchlist, get_global_index_info
from fetchers.it_news import get_it_news_for_report
from template.daily_email import render_email_content
from fetchers.weather import shenzhen_weather
import time

if __name__ == "__main__":
    subject = "每日早报"
    html_content = render_email_content(
        get_mainland_china_index_info(),
        get_mainland_china_stock_watchlist(),
        get_hk_index_info(),
        get_hk_stock_watchlist(),
        get_us_index_info(),
        get_us_stock_watchlist(),
        get_global_index_info(), 
        get_it_news_for_report(),
        shenzhen_weather()
    )
    today = time.strftime("%Y-%m-%d", time.localtime())
    try:
        email_sender.send_email(subject, html_content)
        print(f"✅ {today}邮件发送成功")
    except Exception as e:
        print(f"❌ {today}邮件发送失败：{e}")