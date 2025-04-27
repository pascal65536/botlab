import telebot
import settings

bot = telebot.TeleBot(settings.API_TOKEN, threaded=False)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я эхо-бот. Напиши мне что-нибудь.")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    resp = message.text
    bot.reply_to(message, resp)


if __name__ == "__main__":
    bot.polling(none_stop=True)
