import subprocess
import sys
import os
import acceleromter as accl
import time


print("Starting System")
time.sleep(1)
print("Initializing accelerometer")
#force = accl.accel()
force = 1

if force == 1:
    print("Calibrating Motor")
    os.system("pigs s 4 1000")
    time.sleep(2)
    print("Initializing USS")
    pid = subprocess.Popen([sys.executable, "uss.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           stdin=subprocess.PIPE)
    time.sleep(20)
    #print("Initializing TensorFlow")
    # triger TF here 
                          
    print("Initializing SDR")
    #os.system("python3 sdr_automation.py")
	os.system("pigs s 4 1000") #subject to change to the decided speed
    
    #os.system("pigs s 4 1000")
    os.system("pigs s 4 0")
    GPIO.cleanup()
    print("Shutting Down")
                           


