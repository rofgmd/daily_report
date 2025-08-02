import requests
import re
import os
import yaml
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# 支持多个指数代码：上证、深成、创业板、恒指、美股（用新浪提供的代码）
MAINLAND_CHINESE_MARKET_CODES = {
    "上证指数": "sh000001",
    "深证成指": "sz399001",
    "创业板指": "sz399006"
}

US_MARKET_CODES = {
    "道琼斯": "gb_dji", 
    "纳斯达克": "gb_ixic"
}

def get_mainland_chinese_stock_info(code: str) -> str:
    url = f"http://hq.sinajs.cn/list={code}"
    headers = {
        "Referer": "http://finance.sina.com.cn",
        "User-Agent": "Mozilla/5.0"
    }
    # 请求并转码为 utf-8（新浪返回的是 gb2312 编码）
    resp = requests.get(url, headers=headers)
    raw = resp.content.decode("gb2312")
    lines = raw.strip().split(";\n")
    results = []
    for line in lines:
        if not line.strip():
            continue
        var_name = line.split("=")[0].strip()
        key_raw = var_name.split("_")[-1].upper()
        content = line.split("=")[1].strip().strip('"')
        fields = content.split(',')
        try:
            name = fields[0]
            price = float(fields[3])
            change = float(fields[3]) - float(fields[2])
            pct = (change / float(fields[2])) * 100
            amount = float(fields[9]) / 100000000  # 单位转为亿
            direction = "上涨" if change > 0 else "下跌" if change < 0 else "持平"

            result = f"{name}：收盘价 {price}，{direction} {abs(pct):.2f}%（{change:+.2f}），成交额 {amount:.2f}亿"
            results.append(result)
        except Exception as e:
            return f"获取失败: {e}"  

    return "\n".join(results)  

def get_mainland_chinese_stock_info_list(code: str) -> list[dict]:

    url = f"http://hq.sinajs.cn/list={code}"
    headers = {
        "Referer": "http://finance.sina.com.cn",
        "User-Agent": "Mozilla/5.0"
    }
    resp = requests.get(url, headers=headers)
    raw = resp.content.decode("gb2312")
    lines = raw.strip().split(";\n")
    results = []

    for line in lines:
        if not line.strip():
            continue
        content = line.split("=")[1].strip().strip('"')
        fields = content.split(',')
        try:
            name = fields[0]
            prev_close = float(fields[2])
            price = float(fields[3])
            change = price - prev_close
            pct = (change / prev_close) * 100
            amount = float(fields[9]) / 1e8  # 亿
            direction = "上涨" if change > 0 else "下跌" if change < 0 else "持平"

            results.append({
                "name": name,
                "price": f"{price:.2f}",
                "direction": f"{pct:+.2f}%",
                "volume": f"{amount:.2f}亿"
            })
        except Exception as e:
            results.append({
                "name": "解析失败",
                "price": "N/A",
                "direction": "N/A",
                "volume": f"错误: {e}"
            })

    return results

def get_mainland_china_stock_watchlist(config_file: str = "conf/stock_list.yaml", config_key: str = "stocks_cn"):
    with open(config_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    stocks_list = config[config_key]
    stocks_code  = ','.join(stocks_list)
    result = get_mainland_chinese_stock_info_list(stocks_code)
    return result

def get_mainland_china_index_info() -> str:
    url = "http://hq.sinajs.cn/list=sh000001,sz399001,sz399006"
    headers = {
        "Referer": "http://finance.sina.com.cn",
        "User-Agent": "Mozilla/5.0"
    }
    # 请求并转码为 utf-8（新浪返回的是 gb2312 编码）
    resp = requests.get(url, headers=headers)
    raw = resp.content.decode("gb2312")
    lines = raw.strip().split(";\n")
    results = []
    for line in lines:
        if not line.strip():
            continue
        var_name = line.split("=")[0].strip()
        key_raw = var_name.split("_")[-1].upper()
        content = line.split("=")[1].strip().strip('"')
        fields = content.split(',')
        try:
            name = fields[0]
            price = float(fields[3])
            change = float(fields[3]) - float(fields[2])
            pct = (change / float(fields[2])) * 100
            amount = float(fields[9]) / 100000000  # 单位转为亿
            direction = "上涨" if change > 0 else "下跌" if change < 0 else "持平"

            result = f"{name}：指数收盘价 {price}，{direction} {abs(pct):.2f}%（{change:+.2f}），成交额 {amount:.2f}亿"
            results.append(result)
        except Exception as e:
            return f"获取失败: {e}"  

    return "\n".join(results)  

def get_hk_index_info() -> str:
    url = "https://hq.sinajs.cn/?_=1744186268202&list=rt_hkHSI"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
        "Referer": "https://finance.sina.com.cn/",
        "Content-Type": "application/javascript; charset=GB18030",
    }

    response = requests.get(url, headers=headers)
    response.encoding = "GB18030"  # 设置正确编码

    raw_data = response.text
    data_str = raw_data.split('"')[1]
    fields = data_str.split(',')
    direction = "上涨" if float(fields[7]) > 0 else "下跌" if float(fields[7]) < 0 else "持平"
    return f"恒生指数：指数收盘价 {fields[6]}，{direction} {abs(float(fields[8])):.2f}%（{float(fields[7]):+.2f}），成交额 {float(fields[11])/100000:.2f}亿"    

def get_hk_stock_info_list(code: str) -> str:
    url = f"https://hq.sinajs.cn/list={code}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
        "Referer": "https://finance.sina.com.cn/",
        "Content-Type": "application/javascript; charset=GB18030",
    }

    response = requests.get(url, headers=headers)
    response.encoding = "GB18030"  # 设置正确编码
    lines = response.text.strip().split(";\n")
    results = []
    for line in lines:
        if not line.strip():
            continue

        data_str = line.split('"')[1]
        fields = data_str.split(',')
        try:
            name = fields[1]
            prev_close = float(fields[3])
            price = float(fields[6])
            change = float(fields[7])
            pct = (change / prev_close) * 100
            amount = float(fields[11]) / 1e8  # 亿
            direction = "上涨" if change > 0 else "下跌" if change < 0 else "持平"

            results.append({
                "name": name,
                "price": f"{price:.2f}",
                "direction": f"{pct:+.2f}%",
                "volume": f"{amount:.2f}亿"
            })
        except Exception as e:
            results.append({
                "name": "解析失败",
                "price": "N/A",
                "direction": "N/A",
                "volume": f"错误: {e}"
            })

    return results

def get_hk_stock_watchlist(config_file: str = "conf/stock_list.yaml", config_key: str = "stocks_hk"):
    with open(config_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    stocks_list = config[config_key]
    stocks_code  = ','.join(stocks_list)
    result = get_hk_stock_info_list(stocks_code)
    return result

def get_us_index_info() -> str:
    url = "https://hq.sinajs.cn/?_=0.7533239877415743&list=gb_$dji,gb_ixic,gb_$inx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
        "Referer": "https://stock.finance.sina.com.cn/usstock/quotes/.DJI.html",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-HK;q=0.5",
        "Connection": "Keep-Alive",
        "Content-Type": "application/javascript; charset=GB18030",
    }
    response = requests.get(url, headers=headers)
    response.encoding = "GB18030"
    data = response.text

    # 拆分成两段数据
    lines = data.strip().split(";\n")
    results = []
    name_list = ["道琼斯", "纳斯达克", "标普500"]
    for index, line in enumerate(lines):
        if not line.strip():
            continue
        var_name = line.split("=")[0].strip()
        content = line.split("=")[1].strip().strip('"')
        fields = content.split(',')

        # 指数中文名（fields[0] 乱码可能会因终端显示问题而异常）
        name = var_name.split("_")[-1].upper()  # eg. gb_$dji -> $DJI
        direction = "上涨" if float(fields[4]) > 0 else "下跌" if float(fields[4]) < 0 else "持平"
        result = f"{name_list[index]}：指数收盘价 {fields[1]}，{direction} {abs(float(fields[2])):.2f}%（{float(fields[4]):+.2f}），成交额 {float(fields[10])/100000000:.2f}亿"
        results.append(result)
    
    return "\n".join(results)

def get_us_stock_info_list(code: str) -> str:
    url = f"https://hq.sinajs.cn/list={code}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
        "Referer": "https://stock.finance.sina.com.cn/usstock/quotes/.DJI.html",
        "Content-Type": "application/javascript; charset=GB18030",
    }

    response = requests.get(url, headers=headers)
    response.encoding = "GB18030"  # 设置正确编码
    lines = response.text.strip().split(";\n")
    results = []
    for line in lines:
        if not line.strip():
            continue

        data_str = line.split('"')[1]
        fields = data_str.split(',')
        try:
            name = fields[0]
            price = float(fields[1])
            pct = float(fields[2])
            amount = float(fields[-6]) / 1e8  # 亿
            cap = float(fields[12])/ 1e8

            results.append({
                "name": name,
                "price": f"{price:.2f}",
                "direction": f"{pct:+.2f}%",
                "volume": f"{amount:.2f}亿",
                "cap": f"{cap:.2f}亿",
            })
        except Exception as e:
            results.append({
                "name": "解析失败",
                "price": "N/A",
                "direction": "N/A",
                "volume": f"错误: {e}",
                cap: "N/A",
            })

    return results

def get_us_stock_watchlist(config_file: str = "conf/stock_list.yaml", config_key: str = "stocks_us"):
    with open(config_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    stocks_list = config[config_key]
    stocks_code  = ','.join(stocks_list)
    result = get_us_stock_info_list(stocks_code)
    return result

def get_global_index_info() -> str:
    url = "https://hq.sinajs.cn/?list=znb_UKX,znb_DAX,znb_CAC,znb_NKY,znb_KOSPI,znb_TWJQ"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
        "Referer": "https://stock.finance.sina.com.cn",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-HK;q=0.5",
        "Connection": "Keep-Alive",
        "Content-Type": "application/javascript; charset=GB18030",
    }

    response = requests.get(url, headers=headers)
    response.encoding = "GB18030"
    data = response.text

    lines = data.strip().split(";\n")
    results = []

    name_list= ["英国富时100", "德国DAX指数", "法国CAC40指数", "日经225指数", "韩国首尔综合指数", "台湾加权指数"]

    for line in lines:
        if not line.strip():
            continue
        var_name = line.split("=")[0].strip()
        key_raw = var_name.split("_")[-1].upper()
        content = line.split("=")[1].strip().strip('"')
        fields = content.split(',')

        try:
            change = float(fields[2])
            direction = "上涨" if change > 0 else "下跌" if change < 0 else "持平"
            result = f"{fields[0]}：指数收盘价 {fields[1]}，{direction} {abs(float(fields[3])):.2f}%（{change:+.2f}）"
            results.append(result)                
        except (ValueError, IndexError):
            continue  # 某些字段异常就跳过

    return "\n".join(results)

def fetch_all_markets():
    results = []
    results.append(get_mainland_china_index_info())
    results.append(get_hk_index_info())
    results.append(get_us_index_info())
    results.append(get_global_index_info())
    return results

if __name__ == "__main__":
    for line in fetch_all_markets():
        print(line)