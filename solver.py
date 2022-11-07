from utils.system import Shape
from utils.fluids import Fluid


class Solver:
    def __init__(self, shape, fluid):
        self.shape = shape
        self.fluid = fluid
        self.route = None

    def get_route(self):
        return self.shape.make_route()

    def run(self):
        self.route = self.get_route()
        for device in self.route:
            self.fluid = device(self.fluid).get_fluid_after()
        return self.fluid


if __name__ == "__main__":
    sh = Shape(shape=["Pipe25", "Pipe25"])
    fl = Fluid(p=2.0, name="He")
    s = Solver(sh, fl)
    f = s.run()
    print(f"Pressure: {f.p} bar(a)")
