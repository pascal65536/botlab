import telebot
import settings
import logging
from cachetools import TTLCache
from functools import wraps


bot = telebot.TeleBot(settings.API_TOKEN)


# pip install cachetools
cache = TTLCache(maxsize=100, ttl=10)

LOG_FILE = "cache_decorator.log"
frmt = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=frmt)
logger = logging.getLogger(__name__)


def cache_decorator(func):
    @wraps(func)
    def wrapper(message):
        user_id = str(message.chat.id)
        if user_id in cache:
            return None
        else:
            result = func(message)
            cache[user_id] = result
            return result

    return wrapper


@bot.message_handler(func=lambda message: True)
@cache_decorator
def echo_message(message):
    text = message.text
    logging.info(text)
    bot.reply_to(message, text)


if __name__ == "__main__":
    bot.polling(none_stop=True)
