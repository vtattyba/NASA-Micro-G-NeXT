import subprocess
import sys
import os
import time
import RPi.GPIO as GPIO

#import acceleromter as accl
from detection import Detector
#from sdr import SDR
from motor import Motor
from servo import Servo


print("Starting System")
time.sleep(1)
print("Initializing accelerometer")
force = accl.accel()

#force = 1


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
    # motor initialization
    motor = Motor()
    
    # servo initialization
    servo = Servo()     
    servo.straight()
    
    # tensorflow initialization 
    det = Detector()     
    
    # sdr initialization 
    #sdr = SDR()           
    
    try: 
        while True:
            tf_ret = det.check_tf()
            # uss
            uss_ret = 'N'
            dL = uss(trig1, echo1)
            dR = uss(trig2, echo2)
            countL = countL + 1 if dL < 100 else countL
            countR = countR + 1 if dR < 100 else countR
            count_stop = count_stop + 1 if dL < 100 and dR < 100 else count_stop
            
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
                print('Hi astronaut')
                break
            elif tf_ret == 'N' and uss_ret == 'N':        
                # wait for SDR
                pass
            elif tf_ret == 'S' and uss_ret == 'N':
                servo.straight()
                # motor.rpm(1300)
            elif tf_ret == 'N' and uss_ret == 'S':      # something ahead, not human, stop.
                print('Hi Wall')
                motor.halt()
            elif tf_ret == 'L' and (uss_ret == 'N' or uss_ret == 'R'):
                servo.right()
                #motor.rpm(1200)
            elif tf_ret == 'R' and (uss_ret == 'N' or uss_ret == 'L'):
                servo.left()
                #motor.rpm(1200)
            elif (tf_ret == 'N' or tf_ret == 'S') and uss_ret == 'L':
                servo.left()
                #motor.rpm(1200)
            elif (tf_ret == 'N' or tf_ret == 'S') and uss_ret == 'R':
                servo.right()
                #motor.rpm(1200)
            elif tf_ret == 'L' and uss_ret == 'L':
                servo.right()
                break
            elif tf_ret == 'R' and uss_ret == 'R':
                servo.left()
                break
        motor.quit()
        det.quit()
        servo.quit()
        GPIO.cleanup()
    except KeyboardInterrupt:
        motor.quit()
        det.quit()
        servo.quit()
        GPIO.cleanup()
                           


