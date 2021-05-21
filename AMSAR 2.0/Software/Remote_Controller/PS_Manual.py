import RPi.GPIO as GPIO
import time
import pygame
import os
from imports.pyPS4Controller.controller import Controller

#os.system("sudo pigpiod")
"""
sudo bluetoothctl
agent on
discoverable on
pairable on
default-agent

scan on

connect [address]

trust [address]


def servo (cycle):
    p.ChangeDutyCycle(cycle)
    time.sleep(0.05)
    return
"""
def connect():
    # any code you want to run during initial connection with the controller
    pass

def disconnect():
    # any code you want to run during loss of connection with the controller or keyboard interrupt
    pass


class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_up_arrow_press(self):
       print("motor up")

    def on_down_arrow_press(self):
       print("motor down")

    def on_share_press(self):
       print("Mode CHange")

    def on_options_press(self):
       print("KILL EVERYTHING")



controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen()
