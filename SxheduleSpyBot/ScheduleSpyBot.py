import telebot
from dotenv import load_dotenv
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import requests
from io import BytesIO
from openpyxl import load_workbook

load_dotenv(dotenv_path=r'../Secrets/KEYS.env')
TELEGRAM_BOT_API = os.getenv("BOT_API")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SERVICE_ACCOUNT_FILE = r'../Secrets/schedulespybot-86b7d86a2ebb.json'

# Налаштування доступу до Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/drive.readonly']
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)

def DownloadSheet():
    export_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=xlsx"
    headers = {"Authorization": f"Bearer {credentials.token}"}
    response = requests.get(export_url, headers=headers)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        raise Exception(f"Не вдалося завантажити файл. Код помилки: {response.status_code}")

try:
    workbook = load_workbook(DownloadSheet())    
    print("Файл успішно завантажено")
except Exception as e:
    print(f"Помилка: {e}")

sheet = workbook.worksheets[4]

for cell in sheet["F"]:
    print(cell.value)


# def ColumRangeFormater(column):
#     column_name = []
#     while column > 0:
#         column -= 1
#         column_name.append(chr(65 + column % 26))  # 65 = 'A'
#         column //= 26
#     column_name.reverse()
#     return f"{''.join(column_name)}"



bot = telebot.TeleBot(TELEGRAM_BOT_API)

@bot.message_handler(commands=['start'])
def start(message):
    pass

# @bot.message_handler(func=lambda message: True)
# def send(message):
#     pass

# bot.polling(none_stop=True)
