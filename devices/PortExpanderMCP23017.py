import pigpio

from devices.AbstractGPIO import AbstractGPIO
from devices.Controller import Controller

from enum import Enum



class MCPBank(Enum):
    A = 1
    B = 2


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
    modeA = 0xff
    modeB = 0xff

    pi: pigpio.pi = None
    handle = None

    def __init__(self, pi):
        self.handle = pi.i2c_open(1, self.ADDR, 0)
        self.pi = pi
        # Every pin is set as output!
        self.modeA = 0x00
        self.modeB = 0x00
        self.pi.i2c_write_byte_data(self.handle, self.IODIRA, self.modeA)
        self.pi.i2c_write_byte_data(self.handle, self.IODIRB, self.modeB)

    def pin_on(self, bank: MCPBank, pin: int):

        bit = pin - 1
        if bank == MCPBank.B:
            self.valueB = self.valueB | (1 << bit)
            self.pi.i2c_write_byte_data(self.handle, self.OLATB, self.valueB)
        else:
            self.valueA = self.valueA | (1 << bit)
            self.pi.i2c_write_byte_data(self.handle, self.OLATA, self.valueA)

    def pin_input(self, bank: MCPBank, pin: int):

            bit = pin - 1
            if bank == MCPBank.B:
                self.modeB = self.modeB | (1 << bit)
                self.pi.i2c_write_byte_data(self.handle, self.IODIRB, self.modeB)
            else:
                self.modeA = self.modeA | (1 << bit)
                self.pi.i2c_write_byte_data(self.handle, self.IODIRA, self.modeA)

    def pin_output(self, bank: MCPBank, pin: int):

        bit = pin - 1
        if bank == MCPBank.B:
            self.modeB = self.modeB & (0xff - (1 << bit))
            self.pi.i2c_write_byte_data(self.handle, self.OLATB, self.modeB)
        else:
            self.modeA = self.modeA & (0xff - (1 << bit))
            self.pi.i2c_write_byte_data(self.handle, self.OLATA, self.modeA)

    def pin_off(self, bank: MCPBank, pin: int):

        bit = pin - 1
        if bank == MCPBank.B:
            self.valueB = self.valueB & (0xff - (1 << bit))
            self.pi.i2c_write_byte_data(self.handle, self.OLATB, self.valueB)
        else:
            self.valueA = self.valueA & (0xff - (1 << bit))
            self.pi.i2c_write_byte_data(self.handle, self.OLATA, self.valueA)

    def pin_status(self, bank: MCPBank, pin: int):

        bit = pin - 1
        if bank == MCPBank.A:
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

    def get_gpio(self, bank, pin_number):
        return ExpandedGPIO(self, bank, pin_number)


class ExpandedGPIO(AbstractGPIO):

    name = None
    controller: PortExpanderMCP23017 = None
    bank: MCPBank
    pin: int

    def __init__(self, controller: PortExpanderMCP23017, bank: MCPBank, pin: int):
        self.controller = controller
        self.bank = bank
        self.pin = pin

    def on(self):
        self.controller.pin_output(self.bank, self.pin)
        self.controller.pin_on(self.bank, self.pin)

    def off(self):
        self.controller.pin_output(self.bank, self.pin)
        self.controller.pin_off(self.bank, self.pin)

    def write(self, value):
        if value == 0:
            self.off()
        else:
            self.on()

    def set_mode(self, mode):
        if mode == pigpio.OUTPUT:
            self.controller.pin_output(self.bank, self.pin)
        else:
            self.controller.pin_input(self.bank, self.pin)

