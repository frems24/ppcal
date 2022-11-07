import pytest

from solver import Solver
from utils.system import Shape
from utils.fluids import Fluid


@pytest.fixture(scope="function")
def provide_solver_data():
    sh = Shape()
    fl = Fluid()
    s = Solver(sh, fl)
    return s


def test_solver_uses_fluid_object(provide_solver_data):
    s = provide_solver_data
    fluid = s.run()
    assert fluid.name == "He"


def test_solver_can_make_route_from_shape(provide_solver_data):
    s = provide_solver_data
    s.run()
    assert s.route[0].name == "Pipe DN25"
    assert s.route[1].name == "Pipe DN25"
