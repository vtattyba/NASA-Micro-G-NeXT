import subprocess
import sys
import os
#import acceleromter as accl
import time

from detection import Detector
#from sdr import SDR
from servo import Servo
from uss import USS
'''
print("Starting System")
time.sleep(1)
print("Initializing accelerometer")
#force = accl.accel()
'''
force = 1

if force == 1:
    print("Calibrating Motor")
    os.system("pigs s 4 1000")
    time.sleep(2)
    
    servo = Servo()     # servo initialization
    det = Detector()     # tensorflow initialization 
    #sdr = SDR()         # sdr initialization 
    uss = USS()         # uss initialization
    
    while True:
        
        tf_ret = det.check_tf()
    
    tf.quit()
                           


