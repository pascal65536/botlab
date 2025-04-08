import telebot
import settings
from telebot import TeleBot, types


bot = telebot.TeleBot(settings.API_TOKEN)
# Пример инлайновых кнопок


monkeys_dct = {
    "speak-no-evil-monkey": "🙊",
    "hear-no-evil-monkey": "🙉",
    "see-no-evil-monkey": "🙈",
}


markup = types.InlineKeyboardMarkup()
markup.add(
    *[types.InlineKeyboardButton(z[1], callback_data=z[0]) for z in monkeys_dct.items()]
)


@bot.message_handler(commands=["start"])
def send_keyboard(message):
    msg = f"Нажмите кнопку:"
    bot.send_message(message.chat.id, msg, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.endswith("-monkey"))
def callback(call):
    msg = f"Вы нажали {monkeys_dct[call.data]}"
    bot.edit_message_text(
        text=msg,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
    )


if __name__ == "__main__":
    bot.polling(none_stop=True)
