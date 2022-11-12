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

        list_of_devices = list(scheme_toml)

        for item in list_of_devices:
            description = scheme_toml[item]
            device = getattr(devices, description['device'])(**description)
            self.route.append(device)

        return self.route
