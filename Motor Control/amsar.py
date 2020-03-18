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


def servo(sleep,cycle):
    p.ChangeDutyCycle(cycle)
    time.sleep(sleep)
    return  


GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.IN)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(16, GPIO.IN)
servoPIN = 13
GPIO.setup(servoPIN, GPIO.OUT)
p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(0) # Initialization
R = False
L = False
c = False

try:
    while tg:
        
        
        d1 = uss(7,11)
        d2 = uss(18,16)
        
        print("LEFT - " + str(d1) + "    "+ "RIGHT - " + str(d2))
        
       
        if d1 < 100 :
            countL += 1
        if d2 < 100 :
            countR += 1
        if d1 > 100 and d2 > 100:
            countL = 0
            countR = 0
            if c == False:
                servo(1,6)
            c = True

        if countL >= 5 :
            servo(1,9)
            c = False
           
        if countR >= 5 :
            servo(1,3)
            c = False

            
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()

