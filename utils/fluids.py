import tomli
from dataclasses import dataclass

from settings import TOML_DIR


@dataclass
class Fluid:
    """Properties of working fluid in the system."""
    fluid_name: str

    def __post_init__(self):
        filename = f"{self.fluid_name}.toml"
        with open(TOML_DIR / filename, "rb") as fp:
            fl = tomli.load(fp)
        self.name = fl['name']
        self.p = fl['p']
