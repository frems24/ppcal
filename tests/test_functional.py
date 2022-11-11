import pytest

from solver import Solver


@pytest.fixture(scope="function")
def provide_solver_data():
    process_line_name = "m_4_5_K_sup"
    s = Solver(process_line_name)
    return s


def test_solver_can_compute_dp(provide_solver_data):
    s = provide_solver_data
    start_p = s.fluid.p
    end_fluid = s.run()
    assert end_fluid.p < start_p
