from botBase import bot, logClient
from enumerations import AdminPanel
from datetime import datetime
from pytz import timezone

def log(text:str, threadId:int = AdminPanel.logerThreadId.value):    
    try:
        current_time = datetime.now(timezone("Europe/Kyiv")).strftime("%H:%M:%S")
        print(f"{current_time} - {text}")
        if(threadId == AdminPanel.logerThreadId.value):
            logClient.send_message(AdminPanel.groupId.value, text, message_thread_id=threadId)
        else:
            bot.send_message(AdminPanel.groupId.value, text, message_thread_id=threadId)
    except Exception as e:
        print(f"logger error: {e}")