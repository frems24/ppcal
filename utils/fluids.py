import tomli
from dataclasses import dataclass, field

from settings import TOML_DIR


@dataclass
class Fluid:
    """Properties of working fluid in the system."""
    process_line: str
    m_flow: float = field(init=False, default=None)  # Mass flow, kg / s
    p: float = field(init=False, default=None)       # Pressure, bar(a)
    temp: float = field(init=False, default=None)    # Temperature, K
    rho: float = field(init=False, default=None)     # Density, kg / m3
    mi: float = field(init=False, default=None)      # Dynamic viscosity, Pa s
    dp: float = field(init=False, default=None)      # Pressure drop in device, bar

    def __post_init__(self):
        filename = f"{self.process_line}.toml"
        with open(TOML_DIR / "fluids" / filename, "rb") as fp:
            fl = tomli.load(fp)
        self.name = fl['name']
        self.p = fl['p']
        self.temp = fl['temp']

    def update_fluid(self):  # Temporary implementation
        """Update fluid properties."""
        self.rho = 129.1
        self.mi = 3.5e-6
