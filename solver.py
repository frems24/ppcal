from utils import devices
from utils import fluid


class Shape:
    def __init__(self):
        self.shape = ["Pipe25", "Pipe25"]
        self.route = []

    def make_route(self):
        for desc in self.shape:
            device = getattr(devices, desc)
            self.route.append(device)
        return self.route


class Solver:
    def __init__(self):
        self.fluid = None

    def entry_point(self):
        self.fluid = fluid.Fluid()

    def run(self):
        self.entry_point()
        return self.fluid


if __name__ == "__main__":
    s = Solver()
    f = s.run()
    print(f"Pressure: {f.p} bara")
