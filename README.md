# daily_report

`daily_report` 是一个基于 Python 的自动化信息整合与推送系统，专为每天早上生成个性化的“每日早报”而设计。
该系统整合了 **股票行情、主流新闻、科技资讯** 等内容，并通过 **电子邮件自动推送**，帮助用户在一天开始前快速掌握重要资讯。

---

## ✨ 当前功能进度

| 模块       | 功能描述                                 | 状态      |
| ---------- | ---------------------------------------- | --------- |
| A股大盘行情    | 基于新浪财经接口获取上证/深证/创业板数据 | ✅ 已完成 |
| 节假日判断 | 判断昨日是否为交易日     | ✅ 已完成 |
| 邮件推送   | SMTP 邮件发送模块                        | ✅ 已完成 |
| 科技新闻   | 支持 RSS 新闻源（如 ITHome、少数派）     | ⏳ 开发中 |
| HTML 模板  | 渲染为 HTML 邮件                         | 🛠 规划中 |
| 多市场支持 | 港股、美股行情                           | 🛠 规划中 |
| 体育新闻   | 获取足球、NBA等新闻                      | 🛠 规划中 |

---

## 🛠 项目结构概览

```markdown
├── CHANGELOG.md
├── conf
│   ├── __init__.py
│   ├── env_config.py
│   ├── rss_feeds.yaml
│   └── stock_list.yaml
├── fetchers
│   ├── __init__.py
│   └── stock.py
├──utils
│    ├── __init__.py
│    ├── email_sender.py
│    └── trading_calendar
│       ├── __init__.py
│       ├── base.py
│       └── date_utils.py
├── .env
├── .gitignore
├── main.py
├── README.md
└── requirements.txt

6 directories, 15 files
```

---

## 📦 安装与部署

### 本地部署

#### 1. 克隆项目

```bash
git clone https://github.com/rofgmd/daily_report.git
cd daily_report
```

### 2. 安装依赖

建议使用虚拟环境（如 `venv` / `conda`）

```bash
python -m venv report
source report/bin/activate
pip install -r requirements.txt
```

### 3. 创建环境变量`.env` 文件

```env
EMAIL_USER=your_email@qq.com
EMAIL_PASS=your_smtp_code
EMAIL_RECEIVERS=receiver1@example.com,receiver2@example.com
TUSHARE_TOKEN=your_tushare_token
```

将 `.env` 加入 `.gitignore` 避免泄露敏感信息。

---

## 🚀 功能测试用例

### 获取 A 股行情数据：

```bash
python -m fetchers.stock
```

示例输出：

```
上证指数：指数收盘价 3113.45，上涨 0.54%（+16.87），成交额 6465.10亿
深证成指：指数收盘价 9332.50，下跌 0.34%（-31.99），成交额 8044.22亿
创业板指：指数收盘价 1821.21，上涨 0.77%（+14.00），成交额 3502.26亿
```

### 测试交易日

```bash
reportkevinweng@KevindeMacBook-Air daily_report % python -m utils.trading_calendar.date_utils
```

示例输出：

```markdown
今天是否交易日： True
最近一个交易日： 20250408
格式化： 2025-04-08
```

### 测试STMP邮件发送功能

```bash
python -m utils.email_sender
```

示例输出：

```markdown
邮件发送成功
邮件发送失败
```

---

## 📌 TODO_LIST（未来计划）

- [ ] 完成邮件模块并自动推送日报
- [ ] 添加科技资讯（RSS 抓取）
- [ ] 添加体育资讯
- [ ] 增加港股、美股等多市场行情
- [ ] 支持 HTML 邮件格式模板
- [ ] 使用 Docker 部署或定时任务

---
