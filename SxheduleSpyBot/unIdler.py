from botBase import bot
import threading
import time

def UnIdler():
    print("UnIdler started...")
    while True:
        bot.send_message(8154835372, 'Calm down snowflake. UnIdler is running')
        time.sleep(60)


def StartUnIdler():
    thread = threading.Thread(target=UnIdler)
    thread.start()