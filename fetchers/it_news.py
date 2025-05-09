import yaml
import os
from utils.rss_reader import fetch_rss_feed
from datetime import datetime, timedelta
import pytz

def get_it_news_from_yaml(yaml_path="conf/rss_feeds.yaml", max_items=5):
    it_news_items = []
    full_path = os.path.join(os.path.dirname(__file__), "..", yaml_path)
    with open(full_path, "r") as f:
        feeds_config = yaml.safe_load(f)
        it_news_urls = feeds_config.get("feeds", {}).get("it_news", [])
        for url in it_news_urls:
            entries = fetch_rss_feed(url, max_items=max_items)
            for item in entries:
                it_news_items.append(f"{item['published']} - {item['title']}\n{item['link']}\n")
    return it_news_items

def get_it_news_for_report():
    tz = pytz.timezone("Asia/Shanghai")
    now = datetime.now(tz)
    today_8am = now.replace(hour=8, minute=0, second=0, microsecond=0)
    yesterday_11pm = (today_8am - timedelta(days=1)).replace(hour=23)
    raw_items = get_it_news_from_yaml(max_items=100)
    result = []
    for item in raw_items:
        try:
            published_str, rest = item.split(" - ", 1)
            title_line, url = rest.strip().split("\n", 1)
            published_dt = datetime.strptime(published_str, "%Y-%m-%d %H:%M:%S %Z")
            published_dt = tz.localize(published_dt.replace(tzinfo=None))

            if yesterday_11pm <= published_dt < today_8am:
                result.append([published_dt.strftime("%Y-%m-%d %H:%M"), title_line.strip(), url.strip()])
        except Exception:
            continue  # skip malformed items
    return result



if __name__ == "__main__":
    it_news = get_it_news_for_report()
    for news in it_news:
        print(news)