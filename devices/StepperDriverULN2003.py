import time
from collections import deque

import pigpio
from time import sleep

from devices.AbstractGPIO import AbstractGPIO


class StepperDriverULN2003:
    pi: pigpio.pi = None

    fullStepSequence = (
        (1, 0, 0, 0),
        (0, 1, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1)
    )

    halfStepSequence = (
        (1, 0, 0, 0),
        (1, 1, 0, 0),
        (0, 1, 0, 0),
        (0, 1, 1, 0),
        (0, 0, 1, 0),
        (0, 0, 1, 1),
        (0, 0, 0, 1),
        (1, 0, 0, 1)
    )

    def __init__(self, pi, pin1: AbstractGPIO, pin2: AbstractGPIO, pin3: AbstractGPIO, pin4: AbstractGPIO,  delay_after_step=0.003):
        if not isinstance(pi, pigpio.pi):
            raise TypeError("Is not pigpio.pi instance.")
        pin1.set_mode(pigpio.OUTPUT)
        pin2.set_mode(pigpio.OUTPUT)
        pin3.set_mode(pigpio.OUTPUT)
        pin4.set_mode(pigpio.OUTPUT)
        self.pin1 = pin1
        self.pin2 = pin2
        self.pin3 = pin3
        self.pin4 = pin4
        self.pi = pi
        self.delayAfterStep = delay_after_step
        self.deque = deque(self.fullStepSequence)

    def do_counter_clockwise_step(self):
        self.deque.rotate(-1)
        self.do_step_and_delay(self.deque[0])

    def do_clockwise_step(self):
        self.deque.rotate(1)
        self.do_step_and_delay(self.deque[0])

    def do_step_and_delay(self, step):
        self.pin1.write(step[0])
        self.pin2.write(step[1])
        self.pin3.write(step[2])
        self.pin4.write(step[3])
        sleep(self.delayAfterStep)




