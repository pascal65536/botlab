import os
import logging
import telebot
from telebot import types
import settings
import gmap


bot = telebot.TeleBot(settings.API_TOKEN)
# Запрашивает у пользователя геометку, ведет лог и возвращает карту с метками


folder_name = "log"
if not os.path.exists(folder_name):
    os.mkdir(folder_name)

filename = os.path.join(folder_name, "geo.csv")
format_str = "%(asctime)s;%(levelname)s;%(message)s"
logging.basicConfig(filename=filename, level=logging.INFO, format=format_str)


@bot.message_handler(commands=["start", "help"])
def commands_start(message):
    user = message.from_user
    command = message.text
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    geo_button = types.KeyboardButton("Отправить местоположение", request_location=True)
    markup.add(geo_button)
    user = message.from_user
    msg = f"Привет! Я GEO-бот."
    if user.username:
        msg = f"Привет, {user.username}! Я GEO-бот."
    msg += "Я сохраняю твои геометки. Нажми кнопку ниже, чтобы отправить свое местоположение."
    bot.send_message(message.chat.id, msg, reply_markup=markup)


# Обработка геометок
@bot.message_handler(content_types=["location"])
def handle_location(message):
    user = message.from_user
    location = message.location
    msg = f"Спасибо за ваше местоположение! Вы находитесь на широте {location.latitude} и долготе {location.longitude}."
    bot.send_message(message.chat.id, msg)
    msg = f"{user.id};{user.username};{location.latitude};{location.longitude}"
    logging.info(msg)

    flnm = gmap.create_map_image(location.longitude, location.latitude, user.id)
    bot.send_photo(message.chat.id, open(flnm, "rb"))


# Обработка текстовых сообщений
@bot.message_handler(func=lambda message: True, content_types=["text"])
def echo_all(message):
    user_id = message.from_user.id
    username = message.from_user.username
    text = message.text
    bot.reply_to(message, text)


if __name__ == "__main__":
    bot.infinity_polling()
