import os
import logging
import telebot
import settings
import gmap


bot = telebot.TeleBot(settings.API_TOKEN)
# Добавляем кнопки


folder_name = "log"
if not os.path.exists(folder_name):
    os.mkdir(folder_name)

filename = os.path.join(folder_name, "geo.csv")
format_str = "%(asctime)s;%(levelname)s;%(message)s"
logging.basicConfig(filename=filename, level=logging.INFO, format=format_str)

user_types_dct = dict()


@bot.message_handler(commands=["map", "sat"])
def commands_types(message):
    user = message.from_user
    types = message.text.strip("/")
    _, lat, lon = gmap.get_last_point(user.id)
    lat = lat or "31.105141"
    lon = lon or "121.014223"
    user_types_dct.setdefault(user.id, "map")
    user_types_dct[user.id] = types
    local_types = user_types_dct[user.id]
    flnm = gmap.create_map_image_buttons(
        user.id, lat=lat, lon=lon, types=local_types, zoom=16
    )
    bot.send_photo(message.chat.id, open(flnm, "rb"))


@bot.message_handler(commands=["start"])
def commands_start(message):

    from telebot.types import (
        ReplyKeyboardMarkup,
        ReplyKeyboardRemove,
        KeyboardButton,
    )

    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    geo_button = KeyboardButton("Отправить местоположение", request_location=True)
    markup.add(geo_button)
    markup.add("/map", "/sat")

    user = message.from_user
    command = message.text
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

    lat = location.latitude
    lon = location.longitude
    local_types = user_types_dct.get(user.id, "map")
    flnm = gmap.create_map_image_buttons(
        user.id, lat=lat, lon=lon, types=local_types, zoom=16
    )
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
