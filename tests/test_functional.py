import pytest

from solver import Solver


@pytest.fixture(scope="function")
def provide_solver_data():
    process_line_name = "test/main_supply"
    s = Solver(process_line_name)
    return s


def test_solver_can_compute_dp(provide_solver_data):
    s = provide_solver_data
    end_fluid = s.run()
    assert end_fluid.dp > 0
