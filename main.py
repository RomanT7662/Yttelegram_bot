# Import necessary modules
import os  # For accessing environment variables
from dotenv import load_dotenv  # For loading environment variables from a .env file

# Load environment variables from the .env file
load_dotenv()

# Import the Telegram bot library and custom handler functions
import telebot  # For interacting with the Telegram Bot API
from handlers import start_handler, filter_duration_handler, message_handler  # Custom handlers for commands and messages

# Retrieve the Telegram bot token from environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)  # Initialize the bot with the token

# Define bot commands and associate them with their respective handler functions
bot.message_handler(commands=["start"])(start_handler)  # Handle the /start command
bot.message_handler(commands=["filter_duration"])(filter_duration_handler)  # Handle the /filter_duration command
bot.message_handler(func=lambda message: True)(message_handler)  # Handle any other text messages

# Start the bot and keep it running
if __name__ == "__main__":
    bot.polling(none_stop=True)  # Enable continuous polling to listen for user input
