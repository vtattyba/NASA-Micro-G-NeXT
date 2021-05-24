import sys, time, subprocess
import _thread as thread
import numpy as np

from USS.tri_uss import USS
from Object_Detection.object_detection import Detector
from Motor_Controls.motor import Motor
from SDR.sdr import SDR
from Remote_Controller.controller import Controller

class Runner(Controller):

    def __init__(self, args=None):
        self.manual = True
        
        # init motor
        self.motor = Motor()
        self.motor.turn_left()
        time.sleep(1)
        self.motor.turn_straight()
        
        # tensorflow initialization
        self.detection = 'none'
        #self.detector = Detector(use_TPU=False)
        self.detector = Detector(use_TPU= False if '--notpu' in args else True)
        
        # init uss
        self.uss_val = 'continue'
        self.uss = USS(tolerance=100)
        
        # init sdr
        self.sdr = SDR(temp=False, min_confidence=30)
        
        while 'ACL' not in str(subprocess.check_output(['hcitool', 'con'])):
            print('waiting...')
        print('CONNECTED.')
        start = time.time()
        while abs(start - time.time()) < 5:
            pass
        
        # init controls for manual mode
        Controller.__init__(self)
        
        self.motor.turn_left()
        time.sleep(1)
        self.motor.turn_straight()
        
        while True:
            self.listen_for_controller()
    
    # function that runs when autonomous mode is activated 
    def autonomous(self):
        # function that operates the motor/servo based on a string command
        def turn_based_on_str(string):
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
        
        last_sdr_update = float('inf')
        while not self.manual:
            self.uss_val = self.uss.get()
            self.detection = self.detector.get()
            
            if self.uss_val == 'halt' and self.detection != 'none':
                print('arrived..')
                self.quit()
            elif self.uss_val == 'continue':   # no objects in the way from all the sensors
                if self.detection == 'none':
                    if abs(last_sdr_update - time.time()) > 3:
                        self.motor.stop()
                        sdr_val = self.sdr.get()
                        turn_based_on_str(sdr_val)
                        last_sdr_update = time.time()
                        
                else:
                    turn_based_on_str(self.detection)
            else:
                turn_based_on_str(self.uss_val)
            
        return     
    
    # function that exits the entire program 
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
