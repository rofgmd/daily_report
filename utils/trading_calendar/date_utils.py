import tushare as ts
import os
from datetime import datetime, timedelta
from config.config import TUSHARE_TOKEN

ts.set_token(TUSHARE_TOKEN)
pro = ts.pro_api()

def is_today_trading_day() -> bool:
    today = datetime.today().strftime('%Y%m%d')
    df = pro.trade_cal(exchange='SSE', start_date=today, end_date=today)
    return not df.empty and df.iloc[0]['is_open'] == 1

def get_last_trading_date() -> str:
    today = datetime.today().strftime('%Y%m%d')
    df = pro.trade_cal(exchange='SSE', end_date=today)
    df = df[df['is_open'] == 1]
    if df.empty:
        return None
    return df.iloc[-1]['cal_date']

if __name__ == "__main__":
    print("今天是否交易日：", is_today_trading_day())

    last_day = get_last_trading_date()
    print("最近一个交易日：", last_day)
    # 可选：格式化输出
    if last_day:
        print("格式化：", datetime.strptime(last_day, "%Y%m%d").strftime("%Y-%m-%d"))
