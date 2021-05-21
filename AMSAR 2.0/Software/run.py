import numpy as np

# for manual controls 
#from Remote_Controller.imports.pyPS4Controller.controller import Controller
from Remote_Controller.imports.pyPS4Controller.custcontroller import Controller

from Object_Detection.object_detection import Detector
from Motor_Controls.motor import Motor

class Runner(Controller):
        
        
    def __init__(self, **kwargs):        
        # init tf lite
        self.obj = False
        self.detector = Detector(use_TPU=False)
        
        # init uss
        self.uss = [False, False, False]
        # TODO - initialize USS
        
        self.motor = Motor()
        
        # init controller
        Controller.__init__(self, **kwargs)
        self.manual = True
        
        self.listen()
        
        return

    # function that switches between autonomous/manual mode
    def on_share_press(self):
        self.manual = not self.manual                # switch modes
        print('manual:', self.manual)
        if not self.manual:                          # if it's autonomous mode, 
            self.__autonomous__()
        return
    
    # increase motor speed (manually)
    def on_up_arrow_press(self):
        if self.manual:
            self.motor.increase_speed()
        return
    
    # decrease motor speed (manually)
    def on_down_arrow_press(self):
        if self.manual:
            self.motor.decrease_speed()
        return
    
    def on_left_arrow_press(self):
        if self.manual:
            self.motor.turn_left()
        return
    
    def on_right_arrow_press(self):
        if self.manual:
            self.motor.turn_right()
        return
        
    def on_left_right_arrow_release(self):
        if self.manual:
            self.motor.turn_straight()
        return
    
    def on_options_press(self):
        print('shutting down...')
        self.motor.stop()
        
    
    def __autonomous__(self):
        print('autonomous mode...')
        # a bunch of if statements on conditions
        done = False
        while not done:
            self.obj = self.detector.check_tf()
                
        self.motor = 0
        return 

runner = Runner(interface='/dev/input/js0', connecting_using_ds4drv=False)
