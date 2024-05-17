###########################################
# TELEBOT
###########################################
from flask import Flask # запускаем микросервис для работы бота в вебе
from flask import request # получаем json запросы
#from flask import jsonify # создаем json запросы
#from flask import Response # вернуть json из файла
#import simplejson as json # создаем json запросы

#бот
import telebot
from telebot import types########test_8541_bot

import time # делаем паузу

#import re # регулярные выражения

#import requests # создаем json запросы

import subprocess

#TOKENs
from tokens import TOKEN, DOMEN

global bot
bot = telebot.TeleBot(TOKEN, threaded=False)
bot.remove_webhook()
time.sleep(1)

# start the flask app
app = Flask(__name__)

task_list=["/start", "/vpn", "/Android",  "/iPhone",  "/Windows", "/help", "/contact"]

@bot.message_handler(commands=['start'])
def start_bot(message):
        bot.send_message(message.chat.id, "Привет *" + message.chat.first_name +"* . Хочешь, стабильный, бесплатный VPN, который не блокируется? Жми /vpn что бы получить список доступных команд жми /help")
        
        
@bot.message_handler(commands=['help'])
def help_bot(message):
    bot.send_message(message.chat.id, str(task_list))
      
  


@bot.message_handler(content_types=['text'])
def get_message(message):

 
    if message.text == "/vpn":
        bot.send_message(message.from_user.id, "1. Укажите email или номер телефона для регистрации на сервере VPN")
        bot.register_next_step_handler(message, get_vpn) #следующий шаг      
    
    elif message.text == "/Android":
    
        bot.send_message(message.chat.id, "ссылка для загрузки:")    
        time.sleep(1)  
        bot.send_message(message.chat.id, "https://play.google.com/store/apps/details?id=net.openvpn.openvpn")    
        time.sleep(1)    
        bot.send_message(message.from_user.id, "Установите файл конфигурации для вашего устройства по инструкции:")
        time.sleep(1)
        bot.send_message(message.from_user.id, "https://dzen.ru/a/ZUe4WPbf4kth0wIc?referrer_clid=1400&")
        
        
        
    
    elif message.text == "/iPhone":
    
        bot.send_message(message.chat.id, "ссылка для загрузки:")    
        time.sleep(1)  
        bot.send_message(message.chat.id, "https://apps.apple.com/us/app/openvpn-connect-openvpn-app/id590379981")    
        time.sleep(1)    
        bot.send_message(message.from_user.id, "Установите файл конфигурации для вашего устройства по инструкции:")
        time.sleep(1)
        bot.send_message(message.from_user.id, "https://dzen.ru/a/ZUfO9erRtjkmKRNm?referrer_clid=1400&")
    
    elif message.text == "/Windows":
    
        bot.send_message(message.chat.id, "ссылка для загрузки:")    
        time.sleep(1)  
        bot.send_message(message.chat.id, "https://apps.apple.com/us/app/openvpn-connect-openvpn-app/id590379981")    
        time.sleep(1)    
        bot.send_message(message.from_user.id, "Установите файл конфигурации для вашего устройства по инструкции:")
        time.sleep(1)
        bot.send_message(message.from_user.id, "https://dzen.ru/a/ZUfTNcb_FDZHF29C?referrer_clid=1400&")
        
    elif message.text == "/contact":
        bot.send_message(message.from_user.id, "Не работает VPN, возникли вопросы? Задайте их напрямую боту и ждите ответа администрации")
        bot.register_next_step_handler(message, get_contact)
        
        
    else:
        bot.send_message(message.from_user.id, "К сожалению моя нейронная сеть еще недостаточно развита, в ближайшее время я пройду курс по машинному обучению и стану полноценным ИИ. А пока используй /help.")
    #bot.reply_to(message, message.text) процитирует твой ответ

       
def get_vpn(message): 
        
    bot.send_message(message.from_user.id, "создаю файл конфигурции для %s" % message.text)
    
    config_name = str(message.text)
    
    subprocess.call(["./add_client.sh", config_name ], cwd = "/root/vpn/")
    
    bot.send_message(message.from_user.id, "2. Сохраните файл конфигурции на ваше устройство:")
    
    with open(r'/root/vpn/%s.ovpn' % config_name, 'rb') as config_vpn:
           out_msg  = bot.send_document(message.chat.id, config_vpn)
           
    time.sleep(3)
    
    bot.send_message(message.chat.id, "Выберите на какое устройство установить VPN /Android  /iPhone /Windows")
    bot.send_message(message.chat.id, "Пожалуйста выберите один из вариантов установки, если возникли трудности обратитесь в тех поддержку /contact")
    
    time.sleep(1)

    
 
  
    
def get_contact(message):
    bot.send_message(message.from_user.id, "Спасибо, ваше обращение << %s >> будет рассмотренно в ближайшее время" % message.chat.id)# message.text)

    bot.forward_message("2023848728", message.chat.id, message.id)

     

    
@app.route('/{}'.format(TOKEN), methods=["POST"])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    print("Message")
    return "ok", 200    
    
        
@app.route("/") # Говорим Flask, что за этот адрес отвечает эта функция
def hello_world():
 
    return "Hello!"

bot.infinity_polling()

app.run(host='0.0.0.0', port=80)
