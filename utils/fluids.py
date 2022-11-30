from dataclasses import dataclass, field
from typing import Any


@dataclass
class Fluid:
    """Properties of working fluid in the system."""
    fluid_name: str  # Fluid name
    p: float         # Pressure, bar(a)
    temp: float      # Temperature, K
    flow: float      # Mass flow, kg / s
    props_pkg: str   # Properties calculation package ('coolprop', 'hepak')
    rho: float = field(init=False, default=None)     # Density, kg/m3
    mi: float = field(init=False, default=None)      # Dynamic viscosity, Pa s
    kappa: float = field(init=False, default=None)   # Specific heat ratio CP/cv
    dp: float = field(init=False, default=None)      # Pressure drop in device, bar
    dp_total: float = field(init=False, default=0)   # Cumulative pressure drop at the end of process line, bar
    engine: Any = field(init=False, default=None)    # fluid properties calculation module

    def __post_init__(self):
        if self.props_pkg == "coolprop":
            from . import coolprop
            self.engine = coolprop
        elif self.props_pkg == "hepak":
            from . import hepak
            self.engine = hepak
        else:
            raise ValueError("Only 'CoolProp' or 'HePak' are allowed to calculate fluid properties.")

    def update_fluid(self):
        """Update fluid properties: rho, mi, kappa."""
        self.engine.update_fluid_props(self)
