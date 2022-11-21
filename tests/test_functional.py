import pytest

from solver import Solver


@pytest.fixture(scope="function")
def provide_main_line():
    process_line_name = "test/main_supply"
    props_pkg = "coolprop"
    s = Solver(process_line_name, props_pkg)
    return s


def test_solver_can_compute_dp(provide_main_line):
    s = provide_main_line
    end_fluid = s.run()
    assert end_fluid.dp > 0


def test_solver_can_compute_fluid_props(provide_main_line):
    s = provide_main_line
    start_fluid_rho = s.fluid.rho
    end_fluid = s.run()
    assert end_fluid.rho < start_fluid_rho
