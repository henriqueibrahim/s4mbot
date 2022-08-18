import configparser
import os
import json
import logging
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

def start(update: Update, context: CallbackContext):
	output = "Olá! Eu sou a S4M"
	context.bot.send_message(chat_id=update.effective_chat.id, text=output)

def btc(update: Update, context: CallbackContext):
	os.system("curl -s --location --request GET 'api.coincap.io/v2/assets/bitcoin' > /tmp/bitcoin.json")
	with open ("/tmp/bitcoin.json") as f:
		data = json.load(f)
	price = data["data"]["priceUsd"]
	formatPrice = round(float(price))
	output = f"O preço do Bitcoin é de ${formatPrice}"
	context.bot.send_message(chat_id=update.effective_chat.id, text=output)
	
def peopleinspace(update: Update, context: CallbackContext):
	os.system("curl -s https://www.howmanypeopleareinspacerightnow.com/peopleinspace.json > /tmp/peopleinspace.json")
	with open("/tmp/peopleinspace.json") as f:
		data = json.load(f)
		npeople = data["number"]
	output = f"Tem {npeople} pessoas no espaço agora!"
	context.bot.send_message(chat_id=update.effective_chat.id, text=output)

def weather(update: Update, context: CallbackContext):
	req = f"https://api.hgbrasil.com/weather?key={weatherKey}&woeid=455821"
	os.system(f"curl -s '{req}' > /tmp/weather.json")
	with open("/tmp/weather.json") as f:
		data = json.load(f)
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