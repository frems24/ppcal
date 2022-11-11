import math


def darcy_weisbach(device, fl):
    dp = dzeta_pipe(device, fl) * 8 * fl.m_flow**2 / (math.pi**2 * device.diameter**4 * fl.rho)
    return dp


def dzeta_pipe(device, fl):
    return 0.00001
