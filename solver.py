from utils.system import Scheme
from utils.fluids import Fluid
from utils.devices import Device, Tee
from utils.data_io import (write_data_row, save_data,
                           write_outflow_data, save_outflows_scheme)


class Solver:
    """A class to calculating changes in fluid properties in the system."""
    def __init__(self, process_name: str):
        self.process_name = process_name
        self.route: list[Device] = Scheme(self.process_name).make_route()
        self.fluid: Fluid = self.initiate_fluid()
        self.data: list[dict] = []
        self.outflows: dict = {}

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
            if isinstance(device, Tee):
                self.outflows[device.position] = write_outflow_data(device, self.fluid)
            self.data.append(write_data_row(device, self.fluid))

        save_data(self.process_name, self.data)
        save_outflows_scheme(self.process_name, self.outflows)
        return self.fluid


if __name__ == "__main__":
    process_line_name = "m_4_5_K_sup"
    s = Solver(process_name=process_line_name)
    f = s.run()
    print(f"Pressure at end:   {f.p} bar(a)")
