from typing import List

from utils.system import Scheme
from utils.fluids import Fluid
from utils.devices import Device
from utils.solver_data import save_data, write_data


class Solver:
    """A class to calculating changes in fluid properties in the system."""
    def __init__(self, process_name: str):
        self.process_name = process_name
        self.data: list[dict] = []
        self.route: list[Device] = Scheme(self.process_name).make_route()
        self.fluid: Fluid = self.initiate_fluid()

    def initiate_fluid(self) -> Fluid:
        source = self.route[0]
        return source.get_fluid()

    def run(self):
        """Method to perform calculations and get fluid instance at the end of system."""
        if len(self.route) == 0:
            raise RuntimeError(f"Empty scheme: '{self.process_name}'. Nothing to solve.")
        for device in self.route:
            device.update_p(self.fluid)
            device.update_temp(self.fluid)
            device.update_fluid(self.fluid)
            write_data(self.data, device, self.fluid)
        save_data(self.process_name, self.data)
        return self.fluid


if __name__ == "__main__":
    process_line_name = "m_4_5_K_sup"
    s = Solver(process_name=process_line_name)
    f = s.run()
    print(f"Pressure at end:   {f.p} bar(a)")
