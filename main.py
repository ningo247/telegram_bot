import os
from google.cloud import secretmanager
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
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=context.args[0])

def unknown(update: Update, context: ContextTypes):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def telegram_bot(request):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    # updater = Updater(token=os.environ["TELEGRAM_TOKEN"], use_context=True)
    dispatcher = Dispatcher(bot,None)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    echo_handler = CommandHandler('echo', echo)
    dispatcher.add_handler(echo_handler)

    unknown_handler = MessageHandler(filters.Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)
    
    
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
        
    return "okay"