from dataclasses import dataclass, field
import tomli

from settings import TOML_DIR, PIPE_ROUGHNESS
from . import equations as eq


@dataclass
class Device:
    """Device unit to put the system together."""
    device: str = None  # Exact name of subclass (Pipe, etc.)
    type: str = None    # Exact name of type read from devices/*.toml
    name: str = None    # Descriptive name

    def update_p(self, fluid):
        raise NotImplementedError

    def update_temp(self, fluid):
        raise NotImplementedError

    def update_fluid(self, fluid):
        raise NotImplementedError


@dataclass
class Source(Device):
    entry: str = None        # Name of line's entry point
    mass_flow: float = None  # Mass stream entering the line, kg / s

    def __post_init__(self):
        self.name = "Source"
        if self.entry != "root":  # Very beginning of the whole system
            pass  # Tu wczytać mass flow z pozycji na schemacie

    def update_p(self, fluid):     # Source doesn't updates pressure
        pass

    def update_temp(self, fluid):  # Source doesn't updates temperature
        pass

    def update_fluid(self, fluid):
        fluid.m_flow = self.mass_flow
        fluid.dp = 0.0
        fluid.update_fluid()


@dataclass
class Pipe(Device):
    length: float = None  # Pipe length, m
    diameter: float = field(init=False, default=None)  # Pipe inner diameter, m
    k: float = field(init=False, default=None)  # Pipe roughness, m

    def __post_init__(self):
        self.k = PIPE_ROUGHNESS
        filename = TOML_DIR / "devices" / "pipes.toml"
        with open(filename, "rb") as fp:
            dev = tomli.load(fp)
        self.name = dev[self.type]['name']
        self.diameter = dev[self.type]['diameter']

    def update_p(self, fluid):
        eq.darcy_weisbach(self, fluid)

    def update_temp(self, fluid):
        pass

    def update_fluid(self, fluid):
        fluid.update_fluid()
