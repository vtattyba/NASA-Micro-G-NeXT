import RPi.GPIO as GPIO
import time, os

class Motor():
    
    def __init__(self):
        self.speed = 1000
        self.direction = 0 # can be 4.5, 6, 7.5, for left center right
        
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
        if self.direction != 7.5:
            self.direction = 7.5
            self.__upd_servo__()
            print('LEFT')
        return
    
    def turn_straight(self):
        if self.direction != 6:
            self.direction = 6
            self.__upd_servo__()
            print('STRAIGHT')
        return
    
    def turn_right(self):
        if self.direction != 4.5:
            self.direction = 4.5
            self.__upd_servo__()
            print('RIGHT')
        return
    
    def stop(self):
        os.system('pigs s 5 1000')
        if self.direction != 6:
            self.direction = 6
            self.__upd_servo__()
        print('HALTED.')
        return
    
    def quit(self):
        self.stop()
        os.system('pigs s 5 0')
        os.system('sudo killall pigpiod')
        GPIO.cleanup()
        print('EXITING SYSTEM.')
        return
    
    def __upd_servo__(self):
        p = GPIO.PWM(13, 50)
        p.start(0)
        p.ChangeDutyCycle(self.direction)
        time.sleep(0.1)
        p.stop()
        return