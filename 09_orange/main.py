import telebot
import settings

bot = telebot.TeleBot(settings.API_TOKEN)
anagrams_lst = list()
word = "Апельсинка"
# Анаграмма


@bot.message_handler(commands=["start"])
def start_game(message):
    bot.send_message(message.chat.id, f"Придумай анаграмму к слову {word}.")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    text = message.text
    if text in anagrams_lst:
        bot.reply_to(message, "Такое слово уже называли!")
    else:
        anagrams_lst.append(text)
        bot.reply_to(message, f"Спасибо. Запомню слово {text}.")


if __name__ == "__main__":
    bot.polling(none_stop=True)
