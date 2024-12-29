import enum
from dotenv import load_dotenv
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import requests
from io import BytesIO
from openpyxl import load_workbook, workbook

load_dotenv(dotenv_path=r'../Secrets/KEYS.env')
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SERVICE_ACCOUNT_FILE = r'../Secrets/schedulespybot-86b7d86a2ebb.json'

# Налаштування доступу до Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/drive.readonly']
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)   

class WeekDay(enum.Enum):   
    Понеділок = 0
    Вівторок  = 1
    Середа    = 2
    Четвер    = 3
    Пятниця   = 4
    Субота    = 5
    Неділя    = 6

def GetFirstNonEmptyLine(value):
    if isinstance(value, str):
        lines = value.split("\n")
        return next((line for line in lines if line.strip()), None)
    return value

def LoadSheet():
    export_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=xlsx"
    headers = {"Authorization": f"Bearer {credentials.token}"}
    response = requests.get(export_url, headers=headers)
    if response.status_code == 200:        
        return load_workbook(BytesIO(response.content))         
    else:
        raise Exception(f"Не вдалося завантажити файл. Код помилки: {response.status_code}")
    
def GetSchedule(sheet_ = -1,colum = "F"):       
    workbook = LoadSheet()
    sheet = workbook.worksheets[sheet_]
    output = f"{sheet.title}\n"
    row = 1
    while row <= sheet.max_row:
        cell = sheet[f"{colum}{row}"]

        if cell.coordinate in sheet.merged_cells:        
            for merged_range in sheet.merged_cells.ranges:
                if cell.coordinate in merged_range:
                    main_cell = sheet.cell(merged_range.min_row, merged_range.min_col)
                    main_value = GetFirstNonEmptyLine(main_cell.value)
                    if (row % 17 != 0 and row % 17 != 1) and main_value is not None:
                        output += f"{main_value}\n"
                    elif main_value is None:
                        output += f"нема\n"
                    break
        else:        
            cell_value = GetFirstNonEmptyLine(cell.value)
            if (row % 17 != 0 and row % 17 != 1) and cell_value is not None:
                output += f"{cell_value}\n"
            elif cell_value is None:
                output += f"нема\n"
        if row % 17 == 0:            
            row += 4
        elif row % 17 == 1:            
            row += 3
        else:
            row += 2
    return output
