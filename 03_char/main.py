import telebot
import settings
from behoof_local import save_json, load_json


bot = telebot.TeleBot(settings.API_TOKEN)
# Игра виселица


@bot.message_handler(commands=["start"])
def start_game(message):
    bot.send_message(
        message.chat.id,
        "Привет! Чтобы начать игру, загадай слово с помощью команды /guess <слово>.",
    )


@bot.message_handler(commands=["guess"])
def guess_word(message):
    if message.chat.id != settings.root:
        bot.send_message(message.chat.id, "Вы не можете загадывать слово.")
        return

    word = message.text.split()[1].lower()
    games = {
        "word": word,
        "guessed_letters": [],
        "current_state": "_" * len(word),
    }
    save_json("data", "games.json", games)

    bot.send_message(
        message.chat.id, f"Слово загадано! Давайте отгадывать. Введите буквы."
    )


@bot.message_handler(commands=["status"])
def status_game(message):
    games = load_json("data", "games.json")
    print(f"{games=}")
    word = set(games.get("word", ""))
    guessed_letters = set(games.get("guessed_letters", ""))
    bot.send_message(
        message.chat.id,
        f"Загадано слово из {len(word)} букв. Осталось отгадать {word - guessed_letters} букв. Введите буквы.",
    )


@bot.message_handler(func=lambda message: True)
def guess_letter(message):
    mci_str = str(message.chat.id)
    games = load_json("data", "games.json")
    letter = message.text.lower()
    if letter in games["guessed_letters"]:
        bot.send_message(mci_str, "Эта буква уже была отгадана.")
        return

    games["guessed_letters"].append(letter)
    games.setdefault(mci_str, dict()).setdefault("letters", list())
    games[mci_str]["letters"].append(letter)
    games.setdefault(mci_str, dict()).setdefault("score", 0)
    if letter in games["word"]:
        games[mci_str]["score"] += 1
        bot.send_message(mci_str, f"Поздравляем! Буква '{letter}' есть в слове.")
    else:
        bot.send_message(mci_str, f"К сожалению, буквы '{letter}' нет в слове.")

    current_state = "".join(
        [c if c in games["guessed_letters"] else "_" for c in games["word"]]
    )
    bot.send_message(mci_str, f"Текущее состояние слова: {current_state}")
    score = games.get(mci_str, dict()).get("score", 0)
    bot.send_message(mci_str, f"Ваши очки: {score}")
    letters = games.get(mci_str, dict()).get("letters", list())
    bot.send_message(mci_str, f"Ваши буквы: {letters}")
    games["current_state"] = current_state
    save_json("data", "games.json", games)


if __name__ == "__main__":
    bot.polling(none_stop=True)
