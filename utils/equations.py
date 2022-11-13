import math


def darcy_weisbach(dev, fl) -> float:
    """
    Calculate pressure drop with Darcy-Weisbach equation.
    :param dev: Device class instance
    :param fl: Fluid class instance
    :return: Pressure drop, bar
    """
    nominator = dzeta_pipe(dev, fl) * 8 * (fl.m_flow ** 2)
    denominator = (math.pi ** 2) * (dev.diameter ** 4) * fl.rho
    dp = nominator / denominator  # Pa
    dp_bar = dp / 100_000         # bar
    return dp_bar


def dzeta_pipe(dev, fl) -> float:
    """Local pressure drop coefficient, dimensionless."""
    return (lambda_coefficient(dev, fl) * dev.length) / dev.diameter


def lambda_coefficient(dev, fl):
    """Linear pressure drop coefficient, dimensionless."""
    re = reynolds(dev, fl)
    denominator_inner = (dev.k / (3.7 * dev.diameter)) ** 1.11 + (6.9 / re)
    denominator = (-1.8 * math.log10(denominator_inner)) ** 2
    return 1 / denominator


def reynolds(dev, fl):
    """Calculate the Reynolds number, dimensionless."""
    return (fl.rho * fluid_velocity(dev, fl) * dev.diameter) / fl.mi


def fluid_velocity(dev, fl):
    """Calculate the fluid velocity in the circular pipe, m / s."""
    denominator = math.pi * ((dev.diameter ** 2) / 4) * fl.rho
    return fl.m_flow / denominator
