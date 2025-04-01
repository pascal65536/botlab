import telebot
import settings
import random


bot = telebot.TeleBot(settings.API_TOKEN)
bot.game_dct = dict()
# Как поймать льва в Африке


@bot.message_handler(commands=["start"])
def start_game(message):
    bot.game_dct.setdefault(message.chat.id, dict())
    bot.game_dct[message.chat.id]["leo"] = random.randint(0, 100)
    bot.game_dct[message.chat.id]["count"] = 0
    bot.game_dct[message.chat.id]["result"] = False
    msg = """Я загадал чило от 0 до 100. Угадай его.\n
Пиши числа, а я буду говорить больше или меньше, направляя тебя. Цель - найти число за меньшее число ходов. Неправильные ответы будут игнорироваться, но счетчик шагов неумолим.\n
Чтобы выйти из игры, напиши /stop
Нужны подробности - напиши /rules"""
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=["stop"])
def stop_game(message):
    user = bot.game_dct.get(message.chat.id)
    if not user:
        bot.send_message(message.chat.id, "Игра не запущена.")
        return
    count = bot.game_dct[message.chat.id]["count"]
    result = bot.game_dct[message.chat.id]["result"]
    result = "" if result else "не"
    leo = bot.game_dct[message.chat.id]["leo"]
    msg = f"Вы сделали {count} шагов и {result} угадали число {leo}.\nНапишите /start, чтобы начать заново."
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=["rules"])
def rules_game(message):
    msg = "Я загадал число от 0 до 100. Угадай его."
    bot.send_message(message.chat.id, msg)


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    user = bot.game_dct.get(message.chat.id)
    if not user:
        bot.send_message(message.chat.id, "Игра не запущена.")
        return
    leo = user["leo"]
    if not user["result"]:
        user["count"] += 1
        if not message.text.isdigit():
            msg = f"Нужно ввести именно число, но спасибо за попытку."
        elif int(message.text) > leo:
            msg = f"Вы говорите {message.text}, у меня <b>меньше</b>."
        elif int(message.text) < leo:
            msg = f"Вы говорите {message.text}, у меня <b>больше</b>."
        elif int(message.text) == leo:
            msg = f"Угадал! Вы говорите {message.text}, у меня <b>столько же</b>!"
            user["result"] = True
        bot.send_message(message.chat.id, msg, parse_mode="html")

    if user["result"]:
        msg = f"Игра закончена. Вы угадали число {leo} за {user['count']} ходов.\nНапишите /start, чтобы начать новую игру."
        bot.send_message(message.chat.id, msg)


if __name__ == "__main__":
    bot.polling(none_stop=True)
