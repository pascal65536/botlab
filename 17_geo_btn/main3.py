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

user_dct = dict()


@bot.callback_query_handler(func=lambda callback: True)
def check_callback(callback):
    user_id = callback.from_user.id
    user_dct.setdefault(user_id, dict())
    spn = user_dct[user_id]["spn"]
    lon = float(user_dct[user_id]["lon"])
    lat = float(user_dct[user_id]["lat"])
    move_dct = {
        "left": (str(lon - spn), str(lat)),
        "right": (str(lon + spn), str(lat)),
        "up": (str(lon), str(lat + spn)),
        "down": (str(lon), str(lat - spn)),
    }
    bot.answer_callback_query(callback.id)
    key, value = callback.data.split("_")
    if key == "types":
        user_dct[user_id]["types"] = value
    elif key == "zoom":
        if value == "plus":
            user_dct[user_id]["spn"] = user_dct[user_id]["spn"] / 2
        elif value == "minus":
            user_dct[user_id]["spn"] = user_dct[user_id]["spn"] * 2
    elif key == "move":
        user_dct[user_id]["lon"] = move_dct[value][0]
        user_dct[user_id]["lat"] = move_dct[value][1]
    print(user_dct)
    send_map_with_buttons(user_id, user_dct)


def send_map_with_buttons(user_id, user_dct):
    from telebot.types import (
        InlineKeyboardMarkup,
        InlineKeyboardButton,
        KeyboardButton,
    )

    user_dct.setdefault(user_id, dict()).setdefault("types", "map")
    user_dct.setdefault(user_id, dict()).setdefault("spn", 0.01)
    user_dct.setdefault(user_id, dict()).setdefault("lat", "31.105141")
    user_dct.setdefault(user_id, dict()).setdefault("lon", "121.014223")
    types = user_dct[user_id]["types"]
    spn = user_dct[user_id]["spn"]
    lat = user_dct[user_id]["lat"]
    lon = user_dct[user_id]["lon"]

    flnm = gmap.create_map_image_buttons(
        user_id, lat=lat, lon=lon, types=types, spn=spn
    )
    map_lst = [
        ("🗺️", "types_map"),
        ("🌍", "types_sat"),
        ("🗺️🚦", "types_map,trf"),
        ("🌍🚦", "types_sat,trf"),
    ]
    zoom_lst = [
        ("➕", "zoom_plus"),
        ("🔽", "move_down"),
        ("➖", "zoom_minus"),
    ]
    axis_lst = [
        ("◀️", "move_left"),
        ("🔼", "move_up"),
        ("▶️", "move_right"),
    ]
    keyboard = InlineKeyboardMarkup(row_width=4)
    keyboard.add(
        *[InlineKeyboardButton(sign, callback_data=name) for sign, name in axis_lst]
    )
    keyboard.add(
        *[InlineKeyboardButton(sign, callback_data=name) for sign, name in zoom_lst]
    )
    keyboard.add(
        *[InlineKeyboardButton(sign, callback_data=name) for sign, name in map_lst]
    )
    bot.send_photo(user_id, open(flnm, "rb"), reply_markup=keyboard)


@bot.message_handler(commands=["get_map", "get_points"])
def commands_get(message):
    user = message.from_user
    types = message.text.strip("/")
    if types == "get_map":
        last_point = gmap.get_last_points(user.id, count=1)[0]
        user_dct.setdefault(user.id, dict()).setdefault("lat", last_point[-2])
        user_dct.setdefault(user.id, dict()).setdefault("lon", last_point[-1])
        send_map_with_buttons(user.id, user_dct)
    elif types == "get_points":
        last_points = gmap.get_last_points(user.id, count=10)
        points_lst = list()
        for point in last_points:
            points_lst.append(f"{point[0][:19]} {point[4]:>10}, {point[5]:>10}")
        msg = "\n".join(points_lst)
        bot.send_message(message.chat.id, msg)


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
    markup.add("/get_map", "/get_points")

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


# Обработка текстовых сообщений
@bot.message_handler(func=lambda message: True, content_types=["text"])
def echo_all(message):
    user_id = message.from_user.id
    username = message.from_user.username
    text = message.text
    bot.reply_to(message, text)


if __name__ == "__main__":
    bot.infinity_polling()
