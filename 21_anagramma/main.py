import telebot
import settings
import random
import utils
import datetime


bot = telebot.TeleBot(settings.API_TOKEN)
bot.game_dct = dict()


def get_rusword_lst(num):
    with open("dict/russian.txt", encoding="utf-8") as f:
        filestr = f.read().split()
    print(len(filestr))
    return filestr[:num]


@bot.message_handler(commands=["start"])
def start_game(message):
    if bot.game_dct.get("time"):
        last = str(datetime.datetime.now() - bot.game_dct["time"]).split(".")[0]
        if last <= "0:01:00":
            msg = "Нельзя закончить игру, потому что время последний ответ был дан более 1 минуты назад."
            word = bot.game_dct.get("word")
            if word:
                msg += f"\nЯ задал вам слово <b>{word}</b>."
            bot.send_message(message.chat.id, msg, parse_mode="html")
            return

    rusword_lst = get_rusword_lst(9)
    rusword = random.choice(rusword_lst)
    bot.game_dct["flow"] = dict()
    bot.game_dct["word"] = rusword
    bot.game_dct["time"] = datetime.datetime.now()
    msg = f"""Я задал вам слово <b>{rusword}</b>. Напишите мне как можно больше вариантов слов, составленных из букв этого слова.
        Чтобы начать новую игру - напиши /stop
        Нужны подробности - напиши /rules"""
    bot.send_message(message.chat.id, msg, parse_mode="html")


@bot.message_handler(commands=["stop"])
def stop_game(message):
    word = bot.game_dct.get("word")
    if not word:
        msg = "Игра не начата, напишите /start"
        bot.send_message(message.chat.id, msg, parse_mode="html")
        return
    msg_lst = list()
    msg_lst.append(f'Я задал слово "<b>{word}</b>".')
    last = str(datetime.datetime.now() - bot.game_dct["time"]).split(".")[0]
    msg_lst.append(f"Последний ход сделан <b>{last}</b>.")
    for k, v in bot.game_dct.get("flow").items():
        scores = utils.scores(bot.game_dct["flow"][message.chat.id])
        msg_lst.append(f"Игрок {k} набрал очков: {scores} и составил слов: {len(v)}.")
    msg_lst.append("Напишите /start, чтобы начать заново.")
    msg = "\n".join(msg_lst)
    bot.send_message(message.chat.id, msg, parse_mode="html")


@bot.message_handler(commands=["rules"])
def rules_game(message):
    word = bot.game_dct.get("word")
    msg = f"Я задаю вам слово."
    if word:
        msg = f"Я задал вам слово {word}."
    msg += "\nНадо составить другие слова из его букв. Чем больше, тем лучше."
    bot.send_message(message.chat.id, msg)


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.game_dct.setdefault("flow", dict()).setdefault(message.chat.id, set())
    word = bot.game_dct.get("word")
    reserved_lst = list()
    for k, v in bot.game_dct.get("flow").items():
        reserved_lst.extend(v)
    res = utils.can_append(message.text, word, reserved_lst)
    scores = 0
    if res:
        bot.game_dct["flow"][message.chat.id].add(message.text.lower())
        bot.game_dct["time"] = datetime.datetime.now()
        scores = utils.calc_scores(bot.game_dct["flow"][message.chat.id])
    msg = f"Вы сказали <b>{message.text}</b>. Задано <b>{word}</b>."
    if res:
        msg += f"\nВаше слово подходит"
    else:
        msg += f"\nВаше слово не подходит"
    msg += f"\nКоличество очков: <b>{scores}</b>"
    bot.send_message(message.chat.id, msg, parse_mode="html")
    print(bot.game_dct)


if __name__ == "__main__":
    bot.polling(none_stop=True)
