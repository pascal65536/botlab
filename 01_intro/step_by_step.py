import requests
import settings


token = settings.API_TOKEN
key = "getMe"
url = f"https://api.telegram.org/bot{token}/{key}"
response = requests.get(url, timeout=30)
print(response.status_code)
print(response.json())


token = settings.API_TOKEN
key = "getUpdates"
url = f"https://api.telegram.org/bot{token}/{key}"
response = requests.get(url, timeout=30)
print(response.json())


token = settings.API_TOKEN
key = "sendMessage"
text = "Привет, как дела"
text = text.replace(" ", "+")
url = f"https://api.telegram.org/bot{token}/{key}"
params = {"chat_id": 1234567890, "text": text}
response = requests.post(url, params=params, timeout=30)
print(response.json())
