from utils.system import Shape
from utils.fluids import Fluid


class Solver:
    def __init__(self, shape, fluid):
        self.shape = shape
        self.fluid = fluid
        self.route = None

    def get_route(self):
        self.route = self.shape.make_route()

    def run(self):
        self.get_route()
        return self.fluid


if __name__ == "__main__":
    sh = Shape()
    fl = Fluid()
    s = Solver(sh, fl)
    f = s.run()
    print(f"Pressure: {f.p} bara")
