import os
import telebot
import settings


bot = telebot.TeleBot(settings.API_TOKEN)
# Бот запрашивает у пользователя анкетные данные


status_dct = dict()
status_lst = ["first_name", "last_name", "username", "school", "age", "ok"]
translation = {
    "first_name": "Фамилия",
    "last_name": "Имя",
    "username": "Ник",
    "age": "Возраст",
    "school": "Школа",
}


# Вспомогательная функция
def send_welcome(user_id, status):
    if status == "ok":
        msg = f"Анкета заполнена. Спасибо!"
    else:
        msg = f"Заполните анкету\n<b>{translation[status]}</b>:"
    bot.send_message(user_id, msg, parse_mode="html")


@bot.message_handler(commands=["start"])
def commands_start(message):
    from telebot.types import ReplyKeyboardRemove as rk_remove

    user = message.from_user
    user_id = str(user.id)

    msg = f"Привет, я эхо-бот. Не простой, а очень любопытный!"
    bot.send_message(user_id, msg, reply_markup=rk_remove())

    status_dct[user_id] = status_lst[0]
    send_welcome(user_id, status_dct[user_id])


# Обработка текстовых сообщений
@bot.message_handler(func=lambda message: True, content_types=["text"])
def echo_all(message):
    user_id = str(message.from_user.id)
    if status_dct[user_id] == "ok":
        bot.reply_to(message, message.text)
    else:
        status_dct[user_id] = status_lst[status_lst.index(status_dct[user_id]) + 1]
        send_welcome(user_id, status_dct[user_id])


if __name__ == "__main__":
    bot.infinity_polling()
