import requests
import pprint
import settings

access_key = settings.WEATHER
# https://developer.tech.yandex.ru/services


url = "https://api.weather.yandex.ru/v1/informers"
params = {"lat": 69.352516, "lon": 88.176312}
headers = {"X-Yandex-Weather-Key": access_key}

response = requests.get(url, headers=headers, params=params)
if response.status_code == 200:
    pprint.pprint(response.json())
else:
    print("Ошибка:", response.status_code, response.text)


# Что пришлёт погодный API
result = {
    "fact": {
        "condition": "cloudy",
        "daytime": "d",
        "feels_like": -27,
        "humidity": 78,
        "icon": "bkn_d",
        "obs_time": 1743897600,
        "polar": False,
        "pressure_mm": 739,
        "pressure_pa": 985,
        "season": "spring",
        "temp": -23,
        "wind_dir": "c",
        "wind_gust": 4.7,
        "wind_speed": 0,
    },
    "forecast": {
        "date": "2025-04-06",
        "date_ts": 1743872400,
        "moon_code": 12,
        "moon_text": "first-quarter",
        "parts": [
            {
                "condition": "clear",
                "daytime": "d",
                "feels_like": -22,
                "humidity": 66,
                "icon": "skc_d",
                "part_name": "day",
                "polar": False,
                "prec_mm": 0,
                "prec_period": 360,
                "prec_prob": 0,
                "pressure_mm": 741,
                "pressure_pa": 987,
                "temp_avg": -15,
                "temp_max": -14,
                "temp_min": -16,
                "wind_dir": "e",
                "wind_gust": 5.3,
                "wind_speed": 4.3,
            },
            {
                "condition": "clear",
                "daytime": "d",
                "feels_like": -23,
                "humidity": 71,
                "icon": "skc_d",
                "part_name": "evening",
                "polar": False,
                "prec_mm": 0,
                "prec_period": 240,
                "prec_prob": 0,
                "pressure_mm": 741,
                "pressure_pa": 988,
                "temp_avg": -16,
                "temp_max": -14,
                "temp_min": -18,
                "wind_dir": "e",
                "wind_gust": 5.9,
                "wind_speed": 4.9,
            },
        ],
        "sunrise": "05:50",
        "sunset": "20:29",
        "week": 14,
    },
    "info": {
        "lat": 69.352516,
        "lon": 88.176312,
        "url": "https://yandex.ru/pogoda/11311?lat=69.352516&lon=88.176312",
    },
    "now": 1743900595,
    "now_dt": "2025-04-06T00:49:55.525037Z",
}
