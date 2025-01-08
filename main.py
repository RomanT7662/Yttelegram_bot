import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

import telebot

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

from handlers import start_handler, filter_duration_handler, message_handler

bot.message_handler(commands=["start"])(start_handler)
bot.message_handler(commands=["filter_duration"])(filter_duration_handler)
bot.message_handler(func=lambda message: True)(message_handler)

if __name__ == "__main__":
    bot.polling(none_stop=True)
