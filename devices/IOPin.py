from devices.Controller import Controller
from devices.Device import Device


class IOPin(Device):
    name: str = None
    controller: Controller
