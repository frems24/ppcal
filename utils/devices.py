from dataclasses import dataclass

from .fluids import Fluid


@dataclass
class Device:
    """Device unit to put the system together."""

    def get_fluid_after(self, fluid):
        raise NotImplementedError


@dataclass
class Pipe20(Device):
    name: str = "Pipe DN20"
    length: float = 0
    dp: float = 1.0

    def get_fluid_after(self, fluid):
        fluid.p -= self.dp
        return fluid


@dataclass
class Pipe50(Device):
    name: str = "Pipe DN50"
    length: float = 0
    dp: float = 0.5

    def get_fluid_after(self, fluid):
        fluid.p -= self.dp
        return fluid
