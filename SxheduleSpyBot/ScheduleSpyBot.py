import telebot
from dotenv import load_dotenv
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

load_dotenv(dotenv_path=r'../Secrets/KEYS.env')
TELEGRAM_BOT_API = os.getenv("BOT_API")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SERVICE_ACCOUNT_FILE = r'../Secrets/schedulespybot-86b7d86a2ebb.json'

# Налаштування доступу до Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)

# Функція для отримання всіх аркушів
def GetSheets():
    spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    sheets = spreadsheet.get('sheets', [])
    sheet_titles = [sheet['properties']['title'] for sheet in sheets]
    return sheet_titles, sheets

# Функція для отримання даних з останнього аркуша
def GetDataFromLastSheet():
    sheet_titles, sheets = GetSheets()
    last_sheet = sheets[-1]
    last_sheet_name = last_sheet['properties']['title']
    print(f"Останній аркуш: {last_sheet_name}")
       
    range_name = f"{last_sheet_name}!E4:F102"
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
    values = result.get('values', [])
    return values


def GetRawMergedRanges():
    sheet_titles, sheets = GetSheets()
    last_sheet = sheets[2]
    last_sheet_id = last_sheet['properties']['sheetId']

    # Запит до Google Sheets API для отримання інформації про структуру аркуша
    spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    sheet_data = next(sheet for sheet in spreadsheet['sheets'] if sheet['properties']['sheetId'] == last_sheet_id)
    
    merged_ranges = sheet_data.get('merges', [])
    return merged_ranges


def GetParsedMergedRanges():
    result = []
    merged_ranges = GetRawMergedRanges()
    for merge in merged_ranges:
        start_row = merge['startRowIndex'] + 1
        end_row = merge['endRowIndex']
        start_col = merge['startColumnIndex'] + 1
        end_col = merge['endColumnIndex']

        start_cell = f"{ColumRangeFormater(start_col)}{start_row}"
        end_cell = f"{ColumRangeFormater(end_row)}{end_row}"
        result.append(f"{start_cell}:{end_cell}")
    return result

def ColumRangeFormater(column):    
    column_name = []
    while column > 0:
        column -= 1
        column_name.append(chr(65 + column % 26))  # 65 = 'A'
        column //= 26
    column_name.reverse()
    return f"{''.join(column_name)}"


xxx = GetParsedMergedRanges()
xxx.sort()
for i in xxx:
    print(i)

# merged_ranges = get_merged_ranges()
# merged_addresses = parse_merged_ranges(merged_ranges)

# print(merged_addresses)





# values = get_data_from_last_sheet()
# if not values:
#     print('Немає даних в діапазоні.')
# else:    
#     for row in values:
#         print(row)



bot = telebot.TeleBot(TELEGRAM_BOT_API)

@bot.message_handler(commands=['start'])
def start(message):
    pass

# @bot.message_handler(func=lambda message: True)
# def send(message):
#     pass

# bot.polling(none_stop=True)
