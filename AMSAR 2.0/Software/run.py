import _thread as thread
import numpy as np

from USS.tri_uss import USS
from Object_Detection.object_detection import Detector
from Motor_Controls.motor import Motor
from Remote_Controller.controller import Controller

class Runner(Controller):

    def __init__(self):
        # init controls for manual mode
        self.manual = True
        Controller.__init__(self)
        
        # tensorflow initialization
        self.det_val = False
        #self.detector = Detector(use_TPU=False)
        self.detector = Detector(use_TPU=True)
        
        # init uss
        self.uss_val = [False, False, False]
        self.uss = USS(tolerance=100)
        # TODO - initialize USS
        
        # init motor
        self.motor = Motor()
        
        # init sdr
        # TODO - init sdr
        
        while True:
            self.listen_for_controller()
    
    def autonomous(self):
        while not self.manual:
            self.det_val = self.detector.get()
            #self.uss_val = self.uss.get()
            
            if self.
            
            
        return
        
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

runner = Runner()
