import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
servoPIN = 13
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50)  # GPIO 17 for PWM with 50Hz
p.start(0)  # Initialization


def servo(sleep, cycle):
    p.ChangeDutyCycle(cycle)
    time.sleep(sleep)
    p.ChangeDutyCycle(6)
    return


try:

    def left():
        print("servo left")
        servo(1, 9)


    def right():
        print("servo right")
        servo(1, 3)


    def straight():
        print("servo straight")
        p.ChangeDutyCycle(6)

except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
