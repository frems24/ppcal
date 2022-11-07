from typing import List

from . import devices


class Scheme:
    """Scheme of the whole system."""
    def __init__(self, scheme: List[str]):
        self.scheme = scheme
        self.route = []

    def make_route(self):
        """Make a list of devices connected together in the system."""
        for element in self.scheme:
            device = getattr(devices, element)
            self.route.append(device)
        return self.route
