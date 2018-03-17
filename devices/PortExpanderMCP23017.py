import abc

import pigpio

from devices.Controller import Controller


class PortExpanderMCP23017(Controller):
    ADDR = 0x20
    IODIRA = 0x00
    IODIRB = 0x01
    GPIOA = 0x12
    GPIOB = 0x13
    OLATA = 0x14
    OLATB = 0x15
    valueA = 0x00
    valueB = 0x00

    pi: pigpio.pi = None
    handle = None

    def __init__(self, pi):
        self.handle = pi.i2c_open(1, self.ADDR, 0)
        self.pi = pi
        # Every pin is set as output!
        self.pi.i2c_write_byte_data(self.handle, self.IODIRA, 0x00)
        self.pi.i2c_write_byte_data(self.handle, self.IODIRB, 0x00)

    def pin_on(self, bank, pin):

        bit = pin - 1
        if bank == 'B':
            self.valueB = self.valueB | (1 << bit)
            self.pi.i2c_write_byte_data(self.handle, self.OLATB, self.valueB)
        else:
            self.valueA = self.valueA | (1 << bit)
            self.pi.i2c_write_byte_data(self.handle, self.OLATA, self.valueA)

    def pin_off(self, bank, pin):

        bit = pin - 1
        if bank == 'B':
            self.valueB = self.valueB & (0xff - (1 << bit))
            self.pi.i2c_write_byte_data(self.handle, self.OLATB, self.valueB)
        else:
            self.valueA = self.valueA & (0xff - (1 << bit))
            self.pi.i2c_write_byte_data(self.ADDR, self.OLATA, self.valueA)

    def pin_status(self, bank, pin):

        bit = pin - 1
        if bank == 'A':
            state = ((self.valueA & (1 << bit)) != 0)
        else:
            state = ((self.valueB & (1 << bit)) != 0)
        return state

    def pin_all_off(self):

        self.valueA = 0x0
        self.pi.i2c_write_byte_data(self.handle, self.OLATA, self.valueA)
        self.valueB = 0x0
        self.pi.i2c_write_byte_data(self.handle, self.OLATB, self.valueB)

    def pin_all_on(self):

        self.valueA = 0xff
        self.pi.i2c_write_byte_data(self.handle, self.OLATA, self.valueA)
        self.valueB = 0xff
        self.pi.i2c_write_byte_data(self.handle, self.OLATB, self.valueB)


    