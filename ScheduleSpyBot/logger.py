from botBase import bot, logClient
from enumerations import AdminPanel
from datetime import datetime

def log(text:str, threadId:int = AdminPanel.logerThreadId.value):
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"{current_time} - {text}")
    try:
        if(threadId == AdminPanel.logerThreadId.value):
            logClient.send_message(AdminPanel.groupId.value, text, message_thread_id=threadId)
        else:
            bot.send_message(AdminPanel.groupId.value, text, message_thread_id=threadId)
    except Exception as e:
        print(f"logger error: {e}")