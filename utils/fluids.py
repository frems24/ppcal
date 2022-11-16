from dataclasses import dataclass, field


@dataclass
class Fluid:
    """Properties of working fluid in the system."""
    fluid_name: str  # Fluid name
    p: float         # Pressure, bar(a)
    temp: float      # Temperature, K
    flow: float      # Mass flow, kg / s
    rho: float = field(init=False, default=None)     # Density, kg / m3
    mi: float = field(init=False, default=None)      # Dynamic viscosity, Pa s
    dp: float = field(init=False, default=None)      # Pressure drop in device, bar

    def update_fluid(self):  # Temporary implementation
        """Update fluid properties."""
        self.rho = 129.1
        self.mi = 3.5e-6
