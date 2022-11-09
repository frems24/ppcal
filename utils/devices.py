from dataclasses import dataclass
import tomli

from settings import TOML_DIR


@dataclass
class Device:
    """Device unit to put the system together."""
    device: str = None  # Exact name of subclass (Pipe, etc.)
    type: str = None  # Exact name of type read from devices/*.toml
    name: str = None  # Descriptive name

    def update_p(self, fluid):
        raise NotImplementedError

    def update_temp(self, fluid):
        raise NotImplementedError


@dataclass
class Pipe(Device):
    diameter: float = None
    length: float = None
    dp: float = None  # Temporary line

    def __post_init__(self):
        filename = TOML_DIR / "devices" / "pipes.toml"
        with open(filename, "rb") as fp:
            dev = tomli.load(fp)
        self.name = dev[self.type]['name']
        self.diameter = dev[self.type]['diameter']
        self.dp = dev[self.type]['dp']  # Temporary line

    def update_p(self, fluid):
        fluid.p -= self.dp

    def update_temp(self, fluid):
        pass
