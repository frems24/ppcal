import tomli
from dataclasses import dataclass, field

from settings import TOML_DIR


@dataclass
class Fluid:
    """Properties of working fluid in the system."""
    process_line: str
    m_flow: float = field(init=False, default=None)
    p: float = field(init=False, default=None)
    temp: float = field(init=False, default=None)
    rho: float = field(init=False, default=None)

    def __post_init__(self):
        filename = f"{self.process_line}.toml"
        with open(TOML_DIR / "fluids" / filename, "rb") as fp:
            fl = tomli.load(fp)
        self.name = fl['name']
        self.p = fl['p']
        self.temp = fl['temp']

    def update_fluid(self):  # Temporary implementation
        """Update fluid properties."""
        self.rho = 0.1785  # kg / m3
