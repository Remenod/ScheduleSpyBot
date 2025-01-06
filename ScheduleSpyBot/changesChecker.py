from logger import log
from dataProcessor import CompareAllGroups
import time
import threading

def CheckerLoop(checkCoolDown):
    log("Checker loop started...")
    while True:
        CompareAllGroups()
        time.sleep(checkCoolDown)

def StartCheckerLoop(checkCoolDown):
    thread = threading.Thread(target=CheckerLoop, args=(checkCoolDown,))
    thread.start()