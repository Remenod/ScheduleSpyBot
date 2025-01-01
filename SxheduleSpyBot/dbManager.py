import requests

PHP_API_URL = 'http://telegrambot-rozklad.atwebpages.com/db_handler.php'

def save_schedule(week_number, schedule_text):
    """Зберігає розклад через PHP API"""
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

def get_schedule_from_db(week_number):
    """Отримує розклад через PHP API"""
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
