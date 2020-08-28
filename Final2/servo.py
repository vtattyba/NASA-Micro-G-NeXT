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
		p = GPIO.PWM(37, 50)
		p.start(0)
		p.ChangeDutyCycle(cycle)
		time.sleep(sleep)
		p.stop()
		return
		
	def straight(self):
		self.__servo__(0.1, 6)
		return
		
	def left(self):
		self.__servo__(0.1, 4.5)
		return
		
	def right(self):
		self.__servo__(0.1, 7.5)
		return

	def quit(self):
		GPIO.cleanup()


servo = Servo()
