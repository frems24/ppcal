from dataclasses import dataclass, field
from typing import Callable
from pathlib import Path
import tomllib
import json

from .fluids import Fluid
import settings
from settings import DEVICES_DIR
from . import equations as eq


@dataclass
class Device:
    """Device unit to put the system together."""
    line_filename: Path = None  # Scheme filename of process line
    direction: str = 'forward'  # Direction of calculation relative to mass flow
    calculate: Callable[[float, float], float] = None  # Function to add or subtract parameter
    position: str = None        # Position of device on system scheme
    device: str = None          # Exact name of subclass (Pipe, etc.)
    type: str = None            # Exact name of type read from devices/*.toml
    name: str = None            # Descriptive name
    length: float = None        # Length of device, m (if applicable)
    bell_l: float = 0           # Expansion bellows length, m (if applicable)
    number: int = field(init=False, default=1)  # Number of units (elbows only)

    def get_fluid(self):
        pass

    def update_p(self, fluid):
        raise NotImplementedError

    def update_temp(self, fluid):
        raise NotImplementedError


@dataclass
class Source(Device):
    from_line: str = None    # Get fluid from other line name (from the very beginning if 'root')
    entry: str = None        # Name of line's entry point

    def __post_init__(self):
        self.name = "Source"

    def get_fluid(self) -> Fluid:
        """
        Get fluid instance from fluid file or from tee outflow.
        :return: Fluid instance
        """
        if self.from_line == "root":  # From very beginning of the process line
            if self.entry[:2] != "f-":
                raise ValueError("Name of fluid description file should start with 'f-'.")
            filename = self.line_filename.parent / f"{self.entry}.toml"
            with open(filename, "rb") as fp:
                fluid_description = tomllib.load(fp)
        else:  # From tee outflow
            try:
                with open(self.line_filename.parent / f"{self.from_line}.json", "r") as fp:
                    fluid_description = json.load(fp)[self.entry]
            except FileNotFoundError:
                print("Origin line should be run first.")
                raise

        return Fluid(**fluid_description)

    def update_p(self, fluid):     # Source doesn't updates pressure
        pass

    def update_temp(self, fluid):  # Source doesn't updates temperature
        pass


@dataclass
class Pipe(Device):
    diameter: float = field(init=False, default=None)  # Pipe inner diameter, m
    epsilon: float = field(init=False, default=None)   # Pipe roughness, m

    def __post_init__(self):
        self.epsilon = settings.ROUGHNESS
        filename = DEVICES_DIR / "pipes.toml"
        with open(filename, "rb") as fp:
            devices = tomllib.load(fp)
        self.name = devices[self.type]['name']
        self.diameter = devices[self.type]['diameter']
        if self.bell_l > 0:
            self.length += self.bell_l
            self.name += " bellows"

    def update_p(self, fluid):
        fluid.dp = eq.darcy_weisbach(self, fluid)
        new_p = self.calculate(fluid.p, fluid.dp)
        fluid.p = new_p

    def update_temp(self, fluid):
        pass


@dataclass
class Tee(Device):
    outflow_m: float = None  # Mass stream outflow branched connection
    diameter: float = field(init=False, default=None)  # Internal diameter, m
    epsilon: float = field(init=False, default=None)   # Roughness, m

    def __post_init__(self):
        self.epsilon = settings.ROUGHNESS
        filename = DEVICES_DIR / "tees.toml"
        with open(filename, "rb") as fp:
            devices = tomllib.load(fp)
        self.name = devices[self.type]['name']
        self.diameter = devices[self.type]['diameter']

    def update_p(self, fluid):
        fluid.dp = eq.local_pressure_drop(self, fluid, "tee-straight")
        new_p = self.calculate(fluid.p, fluid.dp)
        fluid.p = new_p

    def update_branched_p(self, branched_fluid):
        branched_fluid.dp = eq.local_pressure_drop(self, branched_fluid, "tee-branched")
        new_p = self.calculate(branched_fluid.p, branched_fluid.dp)
        branched_fluid.p = new_p

    def update_temp(self, fluid):
        pass

    def update_branched_temp(self, fluid):
        pass


@dataclass
class Elbow(Device):
    diameter: float = field(init=False, default=None)  # Internal diameter, m
    epsilon: float = field(init=False, default=None)   # Roughness, m
    number: int = 1                                    # Number of elbows

    def __post_init__(self):
        self.epsilon = settings.ROUGHNESS
        filename = DEVICES_DIR / "elbows.toml"
        with open(filename, "rb") as fp:
            devices = tomllib.load(fp)
        self.name = devices[self.type]['name']
        self.diameter = devices[self.type]['diameter']

    def update_p(self, fluid):
        fluid.dp = eq.local_pressure_drop(self, fluid, "elbow") * self.number
        new_p = self.calculate(fluid.p, fluid.dp)
        fluid.p = new_p

    def update_temp(self, fluid):
        pass


@dataclass
class Valve(Device):
    kv: float = field(init=False, default=None)
    n6: float = field(init=False, default=None)
    xt: float = field(init=False, default=None)

    def __post_init__(self):
        self.n6 = settings.N6
        self.xt = settings.X_T
        filename = DEVICES_DIR / "valves.toml"
        with open(filename, "rb") as fp:
            valves = tomllib.load(fp)
        self.name = valves[self.type]['name']
        self.kv = valves[self.type]['kv'] * settings.VALVE_OPENING

    def update_p(self, fluid):
        fluid.dp = eq.valve_pressure_drop(self, fluid)
        new_p = self.calculate(fluid.p, fluid.dp)
        fluid.p = new_p

    def update_temp(self, fluid):
        pass
