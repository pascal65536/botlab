import telebot
import settings


bot = telebot.TeleBot(settings.API_TOKEN)
anagrams_lst = list()
word = "Апельсинка"
# Анаграмма с памятью и русским словарём

with open("dict/russian.txt", encoding="utf-8") as f:
    filestr = f.read().split()


def append_anagrams(text):
    """
    Многозадачная функция:
    Проверяет наличие слова и добавляет его в список
    """
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
    text = message.text
    if text.upper() not in filestr:
        bot.reply_to(message, "Нет такого слова в русском языке!")
    elif text in anagrams_lst:
        bot.reply_to(message, "Такое слово уже называли!")
    elif len(set(text.lower()) - set(word.lower())) != 0:
        bot.reply_to(message, f"Таких букв нет в слове {word}!")
    else:
        anagrams_lst.append(text.lower())
        msg = f"Спасибо. Запомню слово {text}. Составлено слов: {len(anagrams_lst)}"
        bot.reply_to(message, msg)
    print(anagrams_lst)


if __name__ == "__main__":
    bot.polling(none_stop=True)
