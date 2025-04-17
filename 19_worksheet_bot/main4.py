import os
import json
import telebot
import settings
from telebot import types


bot = telebot.TeleBot(settings.API_TOKEN)
# Бот запрашивает у пользователя анкетные данные

user_dct = dict()
status_dct = dict()
status_lst = ["first_name", "last_name", "username", "school", "age"]
translation = {
    "first_name": "Фамилия",
    "last_name": "Имя",
    "username": "Ник",
    "age": "Возраст",
    "school": "Школа",
}
check = "🔲✅"


def save_json(save_dct):
    file = os.path.join("data", "user.json")
    with open(file, "w", encoding="utf-8") as file:
        json.dump(save_dct, file, ensure_ascii=False, indent=2)


def load_json():
    file = os.path.join("data", "user.json")
    with open(file, encoding="utf-8") as file:
        user_dct = json.load(file)
    return user_dct


# Вспомогательная функция
def send_welcome(user_id):
    user_dct = load_json()
    is_ready = True
    markup = types.InlineKeyboardMarkup()
    for status in status_lst:
        button = check[int(bool(user_dct[user_id].get(status)))]
        name = f"{button} {translation[status]}"
        markup.add(types.InlineKeyboardButton(name, callback_data=status))
        if user_dct[user_id].get(status) is None:
            is_ready = False
    if is_ready:
        msg = f"Анкета заполнена. Спасибо!"
        status_dct[user_id] = "ok"
    else:
        msg = f"Заполните анкету"
    bot.send_message(user_id, msg, reply_markup=markup)


@bot.message_handler(commands=["start"])
def commands_start(message):
    from telebot.types import ReplyKeyboardRemove as rk_remove

    user = message.from_user
    user_id = str(user.id)
    user_dct.setdefault(user_id, dict())
    save_json(user_dct)
    msg = f"Привет, я эхо-бот. Не простой, а очень любопытный!"
    bot.send_message(user_id, msg, reply_markup=rk_remove())
    send_welcome(user_id)


# Обработка текстовых сообщений
@bot.message_handler(func=lambda message: True, content_types=["text"])
def echo_all(message):
    user_id = str(message.from_user.id)
    if status_dct.get(user_id) == "ok":
        bot.reply_to(message, message.text)
    else:
        user_dct.setdefault(user_id, dict()).setdefault(status_dct[user_id], None)
        user_dct[user_id][status_dct[user_id]] = message.text
        save_json(user_dct)
        send_welcome(user_id)


@bot.callback_query_handler(func=lambda callback: True)
def check_callback(callback):
    user_id = str(callback.from_user.id)
    callback_data = callback.data
    status_dct[user_id] = callback_data
    msg = f"Введите `{translation[callback_data]}`"
    bot.send_message(callback.message.chat.id, msg)


if __name__ == "__main__":
    bot.infinity_polling()
