#########################################################
# TELEBOT
#########################################################
from flask import Flask
from flask import request

# создаем json запросы
from flask import json
from flask import jsonify  # создаем json запросы
from flask import Response  # вернуть json из файла
import requests

import time
import telebot
from telebot import types

#git update from webhooks
import git 


app = Flask(__name__)

# TOKENs
global TOKEN
TOKEN = ""
domen = ""

global bot
bot = telebot.TeleBot(TOKEN, threaded=False)
bot.remove_webhook()
time.sleep(1)

bot.set_webhook(url="https://%s.pythonanywhere.com/%s" % (domen, TOKEN))


task_list = ["/weather", "/news", "/bank", "/start", "/help", "/json_data"]


def get_weather(message):
    bot.send_message(
        message.from_user.id, "https://yandex.ru/search/?text=Погода_%s" % message.text
    )


def get_news(message):
    bot.send_message(
        message.from_user.id, "https://yandex.ru/search/?text=Новости_%s" % message.text
    )


def get_bank(message):
    bot.send_message(message.from_user.id, "https://yandex.ru/search/?text=курс_валют")


def post_json(message):
    bot.send_message(message.from_user.id, "post json:" + message.text)
    bot.send_message(
        message.from_user.id, "Делаю json запрос (не более 5 мин)..."
    )
    url = "http://" + domen + ".pythonanywhere.com/api/post_json/"

    params = {message.text: "my_json"}

    dump = json.dumps(params)

    headers = {"Content-type": "application/json", "Accept": "text/plain"}

    response = requests.post(url, data=dump, headers=headers)

    bot.send_message(
        message.from_user.id,
        "Готово, доступ к API через: http://"
        + domen
        + ".pythonanywhere.com/api/get_json/",
    )

    bot.register_next_step_handler("/start", start_bot)


@bot.message_handler(commands=["start"])
def start_bot(message):
    bot.send_message(
        message.chat.id,
        "Привет *"
        + message.chat.first_name
        + "* . Меня зовут Пятница, я здесь в роли ИИ. Чем я могу тебе помочь? /help список моих команд",
    )


@bot.message_handler(commands=["help"])
def help_bot(message):
    bot.send_message(message.chat.id, str(task_list))


@bot.message_handler(content_types=["text"])
def get_message(message):

    if message.text == "/json_data":
        bot.send_message(message.from_user.id, "Введите даные для передачи")
        bot.register_next_step_handler(message, post_json)

    elif message.text == "/weather":
        bot.send_message(message.from_user.id, "Укажите город...")
        bot.register_next_step_handler(message, get_weather)

    elif message.text == "/bank":
        bot.send_message(message.from_user.id, "Хотите узнать валютный курс?")
        bot.register_next_step_handler(message, get_bank)

    elif message.text == "/news":
        bot.send_message(
            message.from_user.id, "/_Политика? /_Эконономика? /_ИТ? Что интереусет?"
        )
        bot.register_next_step_handler(message, get_news)

    else:
        bot.send_message(
            message.from_user.id,
            "Используйте /start для списка команд",
        )
    # bot.reply_to(message, message.text) процитирует твой ответ


@app.route("/{}".format(TOKEN), methods=["POST"])
def webhook():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    print("Message")
    return "ok", 200


@app.route("/api/post_json/", methods=["GET", "POST"])
def POST_json():

    data = request.get_json()
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return jsonify(request.json)


@app.route("/api/get_json/", methods=["GET", "POST"])
def GET_json():

    with open("data.json", "r") as f:
        data = json.load(f)
    generator = (cell for row in data for cell in row)
    print(generator)
    return Response(
        generator,
        mimetype="application/json",
        headers={"Content-Disposition": "attachment;filename=data.json"},
    )


#git update
@app.route('/update_server', methods=['POST'])
    def webhook():
        if request.method == 'POST':
            repo = git.Repo('https://github.com/allex-b/bot_telegram')
            origin = repo.remotes.origin


            origin.pull()


            return 'Updated PythonAnywhere successfully', 200
        else:
            return 'Wrong event type', 400 
