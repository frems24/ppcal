from dataclasses import dataclass
import tomli

from settings import TOML_DIR
from . import equations as eq


@dataclass
class Device:
    """Device unit to put the system together."""
    device: str = None  # Exact name of subclass (Pipe, etc.)
    type: str = None  # Exact name of type read from devices/*.toml
    name: str = None  # Descriptive name

    def update_fluid(self, fluid):
        raise NotImplementedError

    def update_p(self, fluid):
        raise NotImplementedError

    def update_temp(self, fluid):
        raise NotImplementedError


@dataclass
class Source(Device):
    entry: str = None
    mass_flow: float = 0

    def __post_init__(self):
        if self.entry != "root":
            pass  # Tu wczytać mass flow z pozycji na schemacie

    def update_fluid(self, fluid):
        fluid.m_flow = self.mass_flow
        fluid.update_fluid()

    def update_p(self, fluid):     # Source doesn't updates pressure
        pass

    def update_temp(self, fluid):  # Source doesn't updates temperature
        pass


@dataclass
class Pipe(Device):
    diameter: float = None
    length: float = None

    def __post_init__(self):
        filename = TOML_DIR / "devices" / "pipes.toml"
        with open(filename, "rb") as fp:
            dev = tomli.load(fp)
        self.name = dev[self.type]['name']
        self.diameter = dev[self.type]['diameter']

    def update_fluid(self, fluid):
        fluid.update_fluid()

    def update_p(self, fluid):
        dp = eq.darcy_weisbach(self, fluid)
        fluid.p -= dp

    def update_temp(self, fluid):
        pass
