import telebot
import settings
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
)


bot = telebot.TeleBot(settings.API_TOKEN)
# Пример кнопок


@bot.message_handler(commands=["start"])
def start(message):
    msg = "Вы вызвали start"
    location_btn = KeyboardButton(
        text="Отправить местоположение", request_location=True
    )
    contact_btn = KeyboardButton(text="Отправить контакт", request_contact=True)
    reply_markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_markup.add(location_btn, contact_btn)
    bot.send_message(message.chat.id, msg, reply_markup=reply_markup)


@bot.message_handler(func=lambda message: True)
def message(message):
    print(message.chat.id, message.text)
    bot.reply_to(message, f"Вы ввели {message.text}")


if __name__ == "__main__":
    bot.polling(none_stop=True)
