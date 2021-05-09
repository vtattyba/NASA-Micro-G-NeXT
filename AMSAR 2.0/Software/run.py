import numpy as np
from Object_Detection.object_detection import Detector

class Runner():

    def __init__(self):
        print('initializing...')
        self.manual = False                         # manual control via PS4 controller
        
        self.detector = Detector(use_TPU=False)
        
        self.uss = [False, False, False]            # left, center, right sensor (False = no objects, True = object detected)
        self.obj = False                            # object detection (False = no human, True = human)
    
        self.motor = 0
        self.servo = 0

        self.__loop__()
        
        return

    def __loop__(self):
        # a bunch of if statements on conditions
        done = False
        while not done:
            self.obj = self.detector.check_tf()
                

        self.motor = 0
        return 

Runner()
