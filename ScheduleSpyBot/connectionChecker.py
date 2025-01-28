import time
from botBase import bot
from logger import log
import threading

reconnecting_error_sended = False

def connection_checker():
    global reconnecting_error_sended
    while True:
        time.sleep(10)
        try:
            bot.send_message(777000,'')
        except Exception as q:
            if "Bad Request: message text is empty" in str(q) and reconnecting_error_sended:
                log("З'єднання відновленно.")
                reconnecting_error_sended = False
        else:
            if reconnecting_error_sended:
                log("З'єднання відновленно.")
                reconnecting_error_sended = False


def StartConnectionChecker():
    global connection_checker_thread
    connection_checker_thread = threading.Thread(target=connection_checker)
    connection_checker_thread.start()
