from devices.AbstractGPIO import AbstractGPIO


class ExtendedGPIO(AbstractGPIO):

    name = None
    controller = None

    def __init__(self, controller):
        self.controller =  controller
