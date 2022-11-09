from dataclasses import dataclass


@dataclass
class Device:
    """Device unit to put the system together."""
    type: str = ""
    length: float = 0

    def update_p(self, fluid):
        raise NotImplementedError

    def update_temp(self, fluid):
        raise NotImplementedError


@dataclass
class Pipe20(Device):
    name: str = "Pipe DN20"
    dp: float = 1.0

    def update_p(self, fluid):
        fluid.p -= self.dp

    def update_temp(self, fluid):
        pass


@dataclass
class Pipe50(Device):
    name: str = "Pipe DN50"
    dp: float = 0.5

    def update_p(self, fluid):
        fluid.p -= self.dp

    def update_temp(self, fluid):
        pass
