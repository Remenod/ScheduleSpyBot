import openpyxl
import requests
import subprocess
import databaseManager

from io import BytesIO
from botEnv import COMPARER_DLL_PATH, PARSER_DLL_PATH, SPREADSHEET_ID, SERVICE_ACCOUNT_FILE
from logger import log
from botBase import bot
from enumerations import Group, AdminPanel
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request


# Налаштування доступу до Google Sheets API
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive.readonly',
]
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)


def get_sheet_gids() -> list:
    log('Loading gids...')
    try:
        sheet_metadata = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        sheet_gids = []

        for sheet in sheet_metadata['sheets']:
            sheet_gids.append(sheet['properties']['sheetId'])

        return sheet_gids

    except Exception as e:
        print(f'Виникла помилка: {e}')
        return []

    finally:
        log('Gids loaded.')


gids = get_sheet_gids()


def get_right_lines(value: str) -> str:
    if value is None:
        return None

    lines = str(value).split('\n')
    subjectLine = next((line for line in lines if line.strip()), None)
    auditoriumLine = next(
        (
            line
            for line in lines
            if line.strip().startswith('а.') or line.strip().startswith('Наукова бібліотека')
        ),
        None,
    )

    if subjectLine is None:
        return 'помилка обробки розкладу'

    if auditoriumLine is None:
        return f'{subjectLine}'

    return f'{subjectLine} $[]{auditoriumLine}'


def load_workbook() -> openpyxl.workbook.workbook.Workbook:
    export_url = f'https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=xlsx'
    headers = {'Authorization': f'Bearer {credentials.token}'}

    response = requests.get(export_url, headers=headers)

    if response.status_code == 200:
        return openpyxl.load_workbook(BytesIO(response.content))

    text = f'Не вдалося завантажити файл. Код помилки: {response.status_code}'
    log(text)


def get_schedule(sheet_, column_num: Group, raw_output: bool = False) -> str:
    sheet = sheet_
    output = f'{sheet.title}\n'
    row = 1
    while row <= sheet.max_row:
        cell = sheet[f'{column_num.value}{row}']

        if cell.coordinate in sheet.merged_cells:
            for merged_range in sheet.merged_cells.ranges:
                if cell.coordinate in merged_range:
                    main_cell = sheet.cell(merged_range.min_row, merged_range.min_col)
                    main_value = None
                    if not raw_output:
                        main_value = get_right_lines(main_cell.value)
                    else:
                        main_value = main_cell.value

                    if (row % 17 != 0 and row % 17 != 1) and main_value is not None:
                        output += f'{main_value}\n'
                    elif main_value is None:
                        output += 'Пара відсутня\n'
                    break
        else:
            cell_value = None
            if not raw_output:
                cell_value = get_right_lines(cell.value)
            else:
                cell_value = cell.value
            if (row % 17 != 0 and row % 17 != 1) and cell_value is not None:
                output += f'{cell_value}\n'
            elif cell_value is None:
                output += 'Пара відсутня\n'
        if row % 17 == 0:
            row += 4
        elif row % 17 == 1:
            row += 3
        else:
            row += 2
    return output


def compare_schedules(input1: str, input2: str) -> str:
    try:
        run_result = subprocess.run(
            ['dotnet', COMPARER_DLL_PATH, input1, input2],
            capture_output=True,
            text=True,
            encoding='utf-8',
        )
        if run_result.returncode != 0:
            log(f'Execution Error:{run_result.stderr.strip()}')
            return None
        return run_result.stdout.strip()
    except FileNotFoundError:
        log('Error: Compiled executable not found.')
        raise Exception('Error: Compiled executable not found.')


def parse_comparer_output(inp: str) -> str:
    try:
        run_result = subprocess.run(
            ['dotnet', PARSER_DLL_PATH, inp], capture_output=True, text=True, encoding='utf-8'
        )
        if run_result.returncode != 0:
            log(f'Execution Error:{run_result.stderr.strip()}')
            return None
        return run_result.stdout.strip()
    except FileNotFoundError:
        log('Error: Compiled executable not found.')
        raise Exception('Error: Compiled executable not found.')


weekNums = databaseManager.get_all_sheets_numbers()


def compare_all_groups():
    log('Запускаю перевірку...')
    log('Завантажую таблицю з Google API...')

    workbook = load_workbook()
    weekNums = databaseManager.get_all_sheets_numbers()

    if len(weekNums) == 0:
        log('Помилка. Не вдалося отримати записані тижні з бази даних')
        return None

    actualWeekNum = int(weekNums[0])
    lastWeekNum = int(workbook.worksheets[-1].title.split('т')[0])
    lastSavedWeekNum = int(weekNums[-1])
    sameAsOldWeekIndex = 1

    log('Перевіряю наявність нового тижня...')

    if lastWeekNum != lastSavedWeekNum:
        try:
            currWeekNum = lastWeekNum
            while currWeekNum != actualWeekNum:
                sameAsOldWeekIndex += 1
                currWeekNum = int(workbook.worksheets[-sameAsOldWeekIndex].title.split('т')[0])

        except IndexError:
            log('Error: No old week found')
            return None

        finally:
            try:
                global gids
                res = bot.ensure_send_messages(
                    databaseManager.get_all_user_ids(),
                    "В розкладі з'явився новий тиждень.\n Для перегляду можете скористатися командою /schedule",
                )

                if res != {}:
                    log(f'Помилки при повідомленні наявності нового тижня користувачам: \n{res}')

                log("В розкладі з'явились нові тижні")
                gids = get_sheet_gids()
                temp = sameAsOldWeekIndex

                while (actualWeekNum + temp - 1) != actualWeekNum:
                    for group in Group:
                        currSchedule = get_schedule(
                            workbook.worksheets[actualWeekNum + temp - 2], group
                        )
                        databaseManager.write_schedule(
                            actualWeekNum + temp - 1, group, f'{currSchedule}'
                        )

                    temp -= 1

            except Exception as e:
                log(e)
    else:
        log('нових тижнів не знайдено')
        sameAsOldWeekIndex = lastSavedWeekNum - actualWeekNum + 1

    log('Перевіряю зміни в кожній групі...')

    for group in Group:
        newSchedule = get_schedule(workbook.worksheets[-sameAsOldWeekIndex], group)
        oldSchedule = databaseManager.get_old_schedule(actualWeekNum, group)
        comparerOut = compare_schedules(oldSchedule, newSchedule)

        if comparerOut != 'без змін':
            log(f'ВИЯВЛЕНІ ЗМІНИ В РОЗКЛАДІ ГРУПИ {group.name}')

            allCurrGroupUsers = databaseManager.get_users_by_group(group)
            allCurrGroupUsers.append(AdminPanel.groupId.value)

            if allCurrGroupUsers is not None or len(allCurrGroupUsers) != 0:
                res1 = bot.ensure_send_messages(
                    allCurrGroupUsers,
                    f'*В розкладі виявлені зміни:*\n{parse_comparer_output(comparerOut)}',
                    'Markdown',
                )
                bot.ensure_send_messages(
                    allCurrGroupUsers, 'Для перегляду можете скористатися командою /schedule'
                )

                log(f'Помилки при надсиланні змін користувачам: \n{res1}')

        databaseManager.write_schedule(actualWeekNum, group, newSchedule)

    log('Готово')
