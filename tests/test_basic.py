import pytest

from solver import Solver
from utils import data_io


@pytest.fixture(scope="function")
def provide_solver_data():
    process_line_name = "test/main_supply"
    s = Solver(process_line_name)
    return s


def test_solver_uses_fluid_from_source(provide_solver_data):
    s = provide_solver_data
    fluid = s.run()
    assert s.fluid.p > 0
    assert fluid.fluid_name == "He"


def test_solver_can_make_route_from_shape(provide_solver_data):
    s = provide_solver_data
    s.run()
    assert s.route[0].position == "START"
    assert s.route[1].name == "Pipe DN50"
    assert s.route[2].name == "T-connection"
    assert s.route[3].name == "Pipe DN50"


def test_csv_file_contains_data_with_units(provide_solver_data):
    s = provide_solver_data
    data = data_io.read_data(s.process_name)
    assert "device" in data[0].keys()
    assert data[1]["device"] == "Source"
    assert data[0]["pressure"] == "bar(a)"


def test_outflows(provide_solver_data):
    s = provide_solver_data
    s.run()
    assert s.outflows['HWR']['outflow'] > 0
