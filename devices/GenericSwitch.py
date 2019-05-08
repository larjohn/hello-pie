import pigpio as pigpio
import paho.mqtt.client as mqtt
import time
from devices.Device import Device


class GenericSwitch(Device):

    mqttc: mqtt.Client = None
    gpio: int = None

    def on_edge(self, gpio, edge, tick):

        if edge == 1:
            self.mqttc.publish("rpi/devices/sensors/switch/" + str(gpio), "true")
        else:
            self.mqttc.publish("rpi/devices/sensors/switch/" + str(gpio), "false")

    def __init__(self, pi: pigpio.pi, mqttc: mqtt.Client, gpio):
        self.mqttc = mqttc
        self.gpio = gpio
        pi.set_glitch_filter(gpio, 300000)

        #pi.set_pull_up_down(gpio, pigpio.PUD_DOWN)

        pi.set_mode(gpio, pigpio.INPUT)
        pi.callback(gpio, pigpio.EITHER_EDGE, self.on_edge)





