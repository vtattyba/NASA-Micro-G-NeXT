#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import os

countL = 0
countR = 0
tg = True
distance = 0
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


def uss(PIN_TRIGGER, PIN_ECHO):
    GPIO.output(PIN_TRIGGER, GPIO.LOW)
    time.sleep(0.1)
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

trig1 = 29
echo1 = 31
trig2 = 40
echo2 = 38
GPIO.setup(trig1, GPIO.OUT)
GPIO.setup(echo1, GPIO.IN)
GPIO.setup(trig2, GPIO.OUT)
GPIO.setup(echo2, GPIO.IN)

try:
    while tg:

        d1 = uss(trig1, echo1)
        d2 = uss(trig2, echo2)

        print("LEFT - " + str(d1) + "    " + "RIGHT - " + str(d2))

        if d1 < 100:
            countL += 1
        if d2 < 100:
            countR += 1
        if d1 > 100 and d2 > 100:
            countL = 0
            countR = 0
            if c == False:
                os.System("python3 servo_straight.py")
            c = True

        if countL >= 5:
            os.System("python3 servo_left.py")
            c = False

        if countR >= 5:
            os.System("python3 servo_right.py")
            c = False


except KeyboardInterrupt:
    GPIO.cleanup()
