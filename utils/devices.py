from dataclasses import dataclass


@dataclass
class Device:
    """Device unit to put the system together."""
    type: str = None
    length: float = 0

    def update_p(self, fluid):
        raise NotImplementedError

    def update_temp(self, fluid):
        raise NotImplementedError


@dataclass
class Pipe(Device):
    name: str = None
    dp: float = None

    def __post_init__(self):
        if self.name == 'Pipe DN20':
            self.dp = 1.0
        elif self.name == 'Pipe DN50':
            self.dp = 0.5
        else:
            raise ValueError("Unknown pipe type")

    def update_p(self, fluid):
        fluid.p -= self.dp

    def update_temp(self, fluid):
        pass
