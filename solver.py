from utils.system import Scheme
from utils.fluids import Fluid


class Solver:
    """A class to calculating changes in fluid properties in the system."""
    def __init__(self, scheme_name: str, fluid: Fluid):
        self.scheme_name = scheme_name
        self.fluid = fluid
        self.route = None

    def get_route(self):
        return Scheme(self.scheme_name).make_route()

    def run(self):
        """Method to perform calculations and get fluid instance at the end of system."""
        self.route = self.get_route()
        for device in self.route:
            self.fluid = device(self.fluid).get_fluid_after()
        return self.fluid


if __name__ == "__main__":
    fl = Fluid(name="He", p=3.0)
    print(f"Pressure at start: {fl.p} bar(a)")
    s = Solver(scheme_name="three_pipes", fluid=fl)
    f = s.run()
    print(f"Pressure at end:   {f.p} bar(a)")
