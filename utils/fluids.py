from dataclasses import dataclass, field


@dataclass
class Fluid:
    """Properties of working fluid in the system."""
    fluid_name: str  # Fluid name
    p: float         # Pressure, bar(a)
    temp: float      # Temperature, K
    flow: float      # Mass flow, kg / s
    rho: float = field(init=False, default=None)      # Density, kg/m3
    mi: float = field(init=False, default=None)       # Dynamic viscosity, Pa s
    kappa: float = field(init=False, default=None)    # Specific heat ratio CP/cv
    dp: float = field(init=False, default=0.0)        # Pressure drop in device, bar
    dp_total: float = field(init=False, default=0.0)  # Cumulative pressure drop at the end of process line, bar
