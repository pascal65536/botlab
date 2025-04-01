import telebot
import settings


bot = telebot.TeleBot(settings.API_TOKEN)
commands_dct = dict()
# Сохраняем сказанное. Слово - не воробей


@bot.message_handler(commands=["help"])
def help_game(message):
    msg = ", ".join(commands_dct[message.chat.id])
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=["start"])
def start_game(message):
    username = message.from_user.username
    commands_dct[message.chat.id] = list()
    bot.send_message(
        message.chat.id,
        f"Привет {username}. Я буду запоминать все, что ты мне напишешь, а по команде /help я покажу тебе всё, что я запомнил.",
    )


@bot.message_handler(func=lambda message: True)
def commands_message(message):
    text = message.text
    commands_dct[message.chat.id].append(text)
    msg = f"Длина списка: {len(commands_dct[message.chat.id])}"
    bot.reply_to(message, msg)
    print(commands_dct)


if __name__ == "__main__":
    bot.polling(none_stop=True)
