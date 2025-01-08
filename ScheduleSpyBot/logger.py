from botBase import bot, logClient
from enumerations import AdminPanel

def log(text:str, threadId:int = AdminPanel.logerThreadId.value):
    print(text)
    try:        
        if(threadId == AdminPanel.logerThreadId.value):
            logClient.send_message(AdminPanel.groupId.value, text, message_thread_id=threadId)
        else:
            bot.send_message(AdminPanel.groupId.value, text, message_thread_id=threadId)
    except Exception as e:
        print(f"logger error: {e}")