import tomli
from dataclasses import dataclass, field

from settings import TOML_DIR


@dataclass
class Fluid:
    """Properties of working fluid in the system."""
    fluid_name: str
    name: str = field(init=False)
    p: float = field(init=False)

    def __post_init__(self):
        filename = f"{self.fluid_name}.toml"
        with open(TOML_DIR / filename, "rb") as fp:
            fl = tomli.load(fp)['fluid']
        self.name = fl['name']
        self.p = fl['p']
