#!/usr/bin/python
import RPi.GPIO as GPIO
import time, os
import numpy as np

# distance = elapsed * 34000 / 2  # distance of both directions so divide by 2
#     print "Front Distance : %.1f" % distance
#     return distance


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
        return
    
    # function that gets reading from sensor given trigger and echo values
    def get_distance(self, PIN_TRIGGER, PIN_ECHO):
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
    
    # check center USS
    def center(self):
        distance = self.get_distance(self.TRIGGER_CENTER, self.ECHO_CENTER)
        print("Center : " + str(distance))
        return distance, True if distance < self.tol else False
        
    # check right USS
    def right(self):
        distance = self.get_distance(self.TRIGGER_RIGHT, self.ECHO_RIGHT)
        print("Right : " + str(distance))
        return distance, True if distance < self.tol else False
    
    # check left USS
    def left(self):
        distance = self.get_distance(self.TRIGGER_LEFT, self.ECHO_LEFT)
        print("Left : " + str(distance))
        return distance, True if distance < self.tol else False
    
    # function that gets the readings for the sensors
    # outputs - (cd, rd, ld) - distance readings of the ultrasonic sensors
    #         - (lb, cb, rb) - whether or not it is within the distance threshold 
    def get(self):
        ret_vals = ['left', 'straight', 'right']
        distance, values = zip(*[self.left, self.center, self.right])
        if all(v == False for v in values): # no objects in front of AMSAR
            return 'none'
        elif all(v == True for v in values): # all sensors detect something within threshold, stop boat, nowhere to go
            return 'halt'
        elif values[0] == values[2] and values[0] == True:
            return 'halt'
        elif values[1]:   # something in the center of the boat
            return 'halt'
        else:
            pass
            # do something else here
        
    
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
