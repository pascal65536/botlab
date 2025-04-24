import os
import telebot
import settings


bot = telebot.TeleBot(settings.API_TOKEN)
# Бот запрашивает у пользователя анкетные данные


status_dct = dict()
status_lst = ["first_name", "last_name", "username", "school", "age", "ok"]


# Вспомогательная функция
def send_welcome(user_id, status):
    if status == "ok":
        msg = f"Анкета заполнена. Спасибо!"
    else:
        msg = f"Заполните анкету. Введите `{status}`."
    bot.send_message(user_id, msg)


@bot.message_handler(commands=["start"])
def commands_start(message):
    from telebot.types import ReplyKeyboardRemove as rk_remove

    user = message.from_user
    user_id = str(user.id)

    msg = f"Привет, я эхо-бот. Не простой, а очень любопытный и очень больной!"
    bot.send_message(user_id, msg, reply_markup=rk_remove())

    status_dct.setdefault(user_id, status_lst[0])
    status_dct[user_id] = status_lst[0]
    send_welcome(user_id, status_dct[user_id])


# Обработка текстовых сообщений
@bot.message_handler(func=lambda message: True, content_types=["text"])
def echo_all(message):
    print(message.from_user.id, message.text)
    
    user_id = str(message.from_user.id)
    status_dct.setdefault(user_id, status_lst[0])
        
    if status_dct[user_id] == "ok":
        bot.reply_to(message, message.text)
    else:
        status_dct[user_id] = status_lst[status_lst.index(status_dct[user_id]) + 1]
        send_welcome(user_id, status_dct[user_id])


if __name__ == "__main__":
    bot.infinity_polling()
