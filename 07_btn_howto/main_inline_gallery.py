import telebot
import settings
from telebot import TeleBot, types


bot = telebot.TeleBot(settings.API_TOKEN)
# Пример инлайновых кнопок


gallery_dct = {"left": "◀️", "right": "▶️"}

pic_lst = [
    "AgACAgIAAxkBAAIsdGf0BHvOprok-pyghx1_br5OaPvnAALt8DEbIp6gS2S5LOz7eWyiAQADAgADeAADNgQ",
    "AgACAgIAAxkBAAIsfWf0BuiSgUcFyUeioe6Gz19konZSAAIG8TEbIp6gS4Ad4CHbK8yOAQADAgADeAADNgQ",
    "AgACAgIAAxkBAAIsf2f0CFAERTZnMVrDgY7bgUqxeDmaAAIP8TEbIp6gS84e43Q_Fu0UAQADAgADeAADNgQ",
    "AgACAgIAAxkBAAIsg2f0CGxrEgEf1ox-wu_G5Y9-Cn4KAAIT8TEbIp6gS4G-h0uLoF2vAQADAgADeAADNgQ",
    "AgACAgIAAxkBAAIshWf0CHdox_PsSPm7S0dUP7wHnaLzAAIV8TEbIp6gS8n0nAGzCmB2AQADAgADeAADNgQ",
    "AgACAgIAAxkBAAIsgWf0CF_StKMd2aAncepUqAS-z6NIAAIQ8TEbIp6gS8OdQk-cqFqXAQADAgADeAADNgQ",
]

maxlen = len(pic_lst) - 1


prw = lambda current: len(pic_lst) - 1 if current == 0 else current - 1
nxt = lambda current: 0 if current == len(pic_lst) - 1 else current + 1


@bot.message_handler(commands=["start"])
def send_keyboard(message):
    current = 0
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("◀️", callback_data=f"{prw(current)}"),
        types.InlineKeyboardButton("▶️", callback_data=f"{nxt(current)}"),
    )
    bot.send_photo(message.chat.id, pic_lst[0], reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    current = int(call.data)
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("◀️", callback_data=f"{prw(current)}"),
        types.InlineKeyboardButton("▶️", callback_data=f"{nxt(current)}"),
    )
    bot.edit_message_media(
        media=types.InputMediaPhoto(media=pic_lst[current]),
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
    )


@bot.message_handler(content_types=["photo"])
def photo(message):
    fileID = message.photo[-1].file_id
    bot.send_message(message.chat.id, f"Фото сохранено: {fileID}")


if __name__ == "__main__":
    bot.polling(none_stop=True)
