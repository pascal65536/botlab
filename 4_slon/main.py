import telebot
import settings

bot = telebot.TeleBot(settings.API_TOKEN)
# Купи слона


@bot.message_handler(commands=["start"])
def start_game(message):
    bot.send_message(message.chat.id, "Купи слона.")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    resp = f"Все говорят «{message.text}», а ты купи слона!"
    bot.reply_to(message, resp)


if __name__ == "__main__":
    bot.polling(none_stop=True)
