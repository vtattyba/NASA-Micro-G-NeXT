import RPi.GPIO as GPIO
import time


class Servo:
	def __init__(self):
		print('initializing servo motor...')
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(37, GPIO.OUT)
		print('DONE.')
		
	def __servo__(self, sleep, cycle):
		p.ChangeDutyCycle(cycle)
		time.sleep(sleep)
		return
		
	def straight(self):
		p = GPIO.PWM(37, 50)
		p.start(0)
		__servo__(0.1, 6)
		p.stop()
		return
		
	def left(self):
		p = GPIO.PWM(37, 50)
		p.start(0)
		__servo__(0.1, 4.5)
		p.stop()
		return
		
	def right(self):
		p = GPIO.PWM(37, 50)
		p.start(0)
		__servo__(0.1, 7.5)
		p.stop()
		return

	def quit(self):
		GPIO.cleanup()
