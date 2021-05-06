import RPi.GPIO as GPIO
from time import sleep


GPIO.setwarnings(False)
servoPIN = 13
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(0) # Initialization
"""
R = False
L = False
c = False


def left_turn():
    serv(1,9)

def right_turn():
    serv(1,3)

def center():
    serv(1,6)


def servo(sleep,cycle):
    p.ChangeDutyCycle(cycle)
    time.sleep(sleep)
    return  

try:
    while True:
 
        move = input("Please enter l or r:\n")
        
        if move == 'r':
            
            print("Servo will turn RIGHT\n")
            servo(1,3)
            

        elif move == 'l':
         
            print("Servo will turn LEFT\n")
            servo(1,9)
           
        if move == 'c':
            servo(1,9)
            p.stop()
          
            
            
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()


"""

p.ChangeDutyCycle(5) # left -90 deg position
sleep(1)
p.ChangeDutyCycle(7.5) # neutral position
sleep(1)
p.ChangeDutyCycle(10) # right +90 deg position
sleep(1)
p.stop()
GPIO.cleanup()
