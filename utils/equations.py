import math

# Pipes


def darcy_weisbach(dev, fl) -> float:
    """
    Calculate pressure drop with Darcy-Weisbach equation.
    :param dev: Device class instance
    :param fl: Fluid class instance
    :return: Pressure drop, bar
    """
    nominator = dzeta_pipe(dev, fl) * 8 * (fl.flow ** 2)
    denominator = (math.pi ** 2) * (dev.diameter ** 4) * fl.rho
    p_drop_pa = nominator / denominator  # Pa
    p_drop_bar = p_drop_pa / 100_000     # bar
    return p_drop_bar


def dzeta_pipe(dev, fl) -> float:
    """Local pressure drop coefficient, dimensionless."""
    return (lambda_coefficient(dev, fl) * dev.length) / dev.diameter


def lambda_coefficient(dev, fl) -> float:
    """Linear pressure drop coefficient, dimensionless."""
    re = reynolds(dev, fl)
    denominator_inner = (dev.epsilon / (3.7 * dev.diameter)) ** 1.11 + (6.9 / re)
    denominator = (-1.8 * math.log10(denominator_inner)) ** 2
    return 1 / denominator


def reynolds(dev, fl) -> float:
    """Calculate the Reynolds number, dimensionless."""
    return (fl.rho * fluid_velocity(dev, fl) * dev.diameter) / fl.mi


def fluid_velocity(dev, fl) -> float:
    """Calculate the fluid velocity in the circular pipe, m / s."""
    denominator = math.pi * ((dev.diameter ** 2) / 4) * fl.rho
    return fl.flow / denominator

# Flexible hose

# Elbow and T-joint


def local_pressure_drop(dev, fl, mode: str) -> float:
    p_drop_pa = 0.5 * fl.rho * dzeta_local(dev, mode) * (fluid_velocity(dev, fl) ** 2)
    p_drop_bar = p_drop_pa / 100_000     # bar
    return p_drop_bar


def dzeta_local(dev, mode: str) -> float:
    if mode == "elbow":
        return 20 * ft(dev)
    elif mode == "tee-straight":
        return 20 * ft(dev)
    elif mode == "tee-branched":
        return 60 * ft(dev)
    else:
        raise ValueError("Not recognized device for dzeta_local.")


def ft(dev) -> float:
    denominator_inner = dev.epsilon / (3.7 * dev.diameter)
    denominator = math.log10(denominator_inner) ** 2
    return 0.25 / denominator
