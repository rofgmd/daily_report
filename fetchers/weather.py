import requests
import json
from pprint import pprint

# 城市代码：中国天气网 weather.com.cn 查询得到
cities = {
    "深圳": "101280601",
    "广州": "101280101",
    "上海": "101020100",
    "北京": "101010100"
}

class Weather_Info():
    def __init__(self, city, updateTime, weather_data):
        self.city = city
        self.updateTime = updateTime
        self.quality = weather_data.get("quality", "")
        self.moisture = weather_data.get("shidu", "")
        forecast = weather_data.get("forecast", [])
        if forecast:
            today = forecast[0]
            self.low_temperature = today.get("low", "").split(" ")[-1]
            self.high_temperature = today.get("high", "").split(" ")[-1]
            self.sunrise = today.get("sunrise", "")
            self.sunset = today.get("sunset", "")
            self.weather_type = today.get("type", "")
            self.notice = today.get("notice", "")

def fetch_weather(city_code) -> Weather_Info:
    url = f"http://t.weather.itboy.net/api/weather/city/{city_code}"
    try:
        response = requests.get(url, timeout=10)  # 添加 timeout 更安全
        response.raise_for_status()  # 如果响应状态码不是 200，将抛出异常
        data = response.json()  # 解析 JSON 数据

        # 获取字段
        city = data.get("cityInfo", {}).get("city", "")
        updateTime = data.get("cityInfo", {}).get("updateTime", "unknown")
        weather_data = data.get("data", {})
        city_weather = Weather_Info(city, updateTime, weather_data)
        # 返回你需要的字段
        return city_weather
    except Exception as e:
        return Weather_Info(city="未知城市", updateTime="接口异常", weather_data={})

def shenzhen_weather():
    info = fetch_weather(cities["深圳"])
    if isinstance(info, Weather_Info):
        try:
            return (f"{info.city}今日天气如下：气温{info.low_temperature}-{info.high_temperature}，湿度{info.moisture}，总体天气为{info.weather_type}，{info.notice}")
        except AttributeError as e:
            print(f"[WARNING] 天气信息缺失：{e}")
            return "获取天气信息不完整，使用默认值。"
    else:
        return "获取天气信息失败，使用默认值。"

if __name__ == "__main__":
    print(shenzhen_weather())