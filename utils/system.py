import tomli
from operator import add, sub

from settings import SYSTEMS_DIR
from . import devices


class Scheme:
    """Scheme of the whole system."""
    def __init__(self, process_line: str):
        self.process_line = process_line
        self.route: list[devices.Device] = []

    def make_route(self):
        """Make a list of devices connected together in the system."""
        filename = SYSTEMS_DIR / f"{self.process_line}.toml"
        with open(filename, mode="rb") as fp:
            scheme_toml = tomli.load(fp)

        positions = list(scheme_toml)
        direction_desc = scheme_toml['START'].get('direction', 'forward')
        if direction_desc == 'forward':
            calculate = sub
        elif direction_desc == 'reverse':
            calculate = add
        else:
            raise ValueError("Source direction parameter can be only 'forward' or 'reverse'.")

        for position in positions:
            description = scheme_toml[position]
            description['line_filename'] = filename
            description['position'] = position
            description['calculate'] = calculate
            device = getattr(devices, description['device'])(**description)
            self.route.append(device)

        return self.route
