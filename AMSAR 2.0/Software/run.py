import _thread as thread
import numpy as np

from Object_Detection.object_detection import Detector
from Motor_Controls.motor import Motor
from Remote_Controller.controller import Controller

class Runner(Controller):

    def __init__(self):
        # init controls for manual mode
        self.manual = True
        Controller.__init__(self)
        
        # tensorflow initialization
        self.obj = False
        self.detector = Detector(use_TPU=False)
        
        # init uss
        self.uss = [False, False, False]
        # TODO - initialize USS
        
        # init motor
        self.motor = Motor()
        
        # init sdr
        # TODO - init sdr
        
        self.loop()
        
    def autonomous(self):
        while not self.manual:
            self.obj = self.detector.check_tf()
            print(self.obj)
        return
    
    def loop(self):
        while True:
            self.listen_for_controller()
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
        exit(0)
    
    # change modes
    def on_share_press(self):
        self.manual = not self.manual
        print('manual mode:', self.manual)
        self.motor.stop()
        
        if not self.manual:
            thread.start_new_thread(self.autonomous, ())
        return

runner = Runner()

runner.loop()
