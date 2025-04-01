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
category_lst = ["Школьник", "Студент", "Аспирант"]
# Пример кнопок


@bot.message_handler(commands=["help"])
def help(message):
    msg = "Вы вызвали help"
    bot.send_message(message.chat.id, msg, reply_markup=ReplyKeyboardRemove())


@bot.message_handler(commands=["start"])
def start(message):
    msg = "Вы вызвали start"
    location_btn = KeyboardButton(
        text="Отправить местоположение", request_location=True
    )
    contact_btn = KeyboardButton(text="Отправить контакт", request_contact=True)
    reply_markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_markup.add("/start", "/help", "/stop")
    reply_markup.add(*category_lst)
    reply_markup.add(location_btn, contact_btn)
    bot.send_message(message.chat.id, msg, reply_markup=reply_markup)


@bot.message_handler(func=lambda message: True)
def message(message):
    text = message.text
    if text in category_lst:
        keyboard = InlineKeyboardMarkup()
        for category in category_lst:
            keyboard.add(InlineKeyboardButton(category, callback_data=category))
        msg = f"Вы выбрали {text}"
        bot.send_message(message.chat.id, msg, reply_markup=keyboard)
    else:
        msg = f"Вы ввели {text}"
        bot.reply_to(message, msg)


@bot.callback_query_handler(func=lambda call: len(call.data) > 0)
def callback(call):
    if call.data in category_lst:
        msg = f"Вы выбрали {call.data}"
    else:
        msg = f"Вы нажали {call.data}"
    bot.send_message(call.message.chat.id, msg)


if __name__ == "__main__":
    bot.polling(none_stop=True)
