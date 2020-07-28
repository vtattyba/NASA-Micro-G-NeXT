import subprocess
import sys
import servo
import acceleromter as accl
import time


print("Starting System")
time.sleep(2)
print("Initializing accelerometer")
ok = accl.accel()

if ok == 1:
    print("Initializing USS")
    pid = subprocess.Popen([sys.executable, "uss.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           stdin=subprocess.PIPE)
    while True:
        ask = input("You are the SDR Give directions (l or r) \n")
        if ask == 'l':
            servo.left()
        elif ask == 'r':
            servo.right()
        else:
            servo.straight()
            break

