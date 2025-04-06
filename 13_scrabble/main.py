import telebot
import settings
import random


bot = telebot.TeleBot(settings.API_TOKEN)
commands_dct = dict()
# Анаграмма с подсчётом очков как в Scrabble


scrabble_dict = {
    "А": 1,
    "Б": 3,
    "В": 1,
    "Г": 3,
    "Д": 2,
    "Е": 1,
    "Ё": 3,
    "Ж": 5,
    "З": 5,
    "И": 1,
    "Й": 4,
    "К": 2,
    "Л": 2,
    "М": 2,
    "Н": 1,
    "О": 1,
    "П": 2,
    "Р": 1,
    "С": 1,
    "Т": 1,
    "У": 2,
    "Ф": 10,
    "Х": 5,
    "Ц": 5,
    "Ч": 5,
    "Ш": 8,
    "Щ": 10,
    "Ъ": 10,
    "Ы": 4,
    "Ь": 3,
    "Э": 8,
    "Ю": 8,
    "Я": 3,
}


def calc_scores(anagram_lst):
    result = 0
    for word in anagram_lst:
        for letter in word:
            result += scrabble_dict[letter.upper()]
    return result


with open("dict/russians1.txt", encoding="utf-8") as f:
    filestr = f.read().split()


def get_word():
    with open("dict/word_rus.txt", encoding="utf-8") as f:
        filestr = f.read().split()
    return random.choice(filestr)


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


def can_append(text, word, russian=None):
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
    user_dct = commands_dct.get(message.chat.id)
    if not user_dct:
        bot.send_message(message.chat.id, "Игра не начата! Нажмите /start")
        return

    word = user_dct["word"]
    anagram_lst = user_dct["anagrams_lst"]
    helper_lst = helper(word, filestr)
    scores = calc_scores(anagram_lst)
    msg_lst = [
        f"Вам было задано слово: {word}",
        f"Вы назвали слов: {len(anagram_lst)}.",
        f"Можно назвать слов: {len(helper_lst)}.",
        f"Вы набрали очков: {scores}.",
    ]
    msg = "\n".join(msg_lst)
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=["start"])
def start_game(message):
    username = message.from_user.username
    word = get_word()
    user_dct = {"word": word, "anagrams_lst": list()}
    msg = f"Привет, {username}. Придумай анаграмму к слову <b>{word}</b>."
    bot.send_message(message.chat.id, msg, parse_mode="html")
    commands_dct[message.chat.id] = user_dct


@bot.message_handler(func=lambda message: True)
def anagrama_message(message):
    # Ввод данных
    text = message.text
    user_dct = commands_dct.get(message.chat.id)
    if not user_dct:
        bot.send_message(message.chat.id, "Игра не начата! Нажмите /start")
        return
    word = user_dct["word"]
    anagrams_lst = user_dct["anagrams_lst"]

    # Обработка данных
    if not can_append(text, word, filestr):
        msg = "Такое слово нельзя использовать!"
    elif text in anagrams_lst:
        msg = f"Это слово уже использовали."
    else:
        anagrams_lst.append(text)
        commands_dct[message.chat.id] = user_dct
        msg = f"Спасибо. Запомню слово {text}."

    # Вывод данных
    bot.reply_to(message, msg)


if __name__ == "__main__":
    bot.polling(none_stop=True)
