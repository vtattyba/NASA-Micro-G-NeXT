#!/usr/bin/python
import RPi.GPIO as GPIO
import time, os
import numpy as np
from collections import deque

# distance = elapsed * 34000 / 2  # distance of both directions so divide by 2
#     print "Front Distance : %.1f" % distance
#     return distance


# class to define the USS module for initializing and retrieving sensors data. 
class USS():    
    def __init__(self, tolerance=100):
        self.tol = tolerance
        GPIO.setmode(GPIO.BOARD)

        # Define GPIO for ultrasonic central
        self.TRIGGER_CENTER = 38
        self.ECHO_CENTER = 18
        GPIO.setup(self.TRIGGER_CENTER, GPIO.OUT)
        GPIO.setup(self.ECHO_CENTER, GPIO.IN)

        # Define GPIO for ultrasonic Right
        self.TRIGGER_RIGHT = 36
        self.ECHO_RIGHT = 16
        GPIO.setup(self.TRIGGER_RIGHT, GPIO.OUT)
        GPIO.setup(self.ECHO_RIGHT, GPIO.IN)

        # Define GPIO for ultrasonic Left
        self.TRIGGER_LEFT = 40
        self.ECHO_LEFT = 32
        GPIO.setup(self.TRIGGER_LEFT, GPIO.OUT)
        GPIO.setup(self.ECHO_LEFT, GPIO.IN)
        
        self.history = [deque(maxlen=5), deque(maxlen=5), deque(maxlen=5)]
        return
    
    # function that gets reading from sensor given trigger and echo values
    # inputs - PIN_TRIGGER - 
    #        - PIN_ECHO - 
    # outputs - distance from sensor to closest object detected by a sensor
    def get_distance(self, PIN_TRIGGER, PIN_ECHO):
        GPIO.output(PIN_TRIGGER, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(PIN_TRIGGER, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(PIN_TRIGGER, GPIO.LOW)
        pulse_start_time = time.time()
        while GPIO.input(PIN_ECHO) == 0:
            pulse_start_time = time.time()
        pulse_end_time = time.time()
        while GPIO.input(PIN_ECHO) == 1:
            pulse_end_time = time.time()
        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)
        return distance
    
    # check center USS
    def center(self):
        distance = self.get_distance(self.TRIGGER_CENTER, self.ECHO_CENTER)
        return distance
        
    # check right USS
    def right(self):
        distance = self.get_distance(self.TRIGGER_RIGHT, self.ECHO_RIGHT)
        return distance
    
    # check left USS
    def left(self):
        distance = self.get_distance(self.TRIGGER_LEFT, self.ECHO_LEFT)
        return distance
    
    # function that gets the readings for the sensors
    # outputs direction to turn OR to stop OR to continue with path (no objects at all)
    def get(self):
        distances = [self.left(), self.center(), self.right()]   # raw values of whether or not the distance passes the threshold
        thresh_values = [True if d < self.tol else False for d in distances]
        for i, d in enumerate(thresh_values):
            self.history[i].append(d)
        #print('L: %4.2f    |    C: %4.2f    |    R: %4.2f' % tuple(distances))
        values = [v.count(True) >= 3 for v in self.history]
        if all(v == False for v in values):                 # no objects in front of AMSAR
            return 'continue'
        elif values[1]:                                     # object directly in front of AMSAR
            return 'halt'
        elif values[0]:                                     # something to the left, turn right
            return 'right'
        elif values[2]:                                     # something to the right, turn left
            return 'left'
        else:
            print('ERROR?')
        
    def quit(self):
        GPIO.cleanup()
        return

'''
# Avoid obstacles and drive forward
def avoid_obstacle():
    start = time.time()
    while start > time.time() - 60:  # 60 seconds
        if center() < 10:
            print("FRONT  Warning")
            # Stop Motor Here
            # time to stop
            avoid_front()
        elif right() < 10:
            print("RIGHT  Warning")
            # Stop Motor Here
            avoid_right()
        elif left() < 10:
            print("LEFT  Warning")
            # Stop Motor Here
            avoid_left()
        print("---------------")
    
    print("EXITING")
    GPIO.cleanup()
'''
