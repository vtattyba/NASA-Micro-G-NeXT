import os, struct, time
import numpy as np

from Object_Detection.object_detection import Detector
from Motor_Controls.motor import Motor


class Runner():

    def __init__(self, interface, connecting_using_ds4drv=True, event_definition=None, event_format=None):
        self.manual = True
        # controller initializaiton
        self.stop = False
        self.is_connected = False
        self.interface = interface
        self.connecting_using_ds4drv = connecting_using_ds4drv
        self.debug = False  # If you want to see raw event stream, set this to True.
        self.black_listed_buttons = []  # set a list of blocked buttons if you dont want to process their events
        if self.connecting_using_ds4drv and event_definition is None:
            # when device is connected via ds4drv its sending hundreds of events for those button IDs
            # thus they are blacklisted by default. Feel free to adjust this list to your linking when sub-classing
            self.black_listed_buttons += [6, 7, 8, 11, 12, 13]
        self.event_format = event_format if event_format else "3Bh2b"

        if event_definition is None:  # means it wasn't specified by user
            if self.event_format == "LhBB":
                from pyPS4Controller.event_mapping.DefaultMapping import DefaultMapping
                self.event_definition = DefaultMapping
            else:
                from pyPS4Controller.event_mapping.Mapping3Bh2b import Mapping3Bh2b
                self.event_definition = Mapping3Bh2b
        else:
            self.event_definition = event_definition

        self.event_size = struct.calcsize(self.event_format)
        self.event_history = []
        
        # tensorflow initialization
        self.obj = False
        self.detector = Detector(use_TPU=True)
        
        # init uss
        self.uss = [False, False, False]
        # TODO - initialize USS
        
        self.motor = Motor()

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
        self.__loop__()
        return
    
    def listen(self, timeout=30, on_connect=None, on_disconnect=None, on_sequence=None):
        """
        Start listening for events on a given self.interface
        :param timeout: INT, seconds. How long you want to wait for the self.interface.
                        This allows you to start listening and connect your controller after the fact.
                        If self.interface does not become available in N seconds, the script will exit with exit code 1.
        :param on_connect: function object, allows to register a call back when connection is established
        :param on_disconnect: function object, allows to register a call back when connection is lost
        :param on_sequence: list, allows to register a call back on specific input sequence.
                            e.g [{"inputs": ['up', 'up', 'down', 'down', 'left', 'right,
                                             'left', 'right, 'start', 'options'],
                                  "callback": () -> None)}]
        :return: None
        """
        def on_disconnect_callback():
            self.is_connected = False
            if on_disconnect is not None:
                on_disconnect()

        def on_connect_callback():
            self.is_connected = True
            if on_connect is not None:
                on_connect()

        def wait_for_interface():
            print("Waiting for interface: {} to become available . . .".format(self.interface))
            for i in range(timeout):
                if os.path.exists(self.interface):
                    print("Successfully bound to: {}.".format(self.interface))
                    on_connect_callback()
                    return
                time.sleep(1)
            print("Timeout({} sec). Interface not available.".format(timeout))
            exit(1)

        def read_events():
            try:
                return _file.read(self.event_size)
            except IOError:
                print("Interface lost. Device disconnected?")
                on_disconnect_callback()
                exit(1)

        def check_for(sub, full, start_index):
            return [start for start in range(start_index, len(full) - len(sub) + 1) if
                    sub == full[start:start + len(sub)]]

        def unpack():
            __event = struct.unpack(self.event_format, event)
            return (__event[3:], __event[2], __event[1], __event[0])

        wait_for_interface()
        try:
            _file = open(self.interface, "rb")
            event = read_events()
            if on_sequence is None:
                on_sequence = []
            special_inputs_indexes = [0] * len(on_sequence)
            while not self.stop and event:
                (overflow, value, button_type, button_id) = unpack()
                if button_id not in self.black_listed_buttons:
                    self.__handle_event(button_id=button_id, button_type=button_type, value=value, overflow=overflow,
                                        debug=self.debug)
                for i, special_input in enumerate(on_sequence):
                    check = check_for(special_input["inputs"], self.event_history, special_inputs_indexes[i])
                    if len(check) != 0:
                        special_inputs_indexes[i] = check[0] + 1
                        special_input["callback"]()
                event = read_events()
        except KeyboardInterrupt:
            print("\nExiting (Ctrl + C)")
            on_disconnect_callback()
            exit(1)

    def __handle_event(self, button_id, button_type, value, overflow, debug):

        event = self.event_definition(button_id=button_id,
                                      button_type=button_type,
                                      value=value,
                                      connecting_using_ds4drv=self.connecting_using_ds4drv,
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

runner = Runner(interface='/dev/input/js0', connecting_using_ds4drv=False)
runner.listen()


