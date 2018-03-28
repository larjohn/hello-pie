class AbstractGPIO:
    local_name = None

    def on(self):
        raise NotImplementedError

    def off(self):
        raise NotImplementedError

    def set_mode(self, mode):
        raise NotImplementedError

    def write(self, value):
        raise NotImplementedError
