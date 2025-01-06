import requests
from dotenv import load_dotenv
import os
from logger import log

load_dotenv('../Secrets/KEYS.env')

PHP_API_URL       = os.getenv('PHP_API_URL')
USER_IDS_URL      = os.getenv('USER_IDS_URL')
OLD_SCHEDULE_URL  = os.getenv('OLD_SCHEDULE_URL')
ALL_BY_USERS_URL  = os.getenv('ALL_BY_USERS_URL')
SAVE_SCHEDULE_URL = os.getenv('SAVE_SCHEDULE_URL')


#Schedule management

def SaveSchedule(week_number, schedule_text):
    try:
        response = requests.post(PHP_API_URL, data={
            'action': 'save_schedule',
            'week_number': week_number,
            'schedule_text': schedule_text
        })
        response_data = response.json()
        if response.status_code == 200 and response_data.get('success'):    
            log("Розклад успішно збережено через PHP API.")
        else:
            log("Помилка збереження розкладу:", response_data.get('error'))
    except Exception as e:
        log(f"Помилка збереження розкладу через PHP API: {e}")

def GetScheduleFromDB(week_number):
    try:
        response = requests.post(PHP_API_URL, data={
            'action': 'get_schedule',
            'week_number': week_number
        })
        response_data = response.json()
        if response.status_code == 200 and response_data.get('schedule') is not None:
            return response_data['schedule']
        else:
            log("Розкладу для цього тижня не знайдено.")
            return None
    except Exception as e:
        log(f"Помилка отримання розкладу через PHP API: {e}")
        return None

def GetOldSchedule(subgroup):
    data = {
        "action":"get_schedule",
        "subgroup": subgroup
    }
    try:
        response = requests.post(OLD_SCHEDULE_URL,data=data)
        response.raise_for_status()
        result = response.json()
        if "success" in result and result["success"]:            
            return result["schedule"]
        else:
            error_message = result.get("error","Невідома помилка")
            log(f"Помилка:{error_message}")
            return None
    except requests.exceptions.RequestException as e:
        log(f"Помилка запиту до PHP: {e}")
        return None

def WriteSchedule(subgroup,schedule_data):
    log(f"Write Schedule call for {subgroup}")
    data = {
        "action": "save_schedule",
        "subgroup": subgroup,
        "schedule_data": schedule_data
    }
    try:
        response = requests.post(SAVE_SCHEDULE_URL,data=data)
        if response.status_code == 200:
            log("Schedule saved")
            return response.json()
        else:
            log("Write Schedule Error:",response.text)
            return{"error":f"Error{response.status_code}:{response.text}"}
    except Exception as e:
        log(f"Write Schedule Request failed:{e}")
        return{"error":f"Write Schedule Request failed:{e}"}


#User management

def SaveUser(chat_id, full_name, username):
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

def UpdateUserGroup(chat_id, group_name):
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

def GetUserInfo(chat_id):
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
            return None
    except Exception as e:
        log(f"Помилка отримання користувача через PHP API: {e}")
        return None

def GetAllUserIds():
    try:
        response = requests.get(USER_IDS_URL)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            log(f"Помилка отримання користувачів: {result.get('error')}")
            return []
        
    except Exception as e:
        log(f"Помилка під час запиту(GetAllUserIds) до PHP сервера: {e}")
        return []

def GetAllUsersByGroup(group_name):
    try:
        data = {
            "action": "get_chat_ids",
            "group_name": group_name
        }
        response = requests.post(ALL_BY_USERS_URL, data=data)
        result = response.json()
        
        if result.get('success') and 'chat_ids' in result:
            return result['chat_ids']
        else:
            log(f"Помилка отримання користувачів групи {group_name}: {result.get('error')}")
            return []
    except Exception as e:
        log(f"Помилка під час запиту(GetAllUsersByGroup) до PHP сервера: {e}")
        return []