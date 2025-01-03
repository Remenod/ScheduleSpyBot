from botBase import bot
import threading
import time

def UnIdler():
    print("UnIdler started...")
    while True:
        bot.send_message(-1002499863221, 'Calm down snowflakes. UnIdler is running')
        time.sleep(120)


def StartUnIdler():
    thread = threading.Thread(target=UnIdler)
    thread.start()