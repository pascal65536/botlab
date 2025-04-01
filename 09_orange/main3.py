import telebot
import settings


bot = telebot.TeleBot(settings.API_TOKEN)
anagrams_lst = list()
word = "Апельсинка"
# Анаграмма с памятью, русским словарём и помощником


with open("russian.txt", encoding="utf-8") as f:
    filestr = f.read().split()


def helper(word, russian):
    result = list()
    for line in russian:
        if len(line) < 3:
            continue
        if len(set(line.upper()) - set(word.upper())) == 0:
            f = True
            for ch in set(word.upper()):
                if not (line.upper().count(ch) <= word.upper().count(ch)):
                    f = False
                    break
            if f:
                result.append(line)
    return sorted(result, key=len, reverse=True)


def can_append(text, word, russian):
    """
    Однозначная функция
    Проверяет возможность добавления слова в список
    Добавлять будем в другом месте
    """        
    if russian and text.upper() not in russian:
        return False
    elif len(set(text.lower()) - set(word.lower())) != 0:
        return False
    for ch in set(text.lower()):
        if text.lower().count(ch) > word.lower().count(ch):
            return False
    return True


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
