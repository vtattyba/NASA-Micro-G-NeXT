import RPi.GPIO as GPIO
import time, os

class Motor():
    
    def __init__(self):
        self.speed = 1000
        self.direction = 0
        
        # for motor controls (speed)
        os.system('sudo killall pigpiod')
        os.system("sudo pigpiod")
        os.system('pigs s 5 1000')
        time.sleep(2)
        os.system('pigs s 5 1000')

        # for servo (direction)
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(13, GPIO.OUT)

        print('DONE.')
        return
    
    def set_speed(self, val):
        self.speed = val
        self.speed = min(1800, self.speed)
        self.speed = max(1000, self.speed)
        os.system('pigs s 5 ' + str(self.speed))
        print('motor speed:', self.speed)    
    
    def increase_speed(self):
        self.speed += 100
        self.speed = min(1800, self.speed)
        os.system('pigs s 5 ' + str(self.speed))
        print('motor speed:', self.speed)
        return
    
    def decrease_speed(self):
        self.speed -= 100        
        self.speed = max(1000, self.speed)
        os.system('pigs s 5 ' + str(self.speed))
        print('motor speed:', self.speed)
        return
    
    def turn_left(self):
        self.direction = -45
        self.__servo__(0.1, 7.5)
        print('LEFT')
        return
    
    def turn_straight(self):
        self.direction = 0
        self.__servo__(0.1, 6)
        print('STRAIGHT')
        return
    
    def turn_right(self):
        self.direction = 45
        self.__servo__(0.1, 4.5)
        print('RIGHT')
        return
    
    def stop(self):
        os.system('pigs s 5 1000')
        self.__servo__(0.1, 6)
        print('HALTED.')
        return
    
    def quit(self):
        os.system('pigs s 5 1000')
        os.system('pigs s 5 0')
        os.system('sudo killall pigpiod')
        
        self.__servo__(0.1, 6)
        GPIO.cleanup()
        
        print('EXITING SYSTEM.')
        return
    
    def __servo__(self, sleep, cycle):
        p = GPIO.PWM(13, 50)
        p.start(0)
        p.ChangeDutyCycle(cycle)
        time.sleep(sleep)
        p.stop()
        return