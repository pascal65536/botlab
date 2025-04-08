import telebot
import settings
from telebot.types import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
)


bot = telebot.TeleBot(settings.API_TOKEN)
# Пример кнопок


@bot.message_handler(commands=["clear"])
def command_clear(message):
    msg = "Удалили клавиатуру"
    bot.send_message(message.chat.id, msg, reply_markup=ReplyKeyboardRemove())


@bot.message_handler(commands=["user"])
def command_user(message):
    msg = "Кнопки для пользователя"
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    for name in [
        "Как связаться со службой поддержки?",
        "Сколько стоит доставка?",
        "Как долго будет идти посылка?",
        "Как работает курьерская доставка?",
        "Когда приходят письма и сообщения о заказе?",
        "Можно ли оформить заказ по телефону?",
        "Какие документы мне нужны, чтобы получить заказ?",
    ]:
        reply_markup.add(KeyboardButton(text=name))
    bot.send_message(message.chat.id, msg, reply_markup=reply_markup)


@bot.message_handler(commands=["admin"])
def command_admin(message):
    msg = "Кнопки для администратора"
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    reply_markup.add("/add_category", "/delete_category", "/update_category")
    bot.send_message(message.chat.id, msg, reply_markup=reply_markup)


@bot.message_handler(commands=["start"])
def start(message):
    msg = "Доступные команды:"
    msg += "\n/clear - удаляет клавиатуру"
    msg += "\n/user - клавиатура для пользователя"
    msg += "\n/admin - клавиатура для администратора"
    bot.send_message(message.chat.id, msg, reply_markup=ReplyKeyboardRemove())


@bot.message_handler(func=lambda message: True)
def message(message):
    print(message.chat.id, message.text)
    bot.reply_to(message, f"Вы ввели {message.text}")


if __name__ == "__main__":
    bot.polling(none_stop=True)
