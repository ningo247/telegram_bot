import os
from queue import Empty
from google.cloud import secretmanager
import requests, json, random
import telegram
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Updater
from telegram.ext import CommandHandler, Dispatcher, ContextTypes, MessageHandler, filters

# Create the Secret Manager client.
client = secretmanager.SecretManagerServiceClient()
# The secret_name should match the name of the secret you created in # the Secret Manager console
secret_name = "TELEGRAM_TOKEN"
# Your GCP project id
project_id = "telegram-bot-362319"
# Build the resource name of the secret version.
request = {"name": f"projects/{project_id}/secrets/{secret_name}/versions/latest"}
response = client.access_secret_version(request)
# Access the secret version.
TELEGRAM_TOKEN = response.payload.data.decode("UTF-8")


def start(update: Update, context: CallbackContext):
    # Get some fun fact
    reqUrl = "https://uselessfacts.jsph.pl/random.json?language=en"
    headersList = { "Accept": "*/*" }
    response = requests.request("GET", reqUrl, data="",  headers=headersList)
    response_json = json. loads(response.text)
    fun_fact = response_json['text']
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Hi, I am Senpai bot!')
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Before we start, wanna hear a fun fact?')
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'{fun_fact}')

def echo(update: Update, context: CallbackContext):
        if context.args:
            echo_string = ' '.join(context.args)
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'{echo_string}')
        else: context.bot.send_message(chat_id=update.effective_chat.id, text="echo cho ho o!")
        

def unknown(update: Update, context: ContextTypes):
    ADJECTIVES_LIST = ['want', 'need', 'prefer', 'looking for', 'should get', 'need you to give', 'think it\'s time for', 'love', 'in the mood for', 'was expecting']
    adjective = random.choice(ADJECTIVES_LIST)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Let\'s focus here! I really {adjective} a command, which starts with /')

def telegram_bot(request):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    # updater = Updater(token=os.environ["TELEGRAM_TOKEN"], use_context=True)
    dispatcher = Dispatcher(bot,None)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    echo_handler = CommandHandler('echo', echo)
    dispatcher.add_handler(echo_handler)

    unknown_handler = MessageHandler(~ filters.Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)
    
    
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
        
    return "okay"