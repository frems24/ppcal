import tomli

from settings import TOML_DIR
from . import devices


class Scheme:
    """Scheme of the whole system."""
    def __init__(self, scheme_name: str):
        self.scheme_name = scheme_name
        self.route = []

    def make_route(self):
        """Make a list of devices connected together in the system."""
        filename = f"{self.scheme_name}.toml"
        with open(TOML_DIR / filename, mode="rb") as fp:
            scheme_toml = tomli.load(fp)
        list_of_devices = list(scheme_toml)
        for item in list_of_devices:
            description = scheme_toml[item]
            device = getattr(devices, description['type'])(**description)
            self.route.append(device)
        return self.route
