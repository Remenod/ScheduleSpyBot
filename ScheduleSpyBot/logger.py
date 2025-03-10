from telebot.apihelper import ApiException
from botBase import bot, logClient
from enumerations import AdminPanel
from datetime import datetime
from pytz import timezone


def log(text: str, threadId: int = AdminPanel.loggerThreadId.value):
    try:
        current_time = datetime.now(timezone('Europe/Kyiv')).strftime('%H:%M:%S')
        print(f'{current_time} - {text}')
        if threadId == AdminPanel.loggerThreadId.value:
            logClient.ensure_send_message(
                AdminPanel.groupId.value, str(text), message_thread_id=threadId
            )
        else:
            bot.ensure_send_message(AdminPanel.groupId.value, str(text), message_thread_id=threadId)
    except ApiException as e:
        if 'retry after' in str(e):
            log('Виникла помилка Логера. Забагато запитів.')
    except Exception as e:
        print(f'logger error: {e}')
