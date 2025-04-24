import os
import telebot
from telebot import types
import settings


bot = telebot.TeleBot(settings.API_TOKEN)
user_dct = dict()
status_dct = dict()


translation = {
    "first_name": "Фамилия",
    "last_name": "Имя",
    "username": "Ник",
    "age": "Возраст",
    "school": "Школа",
}

check = "🔲✅"

default_dct = {
    "first_name": None,
    "last_name": None,
    "username": None,
    "age": None,
    "school": None,
}


def is_ready(user_id):
    if user_id not in user_dct:
        return False
    for value in user_dct[user_id].values():
        if not value:
            return False
    return True


@bot.callback_query_handler(func=lambda callback: True)
def check_callback(callback):
    user_id = str(callback.from_user.id)
    callback_data = callback.data
    status_dct[user_id] = callback_data
    msg = f"Ожидается ввод данных пользователя `{translation[callback_data]}`"
    bot.send_message(callback.message.chat.id, msg)


def send_anketa(user_id):
    markup = types.InlineKeyboardMarkup()
    for key, value in user_dct[str(user_id)].items():
        name = f"{check[bool(value)]} {translation[key]}"
        markup.add(types.InlineKeyboardButton(name, callback_data=key))
    msg = "Нужно заполнить анкету, чтобы пользоваться ботом"
    bot.send_message(user_id, msg, reply_markup=markup)


@bot.message_handler(commands=["start"])
def commands_start(message):
    from telebot.types import ReplyKeyboardRemove as rk_remove

    user = message.from_user
    user_dct[str(user.id)] = default_dct
    status_dct[str(user.id)] = None

    msg = f"Привет! Я Анкета-бот. Мне нужны твои <del>документы, одежда и мотоцикл</del> фамилия, имя и возраст."
    bot.send_message(message.chat.id, msg, reply_markup=rk_remove(), parse_mode="html")
    send_anketa(user.id)


# Обработка текстовых сообщений
@bot.message_handler(func=lambda message: True, content_types=["text"])
def echo_all(message):
    print(message.from_user.id, message.text)
    
    user_id = str(message.from_user.id)
    username = message.from_user.username
    text = message.text
    if is_ready(user_id):
        bot.reply_to(message, text)
        return

    if status_dct.get(str(user_id)) is None:
        send_anketa(user_id)    
        return

    human_status = translation[status_dct.get(str(user_id))]
    msg = f"Я хотел, чтобы ты написал мне `{human_status}`, а ты написал `{text}`"
    user_dct[user_id][status_dct[user_id]] = text
    status_dct[user_id] = None
    bot.send_message(user_id, msg)
    send_anketa(user_id)


if __name__ == "__main__":
    bot.infinity_polling()
