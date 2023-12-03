import sys
import tomllib
from copy import deepcopy

from settings import BASE_DIR
from utils.system import Scheme
from utils.fluids import Fluid
from utils.devices import Device, Tee
from utils.data_io import (write_data_row, save_data,
                           write_outflow_data, save_outflows_scheme)


class Solver:
    """
    A class to calculate fluid parameters in the process line.
    """
    def __init__(self, process_line: str, engine, update_fluid: bool = True):
        self.process_line_name: str = process_line
        self.engine = engine
        self.route: list[Device] = []
        self.fluid = None
        self.branched_fluid = None
        self.update_fluid = update_fluid
        self.data: list[dict] = []
        self.outflows: dict = {}

        self.initiate_route()

    def initiate_route(self):
        """
        Initiate a list of particular Device instances read from process line description file.
        """
        self.route = Scheme(self.process_line_name).make_route()

    def get_fluid(self) -> Fluid:
        """
        Get fluid instance from source device (very beginning of the process line or outflow from tee).
        :return: Fluid instance
        """
        source = self.route[0]
        return source.get_fluid()

    def run(self):
        """
        Perform calculations and update fluid properties in current process line.
        :return: Calculated fluid instance at the end of process line (for testing purposes only).
        """
        if len(self.route) == 0:
            raise RuntimeError(f"Empty scheme: '{self.process_line_name}'. Nothing to solve.")
        self.fluid = self.get_fluid()
        self.engine.update_fluid_props(self.fluid)

        for device in self.route:
            # In a Tee update main and branched mass flow and calculate branched properties
            if isinstance(device, Tee):
                self.branched_fluid = deepcopy(self.fluid)
                self.fluid.flow -= device.outflow_m
                self.branched_fluid.flow = device.outflow_m
                device.update_branched_p(self.branched_fluid)
                device.update_branched_temp(self.branched_fluid)
                self.outflows[device.position] = write_outflow_data(self.branched_fluid)

            # Calculate main flow properties in all devices
            device.update_p(self.fluid)
            device.update_temp(self.fluid)
            if self.update_fluid:
                self.engine.update_fluid_props(self.fluid)
            self.fluid.dp_total += self.fluid.dp
            self.data.append(write_data_row(device, self.fluid))

        # Save to disk fluid properties in each device and outflow data from each Tee device
        save_data(self.process_line_name, self.data)
        if self.outflows:
            save_outflows_scheme(self.process_line_name, self.outflows)

        return self.fluid


class Runner:
    """A class to organize entire system and run calculations for every process line."""
    def __init__(self, system_name: str):
        self.system_name: str = system_name    # name of system description file
        self.schemes_dir: str = ""             # name of the folder with process lines descriptions
        self.props_pkg: str = ""               # fluid properties calculation package name
        self.engine = None                     # fluid properties calculation module
        self.update_fluid = True               # if true, recalculate fluid properties in every device
        self.process_lines: list[Solver] = []  # a list with all process lines description

    def read_process_lines(self):
        """Read system description file and form a list with Solver instances for each process line."""
        filename = BASE_DIR / self.system_name
        try:
            with open(filename, 'rb') as fp:
                system_description = tomllib.load(fp)
        except FileNotFoundError as e:
            print(f"File Not Found Error: {filename}")
            sys.exit()

        try:
            self.schemes_dir = system_description['schemes_dir']
        except KeyError as e:
            print(f"{e!r}. You should provide name of directory containing system description in schemes_dir section.")
            sys.exit()

        try:
            process_lines_order = system_description['process_lines_order']
        except KeyError as e:
            print(f"{e!r}. You should complete a process_lines_order section.")
            sys.exit()

        if not isinstance(process_lines_order, list):
            print("process_lines_order section should be a list")
            sys.exit()
        elif len(process_lines_order) == 0:
            print("Empty process_lines_order section. Nothing to compute.")

        self.props_pkg = system_description.get('engine', 'coolprop')
        self.update_fluid = system_description.get('update_fluid', True)

        if self.props_pkg == "coolprop":
            from utils import coolprop
            self.engine = coolprop
        elif self.props_pkg == "hepak":
            from utils import hepak
            self.engine = hepak
        else:
            raise ValueError("Only 'CoolProp' or 'HePak' are allowed "
                             "to calculate fluid properties.")

        for process_line_name in process_lines_order:
            line = Solver(process_line=f"{self.schemes_dir}/{process_line_name}",
                          engine=self.engine,
                          update_fluid=self.update_fluid)
            self.process_lines.append(line)

    def execute(self, verbose=False):
        """
        Get a list with all process lines and run calculations for each of them.
        :param verbose: If True, print progres status for each process line.
        """
        self.read_process_lines()
        for process_line in self.process_lines:
            process_line.run()
            if verbose:
                print(f"{process_line.process_line_name}.. Done")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide system filename (sys/...)")
        sys.exit()
    else:
        r = Runner(sys.argv[1])
        r.execute(verbose=True)
