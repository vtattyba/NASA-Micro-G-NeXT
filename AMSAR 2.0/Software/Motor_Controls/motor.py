import RPi.GPIO as GPIO
import time, os

# class the initializes the motor
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
    
    # function that sets the speed of the motor
    # inputs - val - speed to set the motor
    # outputs - None
    def set_speed(self, val):
        self.speed = val
        self.speed = min(1800, self.speed)
        self.speed = max(1000, self.speed)
        os.system('pigs s 5 ' + str(self.speed))
        print('motor speed:', self.speed)    
        return
        
    # function that increases the motor speed by 100
    # inputs - None
    # outputs - None
    def increase_speed(self):
        self.speed += 100
        self.set_speed(self.speed)
        return
    
    # funtion that decreases the speed by 100
    # inputs - None
    # outputs - None
    def decrease_speed(self):
        self.speed -= 100        
        self.set_speed(self.speed)
        return
    
    # function that turns the servo left (approximately 30 degrees)
    # inputs - None
    # outputs - None
    def turn_left(self):
        if self.direction != 7.5:
            self.direction = 7.5
            self.__upd_servo__()
            print('LEFT')
        return

    # function that turns the servo straight (to initial position)
    # inputs - None
    # outputs - None    
    def turn_straight(self):
        if self.direction != 6:
            self.direction = 6
            self.__upd_servo__()
            print('STRAIGHT')
        return
    
    # function that turns the servo right (approximately 30 degrees)
    # inputs - None
    # outputs - None
    def turn_right(self):
        if self.direction != 4.5:
            self.direction = 4.5
            self.__upd_servo__()
            print('RIGHT')
        return
    
    def wiggle(self):
        self.turn_left()
        time.sleep(.75)
        self.turn_straight()
        return 
    
    # function that halts the boat
    # this function does NOT termiante the system
    # inputs - None
    # outputs - None
    def stop(self):
        os.system('pigs s 5 1000')
        if self.direction != 6:
            self.direction = 6
            self.__upd_servo__()
        print('HALTED.')
        return
    
    # function that terminates the motor (used when terminating the system)
    # inputs - None
    # outputs - None 
    def quit(self):
        self.stop()
        os.system('pigs s 5 0')
        os.system('sudo killall pigpiod')
        GPIO.cleanup()
        print('EXITING SYSTEM.')
        return  
    
    # function that updates the servo direction
    # inputs - None, but gets new direction from self.direction
    # outputs - None
    def __upd_servo__(self):
        p = GPIO.PWM(13, 50)
        p.start(0)
        p.ChangeDutyCycle(self.direction)
        time.sleep(0.1)
        p.stop()
        return