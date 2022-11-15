from dataclasses import dataclass, field
import tomli
import json

from .fluids import Fluid
from settings import TOML_DIR, SCHEMES_DIR, PIPE_ROUGHNESS
from . import equations as eq


@dataclass
class Device:
    """Device unit to put the system together."""
    position: str = None  # Position of device on system scheme
    device: str = None    # Exact name of subclass (Pipe, etc.)
    type: str = None      # Exact name of type read from devices/*.toml
    name: str = None      # Descriptive name
    length: float = None  # Length of device (if applicable)

    def get_fluid(self):
        pass

    def update_p(self, fluid):
        raise NotImplementedError

    def update_temp(self, fluid):
        raise NotImplementedError

    def update_fluid(self, fluid):
        raise NotImplementedError


@dataclass
class Source(Device):
    from_line: str = None    # Get fluid from other line name (from the very beginning if 'root')
    entry: str = None        # Name of line's entry point

    def __post_init__(self):
        self.name = "Source"

    def get_fluid(self) -> Fluid:
        if self.from_line == "root":  # From very beginning of the whole system
            filename = f"{self.entry}.toml"
            with open(TOML_DIR / "fluids" / filename, "rb") as fp:
                fluid_description = tomli.load(fp)
            return Fluid(**fluid_description)
        else:                         # From tee
            try:
                with open(SCHEMES_DIR / f"{self.from_line}.json", "r") as fp:
                    line_description = json.load(fp)
            except FileNotFoundError as desc:
                raise FileNotFoundError("Origin line should be run first.")
            entry_description = line_description[self.entry]
            fluid_description = dict()
            fluid_description['fluid_name'] = entry_description['fluid_name']
            fluid_description['p'] = entry_description['pressure']
            fluid_description['temp'] = entry_description['temperature']
            fluid_description['flow'] = entry_description['outflow']
            return Fluid(**fluid_description)

    def update_p(self, fluid):     # Source doesn't updates pressure
        pass

    def update_temp(self, fluid):  # Source doesn't updates temperature
        pass

    def update_fluid(self, fluid):
        fluid.dp = 0.0
        fluid.update_fluid()


@dataclass
class Pipe(Device):
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


@dataclass
class Tee(Device):
    outflow: float = None

    def __post_init__(self):
        self.name = "T-connection"

    def update_p(self, fluid):
        fluid.dp = 0

    def update_temp(self, fluid):
        pass

    def update_fluid(self, fluid):
        fluid.flow -= self.outflow
        fluid.update_fluid()
