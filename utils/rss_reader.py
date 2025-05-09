from dateutil import parser
import pytz
import feedparser
import requests

def fetch_rss_feed(url, max_items=5):
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()

        # 检查内容类型
        content_type = resp.headers.get('Content-Type', '')
        if 'xml' not in content_type and 'rss' not in content_type:
            print("返回的不是RSS/XML内容，可能被Cloudflare拦截了")
            print(resp.text[:500])  # 打印部分内容供调试
            return []

        feed = feedparser.parse(resp.content)
        if not feed.entries:
            print("未获取到RSS条目，可能是被替换为HTML页面")
            return []

        entries = []
        for entry in feed.entries[:max_items]:
            item = {
                "title": entry.title,
                "link": entry.link,
                "published": entry.get("published", "无发布时间")
            }
            from datetime import datetime
            try:
                published_time = parser.parse(item["published"])
                local_tz = datetime.now().astimezone().tzinfo
                item["published"] = published_time.astimezone(local_tz).strftime("%Y-%m-%d %H:%M:%S %Z")
            except Exception:
                pass
            entries.append(item)

        return entries
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return []

# 示例调用
if __name__ == "__main__":
    rss_url = "https://rsshub.app/udn/news/breakingnews/99"  # 可以换成你感兴趣的RSS源
    news_items = fetch_rss_feed(rss_url)
    for item in news_items:
        print(f"{item['published']} - {item['title']}\n{item['link']}\n")