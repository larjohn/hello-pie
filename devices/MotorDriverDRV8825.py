import pigpio as pigpio
from enum import Enum


class MotorDirection(Enum):
    Forward = 1
    Reverse = -1


class MotorDriverDRV8825:

    pinSTEP = None
    pinSLEEP = None
    pinDIR = None
    frequency = 0

    pi: pigpio.pi = None

    def __init__(self, pi, pin_step, pin_sleep, pin_dir, frequency: int = 550):
        self.pinSTEP = pin_step
        self.pinSLEEP = pin_sleep
        self.pinDIR = pin_dir
        self.pi = pi
        self.frequency = frequency
        self.pi.set_mode(self.pinSTEP, pigpio.OUTPUT)
        self.pi.set_mode(self.pinSLEEP, pigpio.OUTPUT)
        self.pi.set_mode(self.pinDIR, pigpio.OUTPUT)

    def turn(self, motor_direction: MotorDirection, steps: int):
        if motor_direction == MotorDirection.Forward:
            self.pi.write(self.pinDIR, 1)
        else:
            self.pi.write(self.pinDIR, 0)
        self.pi.write(self.pinSLEEP, 1)
        self.wave([[self.frequency, steps]])
        #self.pi.write(self.pinSLEEP, 0)

    def wave(self, ramp):
        """Generate ramp wave forms.
        ramp:  List of [Frequency, Steps]
        """
        self.pi.wave_clear()  # clear existing waves
        length = len(ramp)  # number of ramp levels
        wid = [-1] * length

        # Generate a wave per ramp level
        for i in range(length):
            frequency = ramp[i][0]
            micros = int(500000 / frequency)
            wf = [pigpio.pulse(1 << self.pinSTEP, 0, micros), pigpio.pulse(0, 1 << self.pinSTEP, micros)]
            self.pi.wave_add_generic(wf)
            wid[i] = self.pi.wave_create()

        # Generate a chain of waves
        chain = []
        for i in range(length):
            steps = ramp[i][1]
            x = steps & 255
            y = steps >> 8
            chain += [255, 0, wid[i], 255, 1, x, y]

        end_pulse = [pigpio.pulse(0, 1 << self.pinSLEEP,  1000000)]
        self.pi.wave_add_generic(end_pulse)
        end_pulse_id = self.pi.wave_create()
        chain += [end_pulse_id]

        self.pi.wave_chain(chain)  # Transmit chain.




