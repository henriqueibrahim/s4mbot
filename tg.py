import certifi
import configparser
import os
import json
import logging
import pycurl
from io import BytesIO
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler

# Configuração
config = configparser.ConfigParser()
config.read("config.ini")

tgToken = config["telegram"]["token"]
weatherKey = config["hgweather"]["key"]

updater = Updater(token=tgToken, use_context=True)
dispatcher = updater.dispatcher

# Habilitando logs:
logging.basicConfig(filename='tg.log',
					format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
				   	level = logging.INFO)

def getData(url):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(pycurl.USERAGENT, 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Safari/537.36')
    c.setopt(c.CAINFO, certifi.where())
    c.perform()
    c.close()
    body = buffer.getvalue()
    return body

def start(update: Update, context: CallbackContext):
	output = "Olá! Eu sou a S4M"
	context.bot.send_message(chat_id=update.effective_chat.id, text=output)

def btc(update: Update, context: CallbackContext):
	url = "https://api.coincap.io/v2/assets/bitcoin"
	data = json.loads(getData(url))
	bitcoinPrice = data["data"]["priceUsd"]
	formatPrice = round(float(bitcoinPrice))
	output = f"O preço do Bitcoin é de ${formatPrice}"
	context.bot.send_message(chat_id=update.effective_chat.id, text=output)
	
def peopleinspace(update: Update, context: CallbackContext):
	url = "https://www.howmanypeopleareinspacerightnow.com/peopleinspace.json"
	data = json.loads(getData(url))
	numberPeople = data["number"]
	output = f"Tem {numberPeople} pessoas no espaço agora!"
	context.bot.send_message(chat_id=update.effective_chat.id, text=output)

def weather(update: Update, context: CallbackContext):
	url = f"https://api.hgbrasil.com/weather?key={weatherKey}&woeid=455821"
	data = json.loads(getData(url))
	output = f"{data['results']['city']} : Temp: {data['results']['temp']}C\n^_^"
	context.bot.send_message(chat_id=update.effective_chat.id, text=output)
	
# Para todo novo comando a ser acrescentado se deve adicionar ao handler.
# Handlers:
weather_handler = CommandHandler("weather", weather)
dispatcher.add_handler(weather_handler)

peopleinspace_handler = CommandHandler("peopleinspace", peopleinspace)
dispatcher.add_handler(peopleinspace_handler)

btc_handler = CommandHandler("btc", btc)
dispatcher.add_handler(btc_handler)
	
start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

# Iniciando o bot.
updater.start_polling()
