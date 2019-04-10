class AbstractGPIOGroup:
    local_name = None

    def set_step(self, bits):
        raise NotImplementedError

