from dataclasses import dataclass


@dataclass
class Fluid:
    p: float = 1
    name: str = "He"
