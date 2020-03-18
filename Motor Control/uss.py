#!/usr/bin/python
import RPi.GPIO as GPIO
import time
count = 0
tg = True
distance = 0
GPIO.setmode(GPIO.BOARD)
PIN_TRIGGER = 7
PIN_ECHO = 11       
GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)
GPIO.setwarnings(False)
try:
  while tg:
   
    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    #print "Waiting for sensor to settle"

    time.sleep(.1)

    #print "Calculating distance"

    GPIO.output(PIN_TRIGGER, GPIO.HIGH)

    time.sleep(0.00001)

    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    while GPIO.input(PIN_ECHO)==0:
          pulse_start_time = time.time()
    while GPIO.input(PIN_ECHO)==1:
          pulse_end_time = time.time()
    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)
    print ("Distance:",distance,"cm")
          
    if distance < 100 :
          print ("WARNING - ")
          count += 1 
    if distance > 100:
          count = 0
    if count >= 5 :
          print ("STOP:",distance,"cm")
          tg = False
except KeyboardInterrupt:
  GPIO.cleanup()

"""exec(open("hello.py").read());""" 
