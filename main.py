import os
from urllib.request import Request
import json
import requests
from google.cloud import secretmanager
import openai
import telegram
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler, Dispatcher, ContextTypes, MessageHandler, filters


class Bot(telegram.Bot):
    ''' A class to represent a Telegram Bot which can get message update and send a crafted message respond'''

    def __init__(self, token: str, base_url: str = None, base_file_url: str = None, request: 'Request' = None, private_key: bytes = None, private_key_password: bytes = None, defaults: telegram.ext.Defaults = None):
        '''
        Constructs all the necessary attributes for the Bot object.

        Parameters
        ----------
            token: str
                token for telegram
        '''
        super().__init__(token, base_url, base_file_url, request,
                         private_key, private_key_password, defaults)
        self.dispatcher = Dispatcher(self, None)

    def start(self, update: Update,  context: CallbackContext):
        '''Takes in self, update and context, send a response with a random fact'''
        # Get some fun fact
        reqUrl = "https://uselessfacts.jsph.pl/random.json?language=en"
        headersList = {"Accept": "*/*"}
        response = requests.get(reqUrl, data="",
                                headers=headersList, timeout=5)
        response_json = json. loads(response.text)
        fun_fact = response_json['text']
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=f'Hi, I am Senpai bot!')
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=f'Before we start, wanna hear a fun fact?')
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=f'{fun_fact}')

    def echo(self, update: Update, context: CallbackContext):
        '''Take in self, update and context, send an echo response'''
        if not context.args:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="echo cho ho o!")
        else:
            echo_string = ' '.join(context.args)
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=f'{echo_string}')

    def unknown(self, update: Update, context: CallbackContext):
        '''takes in a message update and context, send a ChatGPT response'''
        if context.args:
            usr_msg = ' '.join(context.args)
            response = chat_gpt(usr_msg)
        else: 
            response = "I didn't understand what you were trying to say..."
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)


def chat_gpt(message):
    '''takes in a message update, return ChatGPT'''
    openai.api_key = get_token("OPENAI-API-KEY")
    response = openai.Completion.create(
        engine="davinci",
        prompt=message,
        temperature=0.5,
        max_tokens=1024,
        n=1,
        stop=None,
        timeout=10,
    )
    return response.choices[0].text.strip()

# Getting our TELEGRAM_TOKEN from the cloud
def get_token(secret_name: str) -> str:
    '''return the telegram token from google secret manager'''
    client = secretmanager.SecretManagerServiceClient()     # Create the Secret Manager client.
    # The secret_name should match the name of the secret you created in # the Secret Manager console
    secret_name = secret_name
    # Your GCP project id
    project_id = os.environ.get("PROJECT_ID")
    # Build the resource name of the secret version.
    request = {
        "name": f"projects/{project_id}/secrets/{secret_name}/versions/latest"}
    response = client.access_secret_version(request)
    # Access the secret version and return as string.
    return str(response.payload.data.decode("UTF-8"))


def telegram_bot(request):
    '''main function for telegram bot function'''
    TELEGRAM_TOKEN = get_token("TELEGRAM_TOKEN")
    bot = Bot(TELEGRAM_TOKEN)

    # Create all the bot handlers
    start_handler = CommandHandler('start', bot.start)
    echo_handler = CommandHandler('echo', bot.echo)
    unknown_handler = MessageHandler(~ filters.Filters.command, bot.unknown)

    # Add the bot handlers to dispatcher
    bot.dispatcher.add_handler(echo_handler)
    bot.dispatcher.add_handler(start_handler)
    bot.dispatcher.add_handler(unknown_handler)

    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        bot.dispatcher.process_update(update)

    return "okay"
