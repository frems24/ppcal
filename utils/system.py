import tomli

from . import devices


class Scheme:
    """Scheme of the whole system."""
    def __init__(self, scheme_name: str):
        self.scheme_name = scheme_name
        self.route = []

    def make_route(self):
        """Make a list of devices connected together in the system."""
        filename = f"{self.scheme_name}.toml"
        with open(file=filename, mode="rb") as fp:
            scheme_conf = tomli.load(fp)
        list_of_devices = scheme_conf['scheme']
        for element in list_of_devices:
            device = getattr(devices, element)
            self.route.append(device)
        return self.route
