from botBase import bot, logClient
from enumerations import AdminPanel

def log(text:str, threadId:int = AdminPanel.logerThreadId):
    print(text)
    try:        
        if(threadId == AdminPanel.logerThreadId):
            logClient.send_message(AdminPanel.groupId, text, message_thread_id=threadId)
        else:
            bot.send_message(AdminPanel.groupId, text, message_thread_id=threadId)
    except Exception as e:
        print(f"logger error: {e}")