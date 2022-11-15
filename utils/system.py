import tomli

from settings import TOML_DIR
from . import devices


class Scheme:
    """Scheme of the whole system."""
    def __init__(self, process_line: str):
        self.process_line = process_line
        self.route = []

    def make_route(self):
        """Make a list of devices connected together in the system."""
        filename = f"{self.process_line}.toml"
        with open(TOML_DIR / "schemes" / filename, mode="rb") as fp:
            scheme_toml = tomli.load(fp)

        positions = list(scheme_toml)

        for position in positions:
            description = scheme_toml[position]
            description['position'] = position
            device = getattr(devices, description['device'])(**description)
            self.route.append(device)

        return self.route
