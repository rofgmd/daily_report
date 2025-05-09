from fetchers.stock import get_mainland_china_index_info, get_hk_index_info, get_us_index_info, get_global_index_info
from fetchers.it_news import get_it_news_for_report
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import os

# 映射英文缩写到中文
WEEKDAY_MAP = {
    'Mon': '星期一',
    'Tue': '星期二',
    'Wed': '星期三',
    'Thu': '星期四',
    'Fri': '星期五',
    'Sat': '星期六',
    'Sun': '星期日',
}

def render_email_content(cn_markets, hk_markets, us_markets, global_markets, it_news):
    template_dir = os.path.dirname(__file__)
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('daily_report.html')

    html = template.render(
        date=datetime.now().strftime("%Y年%m月%d日") + "，" + WEEKDAY_MAP[datetime.now().strftime("%a")],
        cn_markets=cn_markets.split("\n"),
        hk_markets=hk_markets,
        us_markets=us_markets.split("\n"),
        global_markets=global_markets.split("\n"),
        it_news = it_news
    )
    return html

if __name__ == "__main__":
    html = render_email_content(
        get_mainland_china_index_info(),
        get_hk_index_info(),
        get_us_index_info(),
        get_global_index_info(), 
        get_it_news_for_report()
    )

    with open("rendered_report.html", "w", encoding="utf-8") as f:
        f.write(html)