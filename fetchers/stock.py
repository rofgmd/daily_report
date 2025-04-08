import requests
from datetime import datetime

# 支持多个指数代码：上证、深成、创业板、恒指、美股（用新浪提供的代码）
CHINESE_MARKET_CODES = {
    "上证指数": "sh000001",
    "深证成指": "sz399001",
    "创业板指": "sz399006"
}

def get_chinese_stock_info(code: str) -> str:
    url = f"http://hq.sinajs.cn/list={code}"
    headers = {
        "Referer": "http://finance.sina.com.cn",
        "User-Agent": "Mozilla/5.0"
    }

    # 请求并转码为 utf-8（新浪返回的是 gb2312 编码）
    resp = requests.get(url, headers=headers)
    raw = resp.content.decode("gb2312")

    # 拆解数据字段
    try:
        data = raw.split('"')[1].split(',')
        name = raw.split('=')[0].split('_')[-1]
        price = data[3]
        change = float(data[3]) - float(data[2])
        pct = (change / float(data[2])) * 100
        amount = float(data[9]) / 100000000  # 单位转为亿
        direction = "上涨" if change > 0 else "下跌" if change < 0 else "持平"

        return f"指数收盘价 {price}，{direction} {abs(pct):.2f}%（{change:+.2f}），成交额 {amount:.2f}亿"
    except Exception as e:
        return f"获取失败: {e}"

def fetch_all_markets():
    results = []
    for name, code in CHINESE_MARKET_CODES.items():
        result = get_chinese_stock_info(code)
        results.append(f"{name}：{result}")
    return results

if __name__ == "__main__":
    for line in fetch_all_markets():
        print(line)