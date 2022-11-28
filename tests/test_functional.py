import pytest

from solver import Runner
from utils import coolprop


@pytest.fixture(scope="function")
def provide_lines():
    system_name = "sys/test_sup_branch_ret.toml"
    r = Runner(system_name)
    r.read_process_lines()
    return r.process_lines


def test_solver_can_compute_dp(provide_lines):
    s = provide_lines[0]
    end_fluid = s.run()
    assert end_fluid.dp > 0


def test_solver_can_compute_fluid_props(provide_lines):
    s = provide_lines[0]
    start_fluid = s.initiate_fluid()
    coolprop.update_fluid_props(start_fluid)
    start_fluid_rho = start_fluid.rho
    end_fluid = s.run()
    assert end_fluid.rho < start_fluid_rho


def test_reversed_route(provide_lines):
    s = provide_lines[2]
    start_fluid = s.initiate_fluid()
    coolprop.update_fluid_props(start_fluid)
    start_fluid_p = start_fluid.p
    end_fluid = s.run()
    assert end_fluid.p > start_fluid_p
