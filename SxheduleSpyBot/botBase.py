import telebot
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=r'../Secrets/KEYS.env')
TELEGRAM_BOT_API = os.getenv("BOT_API")
bot = telebot.TeleBot(TELEGRAM_BOT_API)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Є єдина команда /print {номер тижня}\nНаприклад /print 4 - виведе розклад за 4 тиждень. Поки все")