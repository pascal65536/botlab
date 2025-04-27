import settings
import requests


def setwebhook(token, url):
    telegram_url = f"https://api.telegram.org/bot{token}/setWebhook"
    params = {"url": url}
    print(requests.get(telegram_url, json=params).json())


def deletewebhook(token):
    telegram_url = f"https://api.telegram.org/bot{token}/deleteWebhook"
    print(requests.get(telegram_url).json())


def getwebhookinfo(token):
    telegram_url = f"https://api.telegram.org/bot{token}/getWebhookInfo"
    print(requests.get(telegram_url).json())


if __name__ == "__main__":
    my_url = "https://botfatherkrsk.pythonanywhere.com"
    ret = getwebhookinfo(settings.API_TOKEN)
    print(ret)
    ret = deletewebhook(settings.API_TOKEN)
    print(ret)
    url = f"{my_url}/bot/{settings.API_TOKEN.split(':')[0]}/"
    ret = setwebhook(settings.API_TOKEN, url)
    print(url)
