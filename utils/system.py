from utils import devices


class Shape:
    def __init__(self):
        self.shape = ["Pipe25", "Pipe25"]
        self.route = []

    def make_route(self):
        for desc in self.shape:
            device = getattr(devices, desc)
            self.route.append(device)
        return self.route
