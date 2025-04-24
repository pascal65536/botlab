import os
import csv
import telebot
import settings
import datetime
from behoof_local import save_json, load_json
from telebot.types import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
)


registered_users = load_json("data", "users.json")
no_kbd = telebot.types.ReplyKeyboardRemove()
bot = telebot.TeleBot(settings.API_TOKEN)
# Телеграм-бот для управления мероприятиями
# Пользователь уровня superuser может прислать (shedule.csv) csv файл в кодировке cp-1251 с расписанием 


level_dct = {
    "123": "user",
    "456": "teacher",
    "789": "staff",
    "000": "superuser",
    "yandex": "pdo",
}

reply_markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
reply_markup.add("/info", "/level", "/events")


@bot.message_handler(commands=["info"])
def info_command(message):
    user_id = str(message.chat.id)
    if user_id not in registered_users:
        msg = "Вы не зарегистрированы. Используйте /start для регистрации."
        bot.send_message(user_id, msg, reply_markup=no_kbd)
        return
    user = registered_users[user_id]
    msg = "Привет! Вы запросили информацию о себе."
    if user["first_name"]:
        msg += f"\nВаше имя: *{user['first_name']}*"
    if user["last_name"]:
        msg += f"\nВаша фамилия: *{user['last_name']}*"
    if user["username"]:
        msg += f"\nВаш ник: *{user['username']}*"
    if user["level"]:
        msg += f"\nВаш уровень: *{user['level']}*"
    bot.send_message(user_id, msg, reply_markup=reply_markup, parse_mode="Markdown")


@bot.message_handler(commands=["level"])
def level_command(message):
    user_id = str(message.chat.id)
    if user_id not in registered_users:
        msg = "Вы не зарегистрированы. Используйте /start для регистрации."
        bot.send_message(user_id, msg, reply_markup=no_kbd)
        return
    msg = "Привет! Вы запросили смену статуса. Введите код доступа:"
    bot.send_message(user_id, msg, reply_markup=reply_markup)
    registered_users[user_id]["is_change_level"] = True
    save_json("data", "users.json", registered_users)


@bot.message_handler(commands=["start"])
def start_command(message):
    user_id = str(message.chat.id)
    if user_id in registered_users:
        msg = "Вы уже зарегистрированы."
        bot.send_message(user_id, msg, reply_markup=reply_markup)
        return
    reg_btn = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    reg_btn.add(telebot.types.KeyboardButton("Зарегистрироваться"))
    msg = "Привет! Похоже, вы ещё не зарегистрированы. Нажмите кнопку 'Зарегистрироваться'"
    bot.send_message(user_id, msg, reply_markup=reg_btn)


@bot.message_handler(func=lambda message: message.text == "Зарегистрироваться")
def register_user(message):
    user_id = str(message.chat.id)
    registered_users[user_id] = {
        "first_name": message.from_user.first_name,
        "username": message.from_user.username,
        "last_name": message.from_user.last_name,
        "level": "user",
        "is_change_level": False,
    }
    msg = f"Вы успешно зарегистрированы! Теперь можете запрашивать расписание мероприятий."
    bot.send_message(user_id, msg, reply_markup=reply_markup, parse_mode="Markdown")
    msg = f"Ваш уровень доступа *{registered_users[user_id]['level']}*."
    msg += f"\nЧтобы изменить уровень доступа нажмите /level и введите код доступа."
    bot.send_message(user_id, msg, reply_markup=reply_markup, parse_mode="Markdown")
    save_json("data", "users.json", registered_users)


@bot.message_handler(commands=["events"])
def events_command(message):
    user_id = str(message.chat.id)
    if user_id not in registered_users:
        msg = "Вы не зарегистрированы. Используйте /start для регистрации."
        bot.send_message(user_id, msg, reply_markup=no_kbd)
        return

    events = load_json("data", "events.json")
    if not events:
        msg = "На данный момент нет никаких мероприятий."
        bot.send_message(user_id, msg, reply_markup=reply_markup)
        return
    events.sort(key=lambda x: (x["Дата начала"], x["Время начала"]))

    num = 1
    msg = ""
    level_command = registered_users[user_id]["level"]
    for event_dct in events:
        if level_command not in event_dct["Уровень доступа"]:
            continue
        date_start = event_dct["Дата начала"]
        date_now = datetime.datetime.now().strftime("%Y-%m-%d")
        if date_start < date_now:
            continue
        msg += f"\n*{num}. {event_dct['Название мероприятия']}*"
        msg += f"\n{event_dct['Описание']}"
        msg += f"\nДата проведения: {event_dct['Дата начала']} в {event_dct['Время начала'][:-3]}\n"
        num += 1
        if num > 10:
            break
    msg = f"*Список мероприятий для {level_command}:*\n{msg}"
    bot.send_message(user_id, msg, reply_markup=reply_markup, parse_mode="Markdown")


@bot.message_handler(content_types=["document"])
def handle_document(message):
    user_id = str(message.chat.id)
    if user_id not in registered_users:
        msg = "Вы не зарегистрированы. Используйте /start для регистрации."
        bot.send_message(user_id, msg, reply_markup=no_kbd)
        return

    if registered_users[user_id]["level"] != "superuser":
        msg = "Вы не имеете доступа к этому функционалу."
        bot.reply_to(message, msg, reply_markup=reply_markup)
        return

    file_info = bot.get_file(message.document.file_id)
    ext = file_info.file_path.split(".")[-1].lower()
    if ext not in ["csv"]:
        msg = "Неподходящий тип файла. Пожалуйста, отправьте CSV-файл."
        bot.reply_to(message, msg, reply_markup=reply_markup)
        return

    downloaded_file = bot.download_file(file_info.file_path)
    path_files = os.path.join("_cache")
    if not os.path.exists(path_files):
        os.makedirs(path_files)
    path_table = os.path.join(path_files, f"{user_id}.{ext}")
    with open(path_table, "wb") as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, f"Файл успешно получен!")

    events = list()
    with open(path_table, encoding="cp1251") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if not row:
                continue
            events.append(row)
    save_json("data", "events.json", events)
    bot.send_message(user_id, f"Файл успешно обработан!", reply_markup=reply_markup)

    if os.path.isfile(path_table):
        os.remove(path_table)


@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    user_id = str(message.chat.id)
    text = message.text
    if user_id not in registered_users:
        msg = "Вы не зарегистрированы. Используйте /start для регистрации."
        bot.send_message(user_id, msg, reply_markup=no_kbd)
        return
    is_change_level = registered_users[user_id]["is_change_level"]
    if is_change_level:
        text = text.replace(" ", "").lower()
        level = level_dct.get(text, "user")
        registered_users[user_id]["level"] = level
        msg = f"Ваш статус успешно изменен на *{level}*."
    else:
        msg = "Извините, я не понимаю эту команду."
        msg += "\nИспользуйте /start для начала или /events для просмотра мероприятий."
    bot.send_message(user_id, msg, reply_markup=reply_markup, parse_mode="Markdown")
    registered_users[user_id]["is_change_level"] = False
    save_json("data", "users.json", registered_users)


if __name__ == "__main__":
    bot.polling(none_stop=True)
