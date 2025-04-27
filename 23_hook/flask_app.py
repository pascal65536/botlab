from flask import Flask, request
import json
import settings
from main import bot
from telebot import types
import logging


logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)


app = Flask(__name__)


@app.route(f"/bot/{settings.API_TOKEN.split(':')[0]}/", methods=["POST", "GET"])
def webhook():
    if request.method == "POST":
        text = request.get_data().decode("utf-8")
        request_body_dict = json.loads(text)
        logging.info("Request: %s", text)
        update = types.Update.de_json(request_body_dict)
        bot.process_new_updates([update])
    return {"statusCode": 200}


@app.route("/")
def hello_world():
    return "Hello from Flask!"


if __name__ == "__main__":
    app.run(debug=True)
