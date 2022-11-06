from solver import Solver
from solver import Shape


def test_pressure_is_1():
    s = Solver()
    fluid = s.run()
    assert fluid.p == 1


def test_route():
    sh = Shape()
    route = sh.make_route()
    assert route[0].name == "Pipe DN25"
    assert route[1].name == "Pipe DN25"
