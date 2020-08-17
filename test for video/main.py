import subprocess
import sys
import os
import acceleromter as accl
import time


print("Starting System")
time.sleep(1)
print("Initializing accelerometer")
ok = 1

if ok == 1:
    print("Initializing USS")
    pid = subprocess.Popen([sys.executable, "uss.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           stdin=subprocess.PIPE)
    while True:
        ask = input("You are the SDR Give directions (l or r) \n")
        if ask == 'l':
            os.system("python3 servo_left.py")
        elif ask == 'r':
            os.system("python3 servo_right.py")
        else:
            os.system("python3 servo_straight.py")
            break

