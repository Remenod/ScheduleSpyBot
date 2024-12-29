import os
import subprocess
import requests
from dotenv import load_dotenv
from googleapiclient.discovery import build
from openpyxl import load_workbook, workbook
from google.oauth2.service_account import Credentials
from io import BytesIO
from enum import Enum


load_dotenv(dotenv_path=r'../Secrets/KEYS.env')
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SERVICE_ACCOUNT_FILE = r'../Secrets/schedulespybot-86b7d86a2ebb.json'

# Налаштування доступу до Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/drive.readonly']
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)   

class WeekDay(Enum):   
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

def LoadWorkbook():
    export_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=xlsx"
    headers = {"Authorization": f"Bearer {credentials.token}"}
    response = requests.get(export_url, headers=headers)
    if response.status_code == 200:        
        return load_workbook(BytesIO(response.content))         
    else:
        raise Exception(f"Не вдалося завантажити файл. Код помилки: {response.status_code}")
    
def GetSchedule(workbook_, sheetNum = -1,columNum = "F"):
    workbook = workbook_
    sheet = workbook.worksheets[sheetNum]
    output = f"{sheet.title}\n"
    row = 1
    while row <= sheet.max_row:
        cell = sheet[f"{columNum}{row}"]

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

def CompareSchedules(input1, input2):   
    exe_path = os.path.join("../comparer", "bin", "Debug", "net8.0", "comparer.exe")       
    try:
        run_result = subprocess.run(
        [exe_path, input1, input2], 
        capture_output=True, 
        text=True, 
        encoding="utf-8")
        if run_result.returncode != 0:
            print("Execution Error:", run_result.stderr.strip())
            return None        
        return run_result.stdout.strip()

    except FileNotFoundError:
        print("Error: Compiled executable not found.")
        return None