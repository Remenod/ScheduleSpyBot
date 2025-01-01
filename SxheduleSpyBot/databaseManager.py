import requests

PHP_API_URL = 'http://telegrambot-rozklad.atwebpages.com/db_handler.php'

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
            print("Користувач успішно збережений або оновлений через PHP API.")
        else:
            print("Помилка збереження користувача:", response_data.get('error'))
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
            print("Групу користувача успішно оновлено через PHP API.")
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