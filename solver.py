from utils.system import Scheme
from utils.fluids import Fluid


class Solver:
    """A class to calculating changes in fluid properties in the system."""
    def __init__(self, scheme: Scheme, fluid: Fluid):
        self.scheme = scheme
        self.fluid = fluid
        self.route = None

    def get_route(self):
        return self.scheme.make_route()

    def run(self):
        """Method to perform calculations and get fluid instance at the end of system."""
        self.route = self.get_route()
        for device in self.route:
            self.fluid = device(self.fluid).get_fluid_after()
        return self.fluid


if __name__ == "__main__":
    sh = Scheme(scheme=["Pipe25", "Pipe50", "Pipe25"])
    fl = Fluid(name="He", p=3.0)
    s = Solver(sh, fl)
    f = s.run()
    print(f"Pressure: {f.p} bar(a)")
