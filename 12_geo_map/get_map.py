import requests
from io import BytesIO


lon = 92.864053  # Долгота
lat = 56.023728  # Широта
zoom = 16  # Масштаб карты

map_params = {
    "ll": f"{lon},{lat}",
    "z": f"{zoom}",
    "l": "map",
    "size": "600,450",
    "pt": "92.864,56.023,flag~92.865,56.024,pm2rdl18",
}

url = "https://static-maps.yandex.ru/1.x/"

response = requests.get(url, params=map_params, timeout=10)
print(response.url)


if response.status_code == 200:
    response.raise_for_status()
    with open("map.png", "wb") as f:
        f.write(BytesIO(response.content).getbuffer())
    print("Картинка сохранена как map.png")

else:
    print("Ошибка:", response.content)
