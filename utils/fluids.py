import tomli
from dataclasses import dataclass, field

from settings import TOML_DIR


@dataclass
class Fluid:
    """Properties of working fluid in the system."""
    fluid_name: str
    p: float = field(init=False, default=None)
    temp: float = field(init=False, default=None)

    def __post_init__(self):
        filename = f"{self.fluid_name}.toml"
        with open(TOML_DIR / filename, "rb") as fp:
            fl = tomli.load(fp)
        self.name = fl['name']
        self.p = fl['p']
        self.temp = fl['temp']

    def update_fluid(self):
        """Update fluid properties after p and T change in device."""
        self.p = self.p
        self.temp = self.temp
