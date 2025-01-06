from botBase import bot, logClient
from collections import namedtuple


adminGroupData = namedtuple("adminGroupData", ['groupId','logerThreadId','commandPlaceThreadId'])
adminPanel = adminGroupData(-1002499863221, 2749, 2751)

def log(text, threadId = adminPanel.logerThreadId):
    print(text)
    try:        
        if(threadId == adminPanel.logerThreadId):
            logClient.send_message(adminPanel.groupId, text, message_thread_id=threadId)
        else:
            bot.send_message(adminPanel.groupId, text, message_thread_id=threadId)
    except Exception as e:
        print(e)