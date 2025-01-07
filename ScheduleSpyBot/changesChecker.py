import time
import threading
from logger import log
from dataProcessor import CompareAllGroups

def CheckerLoop(checkCoolDown:int):
    log("Checker loop started...")
    while True:
        CompareAllGroups()
        time.sleep(checkCoolDown)

def StartCheckerLoop(checkCoolDown:int):
    thread = threading.Thread(target=CheckerLoop, args=(checkCoolDown,))
    thread.start()