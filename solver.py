from utils.system import Scheme
from utils.fluids import Fluid


class Solver:
    """A class to calculating changes in fluid properties in the system."""
    def __init__(self, scheme_name: str, fluid_name: str):
        self.scheme_name = scheme_name
        self.fluid_name = fluid_name
        self.fluid = Fluid(fluid_name=fluid_name)
        self.route = None

    def get_route(self):
        return Scheme(self.scheme_name).make_route()

    def run(self):
        """Method to perform calculations and get fluid instance at the end of system."""
        self.route = self.get_route()
        for device in self.route:
            device.update_p(self.fluid)
            device.update_temp(self.fluid)
            self.fluid.update_fluid()
        return self.fluid


if __name__ == "__main__":
    fl = Fluid(fluid_name="he_at_3bar")
    print(f"Pressure at start: {fl.p} bar(a)")
    s = Solver(scheme_name="three_pipes", fluid_name="he_at_3bar")
    f = s.run()
    print(f"Pressure at end:   {f.p} bar(a)")
