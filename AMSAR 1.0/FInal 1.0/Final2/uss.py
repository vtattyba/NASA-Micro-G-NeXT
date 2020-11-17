#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import os


class USS:
    def __init__(self):
        self.trig1 = 33
        self.echo1 = 35
        self.trig2 = 40
        self.echo2 = 38
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.trig1, GPIO.OUT)
        GPIO.setup(self.echo1, GPIO.IN)
        GPIO.setup(self.trig2, GPIO.OUT)
        GPIO.setup(self.echo2, GPIO.IN)

    def __uss__(self, PIN_TRIGGER, PIN_ECHO):
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
        
    def check_uss(self):
        now = time.time()
        countL = 0
        countR = 0
        count_stop = 0
        distance = 0
        
        c = False
        try:
            while True:
                uss_ret = 'N'
                dL = self.__uss__(self.trig1, self.echo1)
                dR = self.__uss__(self.trig2, self.echo2)
                
                countL = countL + 1 if dL < 150 else countL
                countR = countR + 1 if dR < 150 else countR
                count_stop = count_stop + 1 if dL < 150 and dR < 150 else count_stop
                
                if dL > 150 and dR > 150:
                    countL = 0
                    countR = 0
                    count_stop = 0
                    if c == False:
                        uss_ret = 'N'
                        break
                    c = True

                if countL >= 5:
                    uss_ret = 'L'
                    break
                    c = False

                if countR >= 5:
                    uss_ret = 'R'
                    break
                    c = False
                
                if count_stop >= 5: # collision ahead! stop!!!
                    uss_ret = 'S'
                    break
            return uss_ret
        except KeyboardInterrupt:
            GPIO.cleanup()
