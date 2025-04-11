import os
from dotenv import load_dotenv
from pathlib import Path
import yaml

# 加载 .env 文件
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

class ENV_CONFIG:
    def __init__(self):
        # 邮箱配置
        self.EMAIL_USER = os.getenv("EMAIL_USER")
        self.EMAIL_PASS = os.getenv("EMAIL_TOKEN")
        self.EMAIL_RECEIVERS = os.getenv("EMAIL_RECEIVERS", "").split(",")
        self.EMAIL_RECEIVERS = [email.strip() for email in self.EMAIL_RECEIVERS if email.strip()]
        self.SMTP_SERVER = "smtp.qq.com"
        self.SMTP_PORT = 465

        # Tushare Token
        self.TUSHARE_TOKEN = os.getenv("TUSHARE_TOKEN")

    # 股票列表
    def load_stock_list():
        with open("config/stock_list.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)["stocks"]

    # RSS 新闻源
    def load_rss_feeds():
        with open("config/rss_feeds.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)["feeds"]

if __name__ == "__main__":
    env_config = ENV_CONFIG()
    print(env_config.EMAIL_USER)
    print(env_config.EMAIL_PASS)
    print(env_config.EMAIL_RECEIVERS)
    print(env_config.SMTP_SERVER)
    print(env_config.SMTP_PORT)