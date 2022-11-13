import pytest

from solver import Solver
from utils import solver_data


@pytest.fixture(scope="function")
def provide_solver_data():
    process_line_name = "test_pipes"
    s = Solver(process_line_name)
    return s


def test_solver_uses_fluid_object(provide_solver_data):
    s = provide_solver_data
    assert s.fluid.p == 3.0
    fluid = s.run()
    assert fluid.name == "He"


def test_solver_can_make_route_from_shape(provide_solver_data):
    s = provide_solver_data
    s.run()
    assert s.route[1].name == "Pipe DN20"
    assert s.route[2].name == "Pipe DN50"
    assert s.route[3].name == "Pipe DN20"


def test_csv_file_contains_data(provide_solver_data):
    s = provide_solver_data
    data = solver_data.read_data(s.process_name)
    assert "device" in data[0].keys()
    assert data[1]["device"] == "Pipe DN20"
