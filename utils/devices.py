from dataclasses import dataclass, field
import tomli
import json
from pathlib import Path

from .fluids import Fluid
from settings import TOML_DIR, ROUGHNESS
from . import equations as eq


@dataclass
class Device:
    """Device unit to put the system together."""
    line_filename: Path = None  # Scheme filename of process line
    position: str = None        # Position of device on system scheme
    device: str = None          # Exact name of subclass (Pipe, etc.)
    type: str = None            # Exact name of type read from devices/*.toml
    name: str = None            # Descriptive name
    length: float = None        # Length of device (if applicable)

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
                with open(self.line_filename.parent / f"{self.from_line}.json", "r") as fp:
                    fluid_description = json.load(fp)[self.entry]
            except FileNotFoundError:
                raise FileNotFoundError("Origin line should be run first.")
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
    epsilon: float = field(init=False, default=None)   # Pipe roughness, m

    def __post_init__(self):
        self.epsilon = ROUGHNESS
        filename = TOML_DIR / "devices" / "pipes.toml"
        with open(filename, "rb") as fp:
            devices = tomli.load(fp)
        self.name = devices[self.type]['name']
        self.diameter = devices[self.type]['diameter']

    def update_p(self, fluid):
        fluid.dp = eq.darcy_weisbach(self, fluid)
        fluid.p -= fluid.dp

    def update_temp(self, fluid):
        pass

    def update_fluid(self, fluid):
        fluid.update_fluid()


@dataclass
class Tee(Device):
    outflow_m: float = None  # Mass stream outflow branched connection
    diameter: float = field(init=False, default=None)  # Internal diameter, m
    epsilon: float = field(init=False, default=None)   # Roughness, m
    outflow_p: float = field(init=False, default=None)  # Outflow pressure, bar(a)
    outflow_temp: float = field(init=False, default=None)  # Outflow temp, K

    def __post_init__(self):
        self.epsilon = ROUGHNESS
        filename = TOML_DIR / "devices" / "tees.toml"
        with open(filename, "rb") as fp:
            devices = tomli.load(fp)
        self.name = devices[self.type]['name']
        self.diameter = devices[self.type]['diameter']

    def update_p(self, fluid):
        initial_fluid_p = fluid.p
        fluid.dp = eq.local_pressure_drop(self, fluid, "tee-straight")
        outflow_dp = eq.local_pressure_drop(self, fluid, "tee-branched")
        fluid.p = initial_fluid_p - fluid.dp
        self.outflow_p = initial_fluid_p - outflow_dp

    def update_temp(self, fluid):
        self.outflow_temp = fluid.temp

    def update_fluid(self, fluid):
        fluid.flow -= self.outflow_m
        fluid.update_fluid()


@dataclass
class Elbow(Device):
    diameter: float = field(init=False, default=None)  # Internal diameter, m
    epsilon: float = field(init=False, default=None)   # Roughness, m

    def __post_init__(self):
        self.epsilon = ROUGHNESS
        filename = TOML_DIR / "devices" / "elbows.toml"
        with open(filename, "rb") as fp:
            devices = tomli.load(fp)
        self.name = devices[self.type]['name']
        self.diameter = devices[self.type]['diameter']

    def update_p(self, fluid):
        fluid.dp = eq.local_pressure_drop(self, fluid, "elbow")
        fluid.p -= fluid.dp

    def update_temp(self, fluid):
        pass

    def update_fluid(self, fluid):
        fluid.update_fluid()

