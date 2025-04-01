import telebot
import settings


bot = telebot.TeleBot(settings.API_TOKEN)
anagrams_lst = list()
word = "Апельсинка"
# Анаграмма с памятью


def append_anagrams(text):
    if text in anagrams_lst:
        return False
    else:
        anagrams_lst.append(text)
        return True


@bot.message_handler(commands=["start"])
def start_game(message):
    bot.send_message(message.chat.id, f"Придумай анаграмму к слову {word}.")


@bot.message_handler(func=lambda message: True)
def anagrama_message(message):
    # Ввод данных
    text = message.text
    # Обработка данных
    if not append_anagrams(text):
        msg = "Такое слово уже называли!"
    else:
        msg = f"Спасибо. Запомню слово {text}."
    # Вывод данных
    bot.reply_to(message, msg)


if __name__ == "__main__":
    bot.polling(none_stop=True)
