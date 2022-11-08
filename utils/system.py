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
            scheme_conf = tomli.load(fp)
        list_of_devices = list(scheme_conf)
        for element in list_of_devices:
            desc = scheme_conf[element]
            device = getattr(devices, desc['name'])(length=desc['length'])
            self.route.append(device)
        return self.route
