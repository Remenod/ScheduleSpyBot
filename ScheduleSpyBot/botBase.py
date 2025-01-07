import os
import telebot
from dotenv import load_dotenv

load_dotenv(dotenv_path=r'../Secrets/KEYS.env')
TELEGRAM_BOT_API = os.getenv("BOT_API")
LOG_CLIENT_API = os.getenv("LOG_CLIENT_API")
bot       = telebot.TeleBot(TELEGRAM_BOT_API)
logClient = telebot.TeleBot(LOG_CLIENT_API)