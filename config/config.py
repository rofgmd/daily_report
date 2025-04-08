import os
from dotenv import load_dotenv
from pathlib import Path
import yaml

# 加载 .env 文件
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# 邮箱配置
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_TOKEN")
EMAIL_RECEIVERS = os.getenv("EMAIL_RECEIVERS", "").split(",")
EMAIL_RECEIVERS = [email.strip() for email in EMAIL_RECEIVERS if email.strip()]
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465

# Tushare Token
TUSHARE_TOKEN = os.getenv("TUSHARE_TOKEN")

# 股票列表
def load_stock_list():
    with open("config/stock_list.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["stocks"]

# RSS 新闻源
def load_rss_feeds():
    with open("config/rss_feeds.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["feeds"]
