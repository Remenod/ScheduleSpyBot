from dataclasses import dataclass
from multiprocessing.util import SUBDEBUG
from sched import scheduler
from unittest import result
from urllib import response
import requests

PHP_API_URL = 'http://telegrambot-rozklad.atwebpages.com/db_handler.php'
USER_IDS_URL = 'http://telegrambot-rozklad.atwebpages.com/get_user_ids.php'
SAVE_SCHEDULE_URL = 'http://telegrambot-rozklad.atwebpages.com/Schedules.php'
OLD_SCHEDULE_URL = 'http://telegrambot-rozklad.atwebpages.com/old_schedule.php'
ALL_BY_USERS_URL = 'http://telegrambot-rozklad.atwebpages.com/get_all_users_by_group.php'
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
            print("Розклад успішно збережено через PHP API.")
        else:
            print("Помилка збереження розкладу:", response_data.get('error'))
    except Exception as e:
        print(f"Помилка збереження розкладу через PHP API: {e}")

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
            return "Розкладу для цього тижня не знайдено."
    except Exception as e:
        print(f"Помилка отримання розкладу через PHP API: {e}")
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
            print(f"Помилка:{error_message}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Помилка запиту до PHP: {e}")
        return None

def WriteSchedule(subgroup,schedule_data):
    print(f"Write Schedule call for {subgroup}")
    data = {
        "action": "save_schedule",
        "subgroup": subgroup,
        "schedule_data": schedule_data
    }
    try:
        response = requests.post(SAVE_SCHEDULE_URL,data=data)
        if response.status_code == 200:
            print("Schedule saved")
            return response.json()
        else:
            print("Error:",response.text)
            return{"error":f"Error{response.status_code}:{response.text}"}
    except Exception as e:
        print(f"Request failed:{str(e)}")
        return{"error":f"Request failed:{str(e)}"}


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
            print(f"Користувач {full_name} успішно збережений або оновлений через PHP API.")
        else:
            print(f"Помилка збереження користувача {full_name}:", response_data.get('error'))
    except Exception as e:
        print(f"Помилка збереження користувача через PHP API: {e}")

def UpdateUserGroup(chat_id, group_name):
    try:
        response = requests.post(PHP_API_URL, data={
            'action': 'update_group',
            'chat_id': chat_id,
            'group_name': group_name
        })
        response_data = response.json()
        if response.status_code == 200 and response_data.get('success'):
            print(f"Групу користувача {chat_id} успішно оновлено через PHP API.")
        else:
            print("Помилка оновлення групи:", response_data.get('error'))
    except Exception as e:
        print(f"Помилка оновлення групи через PHP API: {e}")

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
            print("Помилка отримання користувача:", response_data.get('error'))
            return None
    except Exception as e:
        print(f"Помилка отримання користувача через PHP API: {e}")
        return None

def GetAllUserIds():
    try:
        response = requests.get(USER_IDS_URL)
        if response.status_code == 200:
            user_ids = response.json()
            return user_ids
        else:
            print(f"Помилка запиту до PHP серверу: {response.status_code}")
            return []
        
    except Exception as e:
        print(f"Помилка під час запиту до PHP сервера: {e}")
        return []

def GetAllUsersByGroup(group_name):
    data = {
        "action": "get_chat_ids",
        "group_name": group_name
    }
    response = requests.post(ALL_BY_USERS_URL, data=data)
    result = response.json()
        
    if result.get('success') and 'chat_ids' in result:
        return result['chat_ids']
        
    return []
