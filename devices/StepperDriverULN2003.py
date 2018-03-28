import time

import pigpio

from devices.AbstractGPIO import AbstractGPIO


class StepperDriverULN2003:

    pi: pigpio.pi = None
    enable_pin = 5
    coil_A_1_pin = None  # IN2
    coil_A_2_pin = None  # IN4
    coil_B_1_pin = None  # IN1
    coil_B_2_pin = None  # IN3

    step_count = 8
    seq = [0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self, pi: pigpio.pi, in1: AbstractGPIO, in2: AbstractGPIO, in3: AbstractGPIO, in4: AbstractGPIO):
        self.seq[0] = [0, 1, 0, 0]
        self.seq[1] = [0, 1, 0, 1]
        self.seq[2] = [0, 0, 0, 1]
        self.seq[3] = [1, 0, 0, 1]
        self.seq[4] = [1, 0, 0, 0]
        self.seq[5] = [1, 0, 1, 0]
        self.seq[6] = [0, 0, 1, 0]
        self.seq[7] = [0, 1, 1, 0]
        self.pi = pi
        self.coil_B_1_pin = in1
        self.coil_A_1_pin = in2
        self.coil_B_2_pin = in3
        self.coil_A_2_pin = in4
        self.pi.set_mode(self.enable_pin, pigpio.OUTPUT)
        self.pi.write(self.enable_pin, 1)

        self.coil_A_1_pin.set_mode(pigpio.OUTPUT)
        self.coil_A_2_pin.set_mode(pigpio.OUTPUT)
        self.coil_B_1_pin.set_mode(pigpio.OUTPUT)
        self.coil_B_2_pin.set_mode(pigpio.OUTPUT)

    def set_step(self, w1, w2, w3, w4):
        self.coil_A_1_pin.write(w1)
        self.coil_A_2_pin.write(w2)
        self.coil_B_1_pin.write(w3)
        self.coil_B_2_pin.write(w4)

    def forward(self, delay, steps):
        for _ in range(steps):
            for j in range(self.step_count):
                self.set_step(self.seq[j][0], self.seq[j][1], self.seq[j][2], self.seq[j][3])
                time.sleep(delay)
        self.set_step(0, 0, 0, 0)

    def backwards(self, delay, steps):
        for i in range(steps):
            for j in reversed(range(self.step_count)):
                self.set_step(self.seq[j][0], self.seq[j][1], self.seq[j][2], self.seq[j][3])
                time.sleep(delay)
        self.set_step(0, 0, 0, 0)

