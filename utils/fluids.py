from dataclasses import dataclass


@dataclass
class Fluid:
    """Properties of working fluid in the system."""
    name: str
    p: float
