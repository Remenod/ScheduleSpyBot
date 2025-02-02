import os
import telebot
from dotenv import load_dotenv
from testModeVariable import TEST_MODE

current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '..', 'Secrets', 'KEYS.env')
load_dotenv(env_path)

if not TEST_MODE:
    TELEGRAM_BOT_API = os.getenv("BOT_API")
else:
    TELEGRAM_BOT_API = os.getenv("BOT_API_TEST")

LOG_CLIENT_API = os.getenv("LOG_CLIENT_API")
bot       = telebot.TeleBot(TELEGRAM_BOT_API)
logClient = telebot.TeleBot(LOG_CLIENT_API)