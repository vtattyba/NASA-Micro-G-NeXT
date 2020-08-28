#!/usr/bin/python
import RPi.GPIO as GPIO
import time
countL = 0
countR = 0
tg = True
distance = 0
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
def uss(PIN_TRIGGER,PIN_ECHO):
    GPIO.output(PIN_TRIGGER, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(PIN_TRIGGER, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(PIN_TRIGGER, GPIO.LOW)
    while GPIO.input(PIN_ECHO)==0:
          pulse_start_time = time.time()
    while GPIO.input(PIN_ECHO)==1:
          pulse_end_time = time.time()
    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)
    return distance  


 


GPIO.setup(40, GPIO.OUT)
GPIO.setup(38, GPIO.IN)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(35, GPIO.IN)
R = False
L = False
c = False

try:
    while tg:
        
        
        d1 = uss(40,38)
        d2 = uss(33,35)
        
        print("LEFT - " + str(d1) + "    "+ "RIGHT - " + str(d2))
        
       
        if d1 < 100 :
            countL += 1
        if d2 < 100 :
            countR += 1
        if d1 > 100 and d2 > 100:
            countL = 0
            countR = 0
            if c == False:
                #servo(1,6)
                print('straight')

            c = True

        if countL >= 5 :
            #servo(.05, 4.5)
            print('left')

            c = False
           
        if countR >= 5 :
            #servo(.05, 7.5)
            print('right')
            c = False

            
except KeyboardInterrupt:
    GPIO.cleanup()

