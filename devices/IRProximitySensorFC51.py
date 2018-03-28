import pigpio as pigpio
import paho.mqtt.client as mqtt

from devices.Device import Device


class IRProximitySensorFC51(Device):

    mqttc: mqtt.Client = None
    gpio: int = None

    def on_tilt(self, gpio,  edge, tick):

        if edge == 0:
            self.mqttc.publish("rpi/devices/sensors/proximity/" + str(gpio), "true")
        else:
            self.mqttc.publish("rpi/devices/sensors/proximity/" + str(gpio), "false")

    def __init__(self, pi: pigpio.pi, mqttc: mqtt.Client, gpio):
        self.mqttc = mqttc
        self.gpio = gpio
        pi.callback(gpio, 1, self.on_tilt)
        pi.callback(gpio, 0, self.on_tilt)



