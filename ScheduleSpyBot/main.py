from csAutoCompiler import CompileAll
CompileAll()

import telebot
import threading
import botCommands # This import is necessary to register commands
import changesChecker
import connectionChecker

from logger import log
from botBase import bot


log("Bot started...")

changesChecker.checkTimeout = 900
changesChecker.StartCheckerLoop(changesChecker.checkTimeout)

def reconnecter():
    while True:
        try:
            bot.polling(none_stop=True,timeout=180)
        except telebot.apihelper.ApiException as r:
            if "retry after" in str(e):
                log("Виникла помилка. Забагато запитів.")
        except Exception as e:
            if not connectionChecker.reconnecting_error_sended:
                log(f"Виникла помилка:\n{e}")
                log("Перезапуск...")
                connectionChecker.reconnecting_error_sended = True
reconnecter_thread = threading.Thread(target=reconnecter)
reconnecter_thread.start()

connectionChecker.StartConnectionChecker()