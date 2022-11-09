import math
import pytest

from solver import Solver


@pytest.fixture(scope="function")
def provide_solver_data():
    scheme_name = "three_pipes"
    fluid_name = "he_at_3bar"
    s = Solver(scheme_name, fluid_name)
    return s


def test_solver_uses_fluid_object(provide_solver_data):
    s = provide_solver_data
    assert s.fluid.p == 3.0
    fluid = s.run()
    assert fluid.name == "He"


def test_solver_can_make_route_from_shape(provide_solver_data):
    s = provide_solver_data
    s.run()
    assert s.route[0].name == "Pipe DN20"
    assert s.route[1].name == "Pipe DN50"
    assert s.route[2].name == "Pipe DN20"


def test_solver_can_compute_route(provide_solver_data):
    s = provide_solver_data
    start_p = s.fluid.p
    end_fluid = s.run()
    dp = sum(device.dp for device in s.route)
    assert math.isclose(start_p - end_fluid.p, dp, abs_tol=0.001)
