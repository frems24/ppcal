from CoolProp import CoolProp as CP


def update_fluid_props(fluid):
    fluid_p_pa = fluid.p * 100_000  # bar -> Pa
    fluid.rho = CP.PropsSI('D', 'T', fluid.temp, 'P', fluid_p_pa, 'He')  # Density, kg/m3
    fluid.mi = CP.PropsSI('V', 'T', fluid.temp, 'P', fluid_p_pa, 'He')  # Dynamic viscosity, Pa s
    c_p = CP.PropsSI('C', 'T', fluid.temp, 'P', fluid_p_pa, 'He')  # Cp, J/kg/K
    c_v = CP.PropsSI('O', 'T', fluid.temp, 'P', fluid_p_pa, 'He')  # Cv, J/kg/K
    fluid.kappa = c_p / c_v  # Specific heat ratio
