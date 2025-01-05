from dataProcessor import CompareAllGroups
import time
import threading

def CheckerLoop(checkCoolDown):
    limit = 30
    if checkCoolDown < limit:
        raise ValueError(f"Cooldown must be at least {limit} seconds")

    print("Checker loop started...")
    while True:
        CompareAllGroups()
        time.sleep(checkCoolDown)

def StartCheckerLoop(checkCoolDown):
    thread = threading.Thread(target=CheckerLoop, args=(checkCoolDown,))
    thread.start()