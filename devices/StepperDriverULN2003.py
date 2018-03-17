import time

import pigpio


class StepperDriverULN2003:

    pi: pigpio.pi = None
    enable_pin = 5
    coil_A_1_pin = 4  # pink
    coil_A_2_pin = 17  # orange
    coil_B_1_pin = 23  # blue
    coil_B_2_pin = 24  # yellow

    step_count = 8
    seq = []

    def __init__(self, pi: pigpio.pi):
        self.seq[0] = [0, 1, 0, 0]
        self.seq[1] = [0, 1, 0, 1]
        self.seq[2] = [0, 0, 0, 1]
        self.seq[3] = [1, 0, 0, 1]
        self.seq[4] = [1, 0, 0, 0]
        self.seq[5] = [1, 0, 1, 0]
        self.seq[6] = [0, 0, 1, 0]
        self.seq[7] = [0, 1, 1, 0]
        self.pi = pi
        self.pi.set_mode(self.enable_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.coil_A_1_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.coil_A_2_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.coil_B_1_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.coil_B_2_pin, pigpio.OUTPUT)

        self.pi.write(self.enable_pin, 1)

    def set_step(self, w1, w2, w3, w4):
        self.pi.write(self.coil_A_1_pin, w1)
        self.pi.write(self.coil_A_2_pin, w2)
        self.pi.write(self.coil_B_1_pin, w3)
        self.pi.write(self.coil_B_2_pin, w4)

    def forward(self, delay, steps):
        for _ in steps:
            for j in range(self.step_count):
                self.set_step(self.seq[j][0], self.seq[j][1], self.seq[j][2], self.seq[j][3])
                time.sleep(delay)

    def backwards(self, delay, steps):
        for i in range(steps):
            for j in reversed(range(self.step_count)):
                self.set_step(self.seq[j][0], self.seq[j][1], self.seq[j][2], self.seq[j][3])
                time.sleep(delay)
