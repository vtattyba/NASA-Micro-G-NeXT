import sys, time
import _thread as thread
import numpy as np

from USS.tri_uss import USS
from Object_Detection.object_detection import Detector
from Motor_Controls.motor import Motor
from SDR.sdr import SDR
from Remote_Controller.controller import Controller

class Runner(Controller):

    def __init__(self, args=None):
        # init controls for manual mode
        self.manual = True
        Controller.__init__(self)
        
        # tensorflow initialization
        self.detection = 'none'
        #self.detector = Detector(use_TPU=False)
        self.detector = Detector(use_TPU= False if '--notpu' in args else True)
        
        # init uss
        self.uss_val = 'none'
        self.uss = USS(tolerance=100)
        
        # init motor
        self.motor = Motor()
        
        # init sdr
        self.sdr = SDR()
        
        while True:
            self.listen_for_controller()
    
    def fetch_detector_values(self):
        while not self.manual:
            self.detection = self.detector.get()
        return
    
    def fetch_uss_values(self):
        while not self.manual:
            self.uss_val = self.uss.get()
        return
    
    def start_sensors(self):
        thread.start_new_thread(self.fetch_detector_values, ())        # start to fetch values from detector
        thread.start_new_thread(self.fetch_uss_values, ())             # start to fetch values from ultrasonic sensors
        return 
    
    def autonomous(self):
        #self.start_sensors()
        while not self.manual:
            self.uss_val = self.uss.get()
            self.detection = self.detector.get()
            
            if self.uss_val == 'halt' and self.detection != 'none':
                print('arrived..')
                self.quit()
            elif self.uss_val == 'continue':   # no objects in the way from all the sensors
                if self.detection == 'none':
                    self.motor.stop()
                    sdr_val = self.sdr.get(temp=True)
                    self.turn_based_str(sdr_val)
                else:
                    self.turn_based_on_str(self.detection)
            else:
                self.turn_based_on_str(self.uss_val)
        return 
                
                
    def turn_based_on_str(self, string):
        if string == 'straight':
            self.motor.turn_straight()
            self.motor.set_speed(1800)
        elif string == 'left':
            self.motor.turn_left()
            self.motor.set_speed(1300)
        elif string == 'right':
            self.motor.turn_right()
            self.motor.set_speed(1300)
        elif string == 'halt': 
            self.motor.stop()
        else: # assume halt?
            self.motor.stop()
        return
            
        
    def quit(self):
        return self.on_options_press()
    
    # increase speed of motor 
    def on_up_arrow_press(self):
        if self.manual:
            self.motor.increase_speed()

    # decrease speed of motor 
    def on_down_arrow_press(self):
        if self.manual:
            self.motor.decrease_speed()

    # turn servo left
    def on_left_arrow_press(self):
        if self.manual:
            self.motor.turn_left()

    # turn servo straight when button is released
    def on_left_right_arrow_release(self):
        if self.manual:
            self.motor.turn_straight()
        return

    # turn servo right
    def on_right_arrow_press(self):
        if self.manual:
            self.motor.turn_right()
        return
    
    # quit the program
    def on_options_press(self):
        print('shutting down...')
        self.motor.stop()
        self.motor.quit()
        
        self.uss.quit()
        self.detector.quit()
        
        exit(1)
        return
    
    # change modes
    def on_share_press(self):
        self.manual = not self.manual
        print('manual mode:', self.manual)
        self.motor.stop()
        
        if not self.manual:
            thread.start_new_thread(self.autonomous, ())
        return

runner = Runner(args=sys.argv[1:] if sys.argv else None)
