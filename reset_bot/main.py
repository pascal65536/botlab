import telebot
import settings
from telebot import types


bot = telebot.TeleBot(settings.API_TOKEN)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_all(message):
    user_id = message.from_user.id
    username = message.from_user.username
    text = message.text
    bot.reply_to(message, text, reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    bot.infinity_polling()
