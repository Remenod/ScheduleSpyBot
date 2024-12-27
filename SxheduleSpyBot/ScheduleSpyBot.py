import telebot
from dotenv import load_dotenv
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

load_dotenv(dotenv_path=r'../Secrets/KEYS.env')
API = os.getenv("BOT_API")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SERVICE_ACCOUNT_FILE = r'../Secrets/schedulespybot-86b7d86a2ebb.json'

# Налаштування доступу до Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)

# Функція для отримання всіх аркушів
def get_sheets():
    spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    sheets = spreadsheet.get('sheets', [])
    sheet_titles = [sheet['properties']['title'] for sheet in sheets]
    return sheet_titles, sheets

# Функція для отримання даних з останнього аркуша
def get_data_from_last_sheet():
    sheet_titles, sheets = get_sheets()
    last_sheet = sheets[-1]
    last_sheet_name = last_sheet['properties']['title']
    print(f"Останній аркуш: {last_sheet_name}")
       
    range_name = f"{last_sheet_name}!F4:F102"
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
    values = result.get('values', [])

    return values

values = get_data_from_last_sheet()

if not values:
    print('Немає даних в діапазоні.')
else:    
    for row in values:
        print(row)

bot = telebot.TeleBot(API)

@bot.message_handler(commands=['start'])
def start(message):
    pass

# @bot.message_handler(func=lambda message: True)
# def send(message):
#     pass

# bot.polling(none_stop=True)
