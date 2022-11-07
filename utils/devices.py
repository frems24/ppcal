from dataclasses import dataclass

from .fluids import Fluid


@dataclass
class Device:
    """Device unit to put the system together."""
    fluid: Fluid
    name: str = ""
    dp: float = 0.0

    def get_fluid_after(self):
        raise NotImplementedError


@dataclass
class Pipe25(Device):
    name: str = "Pipe DN25"
    dp: float = 0.5

    def get_fluid_after(self):
        self.fluid.p -= self.dp
        return self.fluid
