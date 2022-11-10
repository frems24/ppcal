import tomli
from dataclasses import dataclass, field

from settings import TOML_DIR


@dataclass
class Fluid:
    """Properties of working fluid in the system."""
    process_line: str
    p: float = field(init=False, default=None)
    temp: float = field(init=False, default=None)
    m_flow: float = field(init=False, default=None)

    def __post_init__(self):
        filename = f"{self.process_line}.toml"
        with open(TOML_DIR / "fluids" / filename, "rb") as fp:
            fl = tomli.load(fp)
        self.name = fl['name']
        self.p = fl['p']
        self.temp = fl['temp']
        self.m_flow = fl['mass_flow']

        self.update_fluid()

    def update_fluid(self):
        """Update fluid properties after p and T change in device."""
        pass
