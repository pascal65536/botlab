import telebot
import settings
from telebot import TeleBot, types


bot = telebot.TeleBot(settings.API_TOKEN)
# Пример инлайновых кнопок


@bot.message_handler(commands=["start"])
def send_keyboard(message):
    markup = types.InlineKeyboardMarkup(row_width=8)
    row_one = [
        types.InlineKeyboardButton("1", callback_data="btn1"),
        types.InlineKeyboardButton("2", callback_data="btn2"),
        types.InlineKeyboardButton("3", callback_data="btn3"),
        types.InlineKeyboardButton("4", callback_data="btn4"),
        types.InlineKeyboardButton("5", callback_data="btn5"),
        types.InlineKeyboardButton("6", callback_data="btn6"),
        types.InlineKeyboardButton("7", callback_data="btn7"),
        types.InlineKeyboardButton("8", callback_data="btn8"),
    ]
    markup.add(*row_one)

    row_two = [
        types.InlineKeyboardButton("Rutube", url="https://rutube.ru"),
        types.InlineKeyboardButton("Yandex", url="https://yandex.ru"),
        types.InlineKeyboardButton("VK", url="https://vk.com"),
    ]
    markup.add(*row_two)

    row_three = [
        types.InlineKeyboardButton("Half button 1", callback_data="half_1"),
        types.InlineKeyboardButton("Half button 2", callback_data="half_2"),
    ]
    markup.add(*row_three)

    row_four = [
        types.InlineKeyboardButton("Wery long button", callback_data="btnF"),
    ]
    markup.add(*row_four)
    bot.send_message(message.chat.id, "Выберите кнопку:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("btn"))
def callback(call):
    msg = f"Вы выбрали {call.data}"
    bot.send_message(call.message.chat.id, msg)


@bot.callback_query_handler(func=lambda call: call.data.startswith("half_"))
def callback(call):
    msg = f"Вы нажали {call.data}"
    bot.send_message(call.message.chat.id, msg)


if __name__ == "__main__":
    bot.polling(none_stop=True)
