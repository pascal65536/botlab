import telebot
import settings
import random
from utils import scrabble_dict, calc_scores, helper, can_append


bot = telebot.TeleBot(settings.API_TOKEN)
commands_dct = dict()
# Анаграмма с подсчётом очков как в Scrabble. С функциями


with open("dict/russians1.txt", encoding="utf-8") as f:
    filestr = f.read().split()


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
    with open("dict/word_rus.txt", encoding="utf-8") as f:
        wordfilestr = f.read().split()
    word = random.choice(wordfilestr)
    username = message.from_user.username
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
