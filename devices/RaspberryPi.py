import pigpio

from devices.Controller import Controller
from devices.PhysicalGPIO import PhysicalGPIO


class RaspberryPi(Controller):
    pi: pigpio.pi

    def __init__(self, pi: pigpio.pi):
        self.pi = pi

    def get_gpio(self, pin_number):
        return PhysicalGPIO(self.pi, pin_number)
