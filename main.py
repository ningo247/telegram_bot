from logging.config import listen
import os
import telegram
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Updater
from telegram.ext import CommandHandler, Dispatcher, ContextTypes, MessageHandler, filters



def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=context.args[0])

def unknown(update: Update, context: ContextTypes):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def telegram_bot(request):
    bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])
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
        #chat_id = update.message.chat.id
        # Reply with the same message
        #bot.sendMessage(chat_id=chat_id, text=update.message.text)
        # updater.start_webhook(listen='127.0.0.1', port='80', url_path='https://us-central1-telegram-bot-362319.cloudfunctions.net/telegram_bot')
    return "okay"