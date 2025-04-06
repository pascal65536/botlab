import telebot
import settings
import random
import behoof_local as behoof


bot = telebot.TeleBot(settings.API_TOKEN)
commands_dct = behoof.load_json("data", "commands.json")
# Бот с кнопками - исчезающими чекбоксами


@bot.message_handler(commands=["start"])
def start_game(message):
    username = message.from_user.username
    user_id = str(message.chat.id)

    msg = f"Привет, <b>{username}</b>. Напиши мне слова или фразы, которые нужно мониторить."
    bot.send_message(user_id, msg, parse_mode="html")
    commands_dct[user_id] = {"commands": [], "username": username, "message_id": None}
    behoof.save_json("data", "commands.json", commands_dct)


@bot.message_handler(func=lambda message: True)
def commands_message(message):
    # Ввод данных
    msg = message.text
    user_id = str(message.chat.id)
    commands_dct = behoof.load_json("data", "commands.json")
    user_dct = commands_dct[user_id]
    if user_dct["message_id"]:
        bot.delete_message(chat_id=user_id, message_id=user_dct["message_id"])
        user_dct["message_id"] = None

    # Обработка данных
    msg = msg.lower()
    msg = msg.replace("\n", "|")
    msg = msg.replace("\t", "|")
    msg = msg.replace(",", "|")
    msg = msg.replace(".", "|")
    msg = msg.replace("?", "|")
    msg = msg.replace("!", "|")
    msg = msg.replace("(", "|")
    msg = msg.replace(")", "|")
    msg = msg.replace(":", "|")
    for command in msg.split("|"):
        if not command:
            continue
        user_dct["commands"].append(command.strip())
    user_dct["commands"] = sorted(set(user_dct["commands"]))
    commands_dct[user_id] = user_dct
    behoof.save_json("data", "commands.json", commands_dct)
    # Вывод данных
    send_commands(user_id)


def send_commands(user_id, message_id=None):
    commands_dct = behoof.load_json("data", "commands.json")
    if len(commands_dct[user_id]["commands"]) == 0:
        msg = "Список команд пуст. Начните с начала /start"
        bot.send_message(user_id, msg)
        return

    msg = f"Список команд: <b>{', '.join(commands_dct[user_id]['commands'])}</b>"
    reply_keyboard = telebot.types.InlineKeyboardMarkup()
    for num, command in enumerate(commands_dct[user_id]["commands"]):
        reply_keyboard.row(
            telebot.types.InlineKeyboardButton(
                text=f"✅ {command}",
                callback_data=f"command_{num}",
            ),
        )
    res = bot.send_message(user_id, msg, parse_mode="html", reply_markup=reply_keyboard)
    commands_dct[user_id]["message_id"] = res.message_id
    behoof.save_json("data", "commands.json", commands_dct)


@bot.callback_query_handler(func=lambda call: call.data.startswith("command_"))
def get_command(call):
    user_id = str(call.from_user.id)
    command, num = call.data.split("_")
    commands_dct = behoof.load_json("data", "commands.json")
    user_dct = commands_dct[user_id]
    if user_dct["message_id"]:
        bot.delete_message(user_id, user_dct["message_id"])
        user_dct["message_id"] = None
    user_dct["commands"].pop(int(num))
    user_dct["commands"] = sorted(set(user_dct["commands"]))
    commands_dct[user_id] = user_dct
    behoof.save_json("data", "commands.json", commands_dct)
    send_commands(user_id)


if __name__ == "__main__":
    bot.polling(none_stop=True)
