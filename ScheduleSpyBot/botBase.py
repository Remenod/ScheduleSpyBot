import telebot
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=r'../Secrets/KEYS.env')
TELEGRAM_BOT_API = os.getenv("BOT_API")
bot = telebot.TeleBot(TELEGRAM_BOT_API)