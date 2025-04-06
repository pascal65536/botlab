import telebot
import settings
from utils import can_append, helper

# Избавились от функций, убрав их в utils.py


bot = telebot.TeleBot(settings.API_TOKEN)
anagrams_lst = list()
word = "Апельсинка"
# Анаграмма с памятью, русским словарём и помощником


with open("dict/russian.txt", encoding="utf-8") as f:
    filestr = f.read().split()


@bot.message_handler(commands=["help"])
def help_game(message):
    msg = f"Слова, которые можно составить из слова {word}: "
    msg += ", ".join(helper(word, filestr))
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=["start"])
def start_game(message):
    bot.send_message(message.chat.id, f"Придумай анаграмму к слову {word}.")


@bot.message_handler(func=lambda message: True)
def anagrama_message(message):
    """
    Выделяем три основных блока программы
    """
    # Ввод данных
    text = message.text
    # Обработка данных
    if not can_append(text, word, filestr):
        msg = "Такое слово нельзя использовать!"
    elif text in anagrams_lst:
        msg = f"Это слово уже использовали."
    else:
        anagrams_lst.append(text)
        msg = f"Спасибо. Запомню слово {text}."
    # Вывод данных
    print(len(anagrams_lst))
    bot.reply_to(message, msg)


if __name__ == "__main__":
    bot.polling(none_stop=True)
