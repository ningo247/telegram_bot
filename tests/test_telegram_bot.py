import json
import os
import unittest.mock as mock
from unittest.mock import MagicMock
import telegram
import pytest
from main import Bot
from main import get_token
from dotenv import load_dotenv

load_dotenv()
# # test get_token() function
# def test_get_token():
#     token = get_token("OPENAI-API-KEY")
#     assert token is not None

@pytest.fixture
def return_telegram_token():
    # token = os.getenv("telegram_token")
    token = "fake-token"
    return token

class TestBot:

    @mock.patch('requests.get')
    def test_start(self, mock_get, return_telegram_token):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = json.loads({"text": "Some fun fact"})
        mock_get.return_value = mock_response

        telegram_token = return_telegram_token
        bot = Bot(telegram_token)
        update = telegram.Update(1, message=telegram.Message(1, "/start", telegram.Chat(1,telegram.constants.CHAT_PRIVATE)))
        context = MagicMock(args=[])
        bot.start(update, context)

        context.bot.send_message.assert_called_with(
            chat_id=1, text='Hi, I am Senpai bot!'
        )
        context.bot.send_message.assert_called_with(
            chat_id=1, text='Before we start, wanna hear a fun fact?'
        )
        context.bot.send_message.assert_called_with(
            chat_id=1, text='Some fun fact'
        )

    def test_echo(self):
        token = get_token("TELEGRAM_TOKEN")
        bot = Bot(token)
        update = telegram.Update(1, message=telegram.Message(1, "/echo hello world", telegram.Chat(1,telegram.constants.CHAT_PRIVATE)))
        context = MagicMock(args=['hello', 'world'])
        # context.__iter__.return_value = ['hello ', 'world']
        # context.bot.send_message.assert_called_with(chat_id=0, text="TEST MESSAGE")
        bot.echo(update, context)
        context.bot.send_message.assert_called_with(
            chat_id=1, text='hello world'
        )

    # @mock.patch('bot.openai.Completion.create')
    # def test_unknown(self, mock_gpt):
    #     mock_choice = mock.Mock(items = [])
    #     mock_choice.text = "I'm sorry, I don't understand. Can you please provide me with a valid command?"
    #     mock_gpt.return_value.choices = [mock_choice]

    #     bot = Bot("telegram_token")
    #     update = telegram.Update(1, message=telegram.Message(1, "invalid_command"))
    #     context = mock.Mock()
    #     bot.unknown(update, context)
    #     context.bot.send_message.assert_called_with(
    #         chat_id=1, text="I'm sorry, I don't understand. Can you please provide me with a valid command?"
    #     )
