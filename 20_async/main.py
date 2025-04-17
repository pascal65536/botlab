import aiohttp
import asyncio
import settings


# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
TOKEN = settings.API_TOKEN
CHAT_ID = (
    settings.root
)  # Замените на ID чата или пользователя, куда вы хотите отправить сообщения


async def send_message(session, message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    async with session.post(url, json=payload) as response:
        if response.status == 200:
            print(f"Message sent: {message}")
        else:
            print(f"Failed to send message: {response.status}")


async def main():
    messages = [
        "Hello, this is message 1!",
        "This is message 2!",
        "And here's message 3!",
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [send_message(session, msg) for msg in messages]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
