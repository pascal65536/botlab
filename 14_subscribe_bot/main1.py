import telebot
import settings

bot = telebot.TeleBot(settings.API_TOKEN)
bot.subscribe = dict()
subscribe_btns = ["history", "birthday", "custom", "horoscope", "tests"]
# Бот с кнопками - чекбоксами


@bot.callback_query_handler(func=lambda call: call.data.startswith("subscribe_"))
def subscribe_btn(call):
    message = call.message
    bot.subscribe.setdefault(message.chat.id, dict())
    user = bot.subscribe[message.chat.id]
    if call.data == "subscribe_history":
        user["history"] = not user.get("history")
    if call.data == "subscribe_birthday":
        user["birthday"] = not user.get("birthday")
    if call.data == "subscribe_custom":
        user["custom"] = not user.get("custom")
    if call.data == "subscribe_horoscope":
        user["horoscope"] = not user.get("horoscope")
    if call.data == "subscribe_tests":
        user["tests"] = not user.get("horoscope")
    send_menu(message)


@bot.callback_query_handler(func=lambda call: call.data.endswith("_all"))
def all_btn(call):
    message = call.message
    bot.subscribe.setdefault(
        message.chat.id, dict(zip(subscribe_btns, [False] * len(subscribe_btns)))
    )
    user = bot.subscribe[message.chat.id]
    if call.data == "select_all":
        for key in subscribe_btns:
            user[key] = True
    if call.data == "clear_all":
        for key in subscribe_btns:
            user[key] = False
    send_menu(message)


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    send_menu(message)


def send_menu(message):
    bot.subscribe.setdefault(message.chat.id, dict())
    user = bot.subscribe[message.chat.id]
    func = lambda x: "☑️" if user.get(x) else "🔲"
    reply_keyboard = telebot.types.InlineKeyboardMarkup()
    reply_keyboard.row(
        telebot.types.InlineKeyboardButton(
            text=f"{func('history')} Этот день в истории",
            callback_data="subscribe_history",
        ),
    )
    reply_keyboard.row(
        telebot.types.InlineKeyboardButton(
            text=f"{func('birthday')} Дни рождения", callback_data="subscribe_birthday"
        ),
    )
    reply_keyboard.row(
        telebot.types.InlineKeyboardButton(
            text=f"{func('custom')} Народные приметы", callback_data="subscribe_custom"
        ),
    )
    reply_keyboard.row(
        telebot.types.InlineKeyboardButton(
            text=f"{func('horoscope')} Гороскоп", callback_data="subscribe_horoscope"
        ),
    )
    reply_keyboard.row(
        telebot.types.InlineKeyboardButton(
            text=f"{func('tests')} Психологические тесты",
            callback_data="subscribe_tests",
        ),
    )
    reply_keyboard.row(
        telebot.types.InlineKeyboardButton(
            text="❌ Очистить всё", callback_data="clear_all"
        ),
        telebot.types.InlineKeyboardButton(
            text="✅ Выбрать всё", callback_data="select_all"
        ),
    )
    reply_keyboard.row(
        telebot.types.InlineKeyboardButton(
            text="🔝 Вернуться в главное меню", callback_data="main_menu"
        ),
    )
    resp = "Привет, выбери категорию, которую хочешь получать: "

    try:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text=resp,
            parse_mode="html",
            reply_markup=reply_keyboard,
        )
    except Exception as err:
        print(err)
        bot.send_message(
            chat_id=message.chat.id,
            text=resp,
            parse_mode="html",
            reply_markup=reply_keyboard,
        )


if __name__ == "__main__":
    bot.polling(none_stop=True)
