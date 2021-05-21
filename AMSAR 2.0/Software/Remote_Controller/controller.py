import os, struct, time
import numpy as np

from pyPS4Controller.event_mapping.Mapping3Bh2b import Mapping3Bh2b


class Controller():
    def __init__(self):
        self.interface = '/dev/input/js0'
        self.event_format = '3Bh2b'
        self.event_definition = Mapping3Bh2b
        
        self.event_size = struct.calcsize(self.event_format)
        self.event_history = []
        
        self.init_controller()
        
    def init_controller(self, timeout=30):
        print("Waiting for interface: {} to become available . . .".format(self.interface))
        for i in range(timeout):
            if os.path.exists(self.interface):
                print("Successfully bound to: {}.".format(self.interface))
                self._file = open(self.interface, "rb")
                return
            time.sleep(1)
        print("Timeout({} sec). Interface not available.".format(timeout))
        exit(1)
        return 
        
    def listen_for_controller(self):
        try:
            if self._file.readable():
                event = self._file.read(self.event_size)
        except IOError:
            print("Interface lost. Device disconnected?")
            exit(1)

        __event = struct.unpack(self.event_format, event)
        (overflow, value, button_type, button_id) = (__event[3:], __event[2], __event[1], __event[0])
        self.__handle_event(button_id=button_id, button_type=button_type, value=value, overflow=overflow,
                            debug=False)

        return
       
    
    def on_up_arrow_press(self):
        print('UP ARROW')
        return
    
    def on_down_arrow_press(self):
        print('DOWN ARROW')
        return
    
    def on_left_right_arrow_release(self):
        print('LEFT RIGHT ARROW RELEASE')
        return
    
    def on_right_arrow_press(self):
        print('RIGHT ARROW')
        return
        
    def on_options_press(self):
        print('OPTIONS PRESS')
        return
        
    def on_share_press(self):
        print('SHARE PRESS')
        return
   
    
    
    def __handle_event(self, button_id, button_type, value, overflow, debug):

        event = self.event_definition(button_id=button_id,
                                      button_type=button_type,
                                      value=value,
                                      connecting_using_ds4drv=False,
                                      overflow=overflow,
                                      debug=debug)
        if event.options_pressed():
            self.event_history.append("options")
            self.on_options_press()
        elif event.left_right_arrow_released():
            self.on_left_right_arrow_release()
        elif event.left_arrow_pressed():
            self.event_history.append("left")
            self.on_left_arrow_press()
        elif event.right_arrow_pressed():
            self.event_history.append("right")
            self.on_right_arrow_press()
        elif event.up_arrow_pressed():
            self.event_history.append("up")
            self.on_up_arrow_press()
        elif event.down_arrow_pressed():
            self.event_history.append("down")
            self.on_down_arrow_press()
        elif event.share_pressed():
            self.event_history.append("share")
            self.on_share_press()
