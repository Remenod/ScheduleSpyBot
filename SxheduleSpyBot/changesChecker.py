from dataProcessor import CompareAllGroups
import time
import threading

def CheckerLoop(checkCoolDown):
    if checkCoolDown < 30:
        raise ValueError("Cooldown must be at least 30 seconds")

    print("Checker loop started...")
    while True:
        CompareAllGroups()
        time.sleep(checkCoolDown)

def StartCheckerLoop(checkCoolDown):
    thread = threading.Thread(target=CheckerLoop, args=(checkCoolDown,))
    thread.start()