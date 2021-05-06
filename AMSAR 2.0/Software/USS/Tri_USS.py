#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import os

# distance = elapsed * 34000 / 2  # distance of both directions so divide by 2
#     print "Front Distance : %.1f" % distance
#     return distance

GPIO.setmode(GPIO.BOARD)

# Define GPIO for ultrasonic central
TRIGGER_CENTER = 38
ECHO_CENTER = 18
GPIO.setup(TRIGGER_CENTER, GPIO.OUT)
GPIO.setup(ECHO_CENTER, GPIO.IN)

# Define GPIO for ultrasonic Right
TRIGGER_RIGHT = 36
ECHO_RIGHT = 16
GPIO.setup(TRIGGER_RIGHT, GPIO.OUT)
GPIO.setup(ECHO_RIGHT, GPIO.IN)

# Define GPIO for ultrasonic Left
TRIGGER_LEFT = 40
ECHO_LEFT = 32
GPIO.setup(TRIGGER_LEFT, GPIO.OUT)
GPIO.setup(ECHO_LEFT, GPIO.IN)


def motor_full_speed():
    print("full speed")
    #motor

def get_distance(PIN_TRIGGER, PIN_ECHO):
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

# Detect front obstacle
def center():
    distance = get_distance(TRIGGER_CENTER,ECHO_CENTER)
    print("Center : " + str(distance))
    return distance
    

def right():
    distance = get_distance(TRIGGER_RIGHT,ECHO_RIGHT)
    print("Right : " + str(distance))
    return distance


def left():
    distance = get_distance(TRIGGER_LEFT,ECHO_LEFT)
    print("Left : " + str(distance))
    return distance


# Check front obstacle and turn right if there is an obstacle
def avoid_front():
    while center() < 60:
        # Servo turn right
        # low speed motor
        print("Turning Right")
    motor_full_speed()


# Check right obstacle and turn left if there is an obstacle
def avoid_right():
    while right() < 60:
        # Servo turn left
        # low speed motor
        print("Turning Left")
    motor_full_speed()


# Check left obstacle and turn right if there is an obstacle
def avoid_left():
    while left() < 30:
        # Servo turn Right
        # low speed motor
        print("Turning Right")
    motor_full_speed()


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
    
def test():
    while True:
        c = center()
       # l = left()        

def main():
    print("Initializing")
    try:
        test()
    finally:
        print("EXITING")
        GPIO.cleanup()

if __name__ == "__main__":
    print("Running Tri-Setup USS")
    main()

