import sys
import tomli

from settings import BASE_DIR
from utils.system import Scheme
from utils.fluids import Fluid
from utils.devices import Device, Tee
from utils.data_io import (write_data_row, save_data,
                           write_outflow_data, save_outflows_scheme)


class Solver:
    """A class to calculating changes in fluid properties in the system line."""
    def __init__(self, process_line: str, props_pkg: str = "coolprop"):
        self.process_line_name: str = process_line
        self.props_pkg: str = props_pkg
        self.route: list[Device] = Scheme(self.process_line_name).make_route()
        self.fluid = None
        self.data: list[dict] = []
        self.outflows: dict = {}

    def initiate_fluid(self) -> Fluid:
        source = self.route[0]
        return source.get_fluid(self.props_pkg)

    def run(self):
        """Method to perform calculations and get fluid instance at the end of system line."""
        if len(self.route) == 0:
            raise RuntimeError(f"Empty scheme: '{self.process_line_name}'. Nothing to solve.")
        self.fluid = self.initiate_fluid()
        for device in self.route:
            device.update_p(self.fluid)
            device.update_temp(self.fluid)
            device.update_fluid(self.fluid)
            if isinstance(device, Tee):
                self.outflows[device.position] = write_outflow_data(device, self.fluid)
            self.data.append(write_data_row(device, self.fluid))

        save_data(self.process_line_name, self.data)
        if self.outflows:
            save_outflows_scheme(self.process_line_name, self.outflows)
        return self.fluid


class Runner:
    """A class to organize entire system and run calculations for every process line."""
    def __init__(self, system_name: str):
        self.system_name: str = system_name
        self.schemes_dir: str = ""
        self.engine: str = ""
        self.process_lines: list[Solver] = []

    def read_process_lines(self):
        filename = BASE_DIR / self.system_name
        with open(filename, 'rb') as fp:
            system_description = tomli.load(fp)
        self.schemes_dir = system_description['schemes_dir']
        self.engine = system_description.get('engine', 'coolprop')
        process_lines_order = system_description['process_lines_order']

        for process_line_name in process_lines_order:
            line = Solver(process_line=f"{self.schemes_dir}/{process_line_name}", props_pkg=self.engine)
            self.process_lines.append(line)

    def execute(self, verbose=False):
        self.read_process_lines()
        for line in self.process_lines:
            line.run()
            if verbose:
                print(f"{line.process_line_name}.. Done")


if __name__ == "__main__":
    r = Runner(sys.argv[1])
    r.execute(verbose=True)
