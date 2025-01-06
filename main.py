import os
from dotenv import load_dotenv

load_dotenv()

import telebot
from handlers import start_handler, filter_duration_handler, message_handler

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

bot.message_handler(commands=["start"])(start_handler)
bot.message_handler(commands=["filter_duration"])(filter_duration_handler)
bot.message_handler(func=lambda message: True)(message_handler)

if __name__ == "__main__":
    bot.polling(none_stop=True)
