import os
import logging
import telebot
import settings


bot = telebot.TeleBot(settings.API_TOKEN)
# Бот требует у пользователя геометку


folder_name = "log"
if not os.path.exists(folder_name):
    os.mkdir(folder_name)

filename = os.path.join(folder_name, "geo.csv")
format_str = "%(asctime)s;%(levelname)s;%(message)s"
logging.basicConfig(filename=filename, level=logging.INFO, format=format_str)

status_dct = dict()


# Вспомогательная функция для отправки приветствия
def send_welcome(user_id):
    from telebot.types import ReplyKeyboardRemove as rk_remove

    msg = f"Привет! Вы можете пользоваться ботом, если отправите местоположение."
    bot.send_message(user_id, msg, reply_markup=rk_remove())


@bot.message_handler(commands=["start"])
def commands_start(message):
    user = message.from_user
    user_id = str(user.id)
    status_dct[user_id] = "location"
    send_welcome(user_id)


# Обработка геометок
@bot.message_handler(content_types=["location"])
def handle_location(message):
    user = message.from_user
    user_id = str(user.id)
    lat = message.location.latitude
    lon = message.location.longitude
    msg = f"Спасибо за ваше местоположение! Вы находитесь на широте {lat} и долготе {lon}."
    bot.send_message(user_id, msg)
    logging.info(f"{user.id};{user.username};{lat};{lon}")
    status_dct[user_id] = "ok"


# Обработка текстовых сообщений
@bot.message_handler(func=lambda message: True, content_types=["text"])
def echo_all(message):
    print(message.from_user.id, message.text)
    
    user_id = str(message.from_user.id)
    if status_dct[user_id] == "ok":
        bot.reply_to(message, message.text)
    else:
        send_welcome(user_id)


if __name__ == "__main__":
    bot.infinity_polling()
