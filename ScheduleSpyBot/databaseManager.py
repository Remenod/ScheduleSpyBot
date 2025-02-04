import os
from urllib import response
import requests
from logger import log
from typing import Union
from dotenv import load_dotenv
from enumerations import Group
from testModeVariable import TEST_MODE


current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '..', 'Secrets', 'KEYS.env')

load_dotenv(env_path)

if not TEST_MODE:
    PHP_API_URL        = os.getenv('PHP_API_URL')
    USER_IDS_URL       = os.getenv('USER_IDS_URL')
    OLD_SCHEDULE_URL   = os.getenv('OLD_SCHEDULE_URL')
    ALL_BY_USERS_URL   = os.getenv('ALL_BY_USERS_URL')
    SAVE_SCHEDULE_URL  = os.getenv('SAVE_SCHEDULE_URL')
    GET_SHEET_NAME_URL = os.getenv('GET_SHEET_NAME')
    DELETE_SHEET_URL   = os.getenv('DELETE_SHEET')
    BLOCK_USERS_URL    = os.getenv('BLOCK_USERS_URL')
    GET_BLOCKED_URL    = os.getenv('GET_BLOCKED_USERS_URL')

else:
    PHP_API_URL        = os.getenv('PHP_API_URL_T')
    USER_IDS_URL       = os.getenv('USER_IDS_URL_T')
    OLD_SCHEDULE_URL   = os.getenv('OLD_SCHEDULE_URL_T')
    ALL_BY_USERS_URL   = os.getenv('ALL_BY_USERS_URL_T')
    SAVE_SCHEDULE_URL  = os.getenv('SAVE_SCHEDULE_URL_T')
    GET_SHEET_NAME_URL = os.getenv('GET_SHEET_NAME_T')
    DELETE_SHEET_URL   = os.getenv('DELETE_SHEET_T')
    BLOCK_USERS_URL    = os.getenv('BLOCK_USERS_T')
    GET_BLOCKED_URL    = os.getenv('GET_BLOCKED_USERS_T')


#Schedule management

def GetOldSchedule(sheet_number:int, subgroup:Group) -> str:
    data = {
        "action":"get_schedule",
        "subgroup_name": subgroup.name,
        "sheet_number": sheet_number
    }
    try:
        response = requests.post(OLD_SCHEDULE_URL,data=data)
        response.raise_for_status()
        result = response.json()
        if response.status_code == 200:       
            return result["schedule"]
        else:
            error_message = result.get("error","Невідома помилка")
            log(f"Помилка:{error_message}")
            return None
    except requests.exceptions.RequestException as e:
        log(f"Помилка запиту до PHP: {e}")
        return None

def WriteSchedule(sheet_number:int,subgroup:Group,schedule_data:str):
    data = {
        "action": "save_schedule",
        "sheet_number":sheet_number,
        "subgroup": subgroup.name,
        "schedule_data": schedule_data
    }
    try:
        response = requests.post(SAVE_SCHEDULE_URL,data=data)
        if response.status_code == 200:
            pass
        else:
            log(f"Write Schedule Error:{response.text}")            
    except Exception as e:
        log(f"Write Schedule Request failed:{e}")        

def GetAllSheetsNumbers() -> list:
    try:
        response = requests.get(GET_SHEET_NAME_URL)
        if response.status_code == 200:
            return response.json()
        else:
             log(f"Помилка запиту: статус {response.status_code}")
             return []
    except requests.exceptions.RequestException as e:
        log(f"Помилка підключення до сервер: {e}")
        return []

def DeleteSheet(sheet_number:int):
    data = {
        'action':'delete_sheet',
        'sheet_number':sheet_number
    }
    try:
        response = requests.post(DELETE_SHEET_URL,data=data)
        if response.status_code == 200:
            pass
        else:
            log(f"Помилка запиту: статус {response.status_code}")
    except Exception as e:
        log(f"Помилка видалиння тижня: {e}")        


#User management

def GetUserByUsername(username:str) -> dict:    
    if username.startswith('@'):
        username = username.replace('@', '', 1)
    userIds = GetAllUserIds()
    for userId in userIds:
        user = GetUserInfo(userId)
        if user['username'] == username:
            user['chat_id'] = userId
            return user
    log(f"Користувача з ім'ям @{username} не знайдено.")
    return {}

def SaveUser(chat_id: Union[int, str], full_name:str, username:str):
    if username is None:
        username = "None"
    try:
        response = requests.post(PHP_API_URL, data={
            'action': 'save_user',
            'chat_id': chat_id,
            'full_name': full_name,
            'username': username
        })
        response_data = response.json()
        if response.status_code == 200 and response_data.get('success'):
            log(f"Користувач {full_name} успішно збережений або оновлений через PHP API.")
        else:
            log(f"Помилка збереження користувача {full_name}:", response_data.get('error'))
    except Exception as e:
        log(f"Помилка збереження користувача через PHP API: {e}")

def UpdateUserGroup(chat_id: Union[int, str], group_name):
    try:
        response = requests.post(PHP_API_URL, data={
            'action': 'update_group',
            'chat_id': chat_id,
            'group_name': group_name
        })
        response_data = response.json()
        if response.status_code == 200 and response_data.get('success'):
            log(f"Групу користувача {chat_id} успішно оновлено через PHP API.")
        else:
            log("Помилка оновлення групи:", response_data.get('error'))
    except Exception as e:
        log(f"Помилка оновлення групи через PHP API: {e}")

def GetUserInfo(chat_id:Union[int, str]) -> dict:
    try:
        response = requests.post(PHP_API_URL, data={
            'action': 'get_user',
            'chat_id': chat_id
        })
        response_data = response.json()
        if response.status_code == 200 and response_data.get('user') is not None:
            return response_data['user']
        else:
            log("Помилка отримання користувача:", response_data.get('error'))
            return {}
    except Exception as e:
        log(f"Помилка отримання користувача через PHP API: {e}")
        return {}

def GetAllUserIds() -> list:
    try:
        response = requests.get(USER_IDS_URL)
        if response.status_code == 200:
            result = response.json()

            ignore = GetBlockedUsers()
            return list(set(result) - set(ignore))
        else:
            log(f"Помилка отримання користувачів: {result.get('error')}")
            return []
        
    except Exception as e:
        log(f"Помилка під час запиту(GetAllUserIds) до PHP сервера: {e}")
        return []

def GetAllUsersByGroup(group:Group) -> list:
    try:
        data = {
            "action": "get_chat_ids",
            "group_name": group.name
        }
        response = requests.post(ALL_BY_USERS_URL, data=data)
        result = response.json()
        
        if result.get('success') and 'chat_ids' in result:
            ignore = GetBlockedUsers()
            return list(set(result['chat_ids']) - set(ignore))            
        else:
            log(f"Помилка отримання користувачів групи {group.name}: {result.get('error')}")
            return []
    except Exception as e:
        log(f"Помилка під час запиту(GetAllUsersByGroup) до PHP сервера: {e}")
        return []

def BlockUser(chat_id: Union[int,str]):
    try:
        response = requests.post(BLOCK_USERS_URL,data={
            'action':'block',
            'user_id':chat_id
            })
        response_data = response.json()
        if response.status_code == 200 and response_data.get('status') == 'success':
            log(f"Користувач {chat_id} успішно заблокований!")
        else:
            log(f"Помилка блокування {chat_id}: {response_data.get('message', 'Невідома помилка')}")
    except Exception as e:
        log(f"Помилка підключення до PHP API : {e}")

def GetBlockedUsers() -> list:
    try:
        response = requests.post(GET_BLOCKED_URL,data = {
            'action':'get_blocked'
            })
        response_data = response.json()
        if response.status_code == 200:
            return response_data.get('data',[])
        else:
            log(f"Помилка отримання списку заблокованих: {response_data.get('message', 'Невідома помилка')}")
            return []
    except Exception as e:
        log(f"Помилка підключення до PHP API: {e}")
        return []