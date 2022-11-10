from utils.system import Scheme
from utils.fluids import Fluid


class Solver:
    """A class to calculating changes in fluid properties in the system."""
    def __init__(self, process_line: str):
        self.route = Scheme(process_line=process_line).make_route()
        self.fluid = Fluid(process_line=process_line)

    def run(self):
        """Method to perform calculations and get fluid instance at the end of system."""
        for device in self.route:
            device.update_p(self.fluid)
            device.update_temp(self.fluid)
            self.fluid.update_fluid()
        return self.fluid


if __name__ == "__main__":
    process_line = "m_4_5_K_sup"
    fl = Fluid(process_line=process_line)
    print(f"Pressure at start: {fl.p} bar(a)")
    s = Solver(process_line=process_line)
    f = s.run()
    print(f"Pressure at end:   {f.p} bar(a)")
