import os
import logging
import telebot
import settings
from telebot import types
from functools import wraps
from datetime import datetime
from behoof_local import save_json, load_json
from utils import generate_name


bot = telebot.TeleBot(settings.API_TOKEN)
# Запрашивает у пользователя геометку и сохраняет JSON в персональную папку


folder_name = "log"
if not os.path.exists(folder_name):
    os.mkdir(folder_name)

logging.basicConfig(
    filename=os.path.join(folder_name, "bot_actions.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# Декоратор для логирования
def log_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Логируем входные параметры
            msg = f"Calling function: {func.__name__} with args: {args[0].json} and kwargs: {kwargs}"
            logging.info(msg)
            result = func(*args, **kwargs)
            # Логируем выходное значение
            logging.info(f"Function {func.__name__} returned: {result}")
            return result
        except Exception as e:
            # Логируем исключения
            logging.error(f"Exception in function {func.__name__}: {e}", exc_info=True)
            raise

    return wrapper


@bot.message_handler(commands=["start", "help"])
@log_action
def commands_start(message):
    user = message.from_user
    command = message.text
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    geo_button = types.KeyboardButton("Отправить местоположение", request_location=True)
    markup.add(geo_button)
    name = generate_name(user.id)
    msg = f"Привет, {name}! Я GEO-бот. Я сохраняю твои геометки. Нажми кнопку ниже, чтобы отправить свое местоположение."
    bot.send_message(message.chat.id, msg, reply_markup=markup)
    entry = {
        "user_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "timestamp": datetime.now().isoformat(),
        "name": name,
    }
    data_json = load_json(["data", str(user.id)], "data.json")
    data_json.setdefault("info", list())
    data_json["info"].append(entry)
    save_json(["data", str(user.id)], "data.json", data_json)


# Обработка геометок
@bot.message_handler(content_types=["location"])
@log_action
def handle_location(message):
    user = message.from_user
    location = message.location
    entry = {
        "user_id": user.id,
        "username": user.username,
        "timestamp": datetime.now().isoformat(),
        "latitude": location.latitude,
        "longitude": location.longitude,
    }
    msg = f"Спасибо за ваше местоположение! Вы находитесь на широте {location.latitude} и долготе {location.longitude}."
    bot.send_message(message.chat.id, msg)
    data_json = load_json(["data", str(user.id)], "data.json")
    data_json.setdefault("map", list())
    data_json["map"].append(entry)
    save_json(["data", str(user.id)], "data.json", data_json)


# Обработка текстовых сообщений
@bot.message_handler(func=lambda message: True, content_types=["text"])
@log_action
def echo_all(message):
    user_id = message.from_user.id
    username = message.from_user.username
    text = message.text
    bot.reply_to(message, text)


if __name__ == "__main__":
    bot.infinity_polling()
