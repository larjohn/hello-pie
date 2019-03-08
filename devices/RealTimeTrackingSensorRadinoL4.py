import pigpio as pigpio
from devices.Device import Device
from helpers.I2CSniffer import I2CSniffer
import struct

class RealTimeTrackingSensorRadinoL4(Device):
    pi: pigpio.pi = None
    address = 0x08
    handle = None
    sniffer = None

    def __init__(self, pi: pigpio.pi, address=0x08):
        self.address = address
        self.pi = pi
        self.handle = pi.i2c_open(1, self.address, 0)

    def read(self):  # channel
        try:
            self.pi.i2c_write_byte(self.handle, 0x08)
            self.pi.i2c_read_byte(self.handle)  # dummy read to start conversion
        except Exception as e:
            print("Address: %s" % self.handle)
            print(e)

        return self.pi.i2c_read_device(self.handle, 2)

    def readfloat(self):
        block = self.pi.i2c_read_block_data(self.handle, 0)  # second arg is 'cmd'. It is andatory but not used in this case. It may be used by the higher level protocol
        # block is a list of 32 elements (int)
        # return block
        n = struct.unpack('<l', ''.join([chr(i) for i in block[:4]]))[0]
        return n

    def readInteger(self):
        # block = self.pi.i2c_read_block_data(self.handle, 0)  # second arg is 'cmd'. It is andatory but not used in this case. It may be used by the higher level protocol
        # block is a list of 32 elements (int)
        # return block


        a =  self.pi.i2c_read_device(self.handle,4)
        return struct.unpack('f', a[1])


    def write(self, val):
        try:
            temp = val  # move string value to temp
            temp = int(temp)  # change string to integer
            # print temp to see on terminal else comment out
            self.pi.i2c_write_byte(self.handle, temp)
        except Exception as e:
            print("Error: Device address: 0x%2X" % self.address)
            print(e)
