from imports.pyPS4Controller.controller import Controller
"""
sudo bluetoothctl
agent on
discoverable on
pairable on
default-agent

scan on

connect [address]

trust [address]
"""

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)


controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen()
