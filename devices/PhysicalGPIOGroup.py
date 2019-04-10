import pigpio

from devices import AbstractGPIO
from devices.AbstractGPIOGroup import AbstractGPIOGroup


class PhysicalGPIOGroup(AbstractGPIOGroup):

    name = None
    controller: pigpio.pi = None
    gpios: [AbstractGPIO]

    def __init__(self, controller: pigpio.pi, gpios: [AbstractGPIO]):
        self.controller = controller
        self.gpios = gpios
        for j in range(self.gpios.count):
            self.gpios[j].set_mode(pigpio.OUTPUT)

    def set_step(self, bits):
        for j in range(self.gpios.count):
            self.gpios[j].write(bits[j])
