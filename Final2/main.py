import subprocess
import sys
import os
#import acceleromter as accl
import time

from detection import Detector
#from sdr import SDR
from servo import Servo
import RPi.GPIO as GPIO
import concurrent.futures

'''
print("Starting System")
time.sleep(1)
print("Initializing accelerometer")
#force = accl.accel()
'''
force = 1


countL = 0
countR = 0
count_stop = 0
distance = 0
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
def uss(PIN_TRIGGER, PIN_ECHO):
    GPIO.output(PIN_TRIGGER, GPIO.LOW)
    time.sleep(0.05)
    GPIO.output(PIN_TRIGGER, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(PIN_TRIGGER, GPIO.LOW)
    while GPIO.input(PIN_ECHO) == 0:
        pulse_start_time = time.time()
    while GPIO.input(PIN_ECHO) == 1:
        pulse_end_time = time.time()
    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)
    return distance
trig1 = 33
echo1 = 35
trig2 = 40
echo2 = 38
c = False
GPIO.setup(trig1, GPIO.OUT)
GPIO.setup(echo1, GPIO.IN)
GPIO.setup(trig2, GPIO.OUT)
GPIO.setup(echo2, GPIO.IN)

if force == 1:
    print("Calibrating Motor")
    os.system("pigs s 4 1000")
    time.sleep(2)
    
    # servo initialization
    servo = Servo()     
    servo.straight()
    
    # tensorflow initialization 
    det = Detector()     
    
    # sdr initialization 
    #sdr = SDR()        
    
    # uss initialization 
    #uss = USS()         
    
    try: 
        while True:
            # DETECTS WHETHER OR NOT PERSON IN FRAME
            # RETURNS: -1 - PERSON IN LEFT SIDE OF FRAME
            #           0 - PERSON IN CENTER OF FRAME
            #           1 - PERSON IN RIGHT OF FRAME
            #           2 - NOTHING FOUNDIN FRAME
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(det.check_tf)
                tf_ret = future.result()
    
            
            # uss
            uss_ret = 'N'
            dL = uss(trig1, echo1)
            dR = uss(trig2, echo2)
            
            countL = countL + 1 if dL < 150 else countL
            countR = countR + 1 if dR < 150 else countR
            count_stop = count_stop + 1 if dL < 150 and dR < 150 else count_stop
            
            if dL > 100 and dR > 100:
                countL = 0
                countR = 0
                count_stop = 0
                if c == False:
                    uss_ret = 'N'
                c = True

            if countL >= 3:
                uss_ret = 'L'
                c = False

            if countR >= 3:
                uss_ret = 'R'
                c = False
            
            if count_stop >= 3: 
                uss_ret = 'S'
                
            print('tf_ret:', tf_ret, 'uss_ret:', uss_ret)
            
            if (tf_ret == 'S' or tf_ret == 'L' or tf_ret == 'R') and uss_ret == 'S':        # arrived at astronaut
                print('DONE')
                det.quit()
                servo.quit()
                GPIO.cleanup()
                break
            elif tf_ret = 'N' and uss_ret == 'S':        # wall 
                print('PANIC.')
            elif uss_ret == 'L':                         # something on left, has to go right
                servo.right()
            elif uss_ret == 'R' :                        # something on right, go left
                servo.left()
            elif tf_ret = 'L' and (uss_ret == 'N' or uss_ret == 'R'):   # detection on left, and nothing in way
                servo.left()
            elif tf_ret = 'R' and (uss_ret == 'N' or uss_ret == 'L'):   # detection on right, and nothing in way
                servo.right()
            elif uss_ret = 'N' and tf_ret == 'N':        # wait for SDR
                pass #temporary
                        
            else:                                        # nothing in way, go straight                                     
                servo.straight()
        
    except KeyboardInterrupt:
        det.quit()
        servo.quit()
        GPIO.cleanup()
                           


