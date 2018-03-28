import pigpio

from devices.AbstractGPIO import AbstractGPIO


class PhysicalGPIO(AbstractGPIO):

    name = None
    controller: pigpio.pi = None
    gpio: None

    def __init__(self, controller: pigpio.pi, gpio_number: int):
        self.controller = controller
        self.gpio = gpio_number

    def set_mode(self, mode):
        self.controller.set_mode(self.gpio, mode)

    def on(self):
        self.controller.write(self.gpio, 1)

    def off(self):
        self.controller.write(self.gpio, 0)

    def write(self, value):
        self.controller.write(self.gpio, value)
