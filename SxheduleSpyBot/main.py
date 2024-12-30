from csAutoCompiler import CompileAll
from botBase import bot
import threading
import time

CompileAll()
print("Bot started...")


def UnIdler():
    print("UnIdler started...")
    while True:
        bot.send_message(8154835372, 'Calm down snowflake. UnIdler is running')
        time.sleep(60)

thread = threading.Thread(target=UnIdler)
thread.start()

bot.polling(none_stop=True)
