import pytest

from solver import Solver
from utils import data_io


@pytest.fixture(scope="function")
def provide_main_line():
    process_line_name = "test/main_supply"
    s = Solver(process_line_name)
    return s


@pytest.fixture(scope="function")
def provide_branch_line():
    process_line_name = "test/branch_from_main"
    s = Solver(process_line_name)
    return s


def test_solver_uses_fluid_from_source(provide_main_line):
    s = provide_main_line
    fluid = s.run()
    assert s.fluid.p > 0
    assert fluid.fluid_name == "He"


def test_solver_can_make_route_from_shape(provide_main_line):
    s = provide_main_line
    s.run()
    assert s.route[0].position == "START"
    assert s.route[1].name == "Pipe DN50"
    assert s.route[2].name == "T-conn DN50"
    assert s.route[3].name == "Pipe DN50"


def test_csv_file_contains_data_with_units(provide_main_line):
    s = provide_main_line
    data = data_io.read_data(s.process_name)
    assert "device" in data[0].keys()
    assert data[1]["device"] == "Source"
    assert data[0]["pressure"] == "bar(a)"


def test_outflows(provide_main_line):
    s = provide_main_line
    s.run()
    assert s.outflows['HWR']['flow'] > 0


def test_branch_line(provide_main_line, provide_branch_line):
    s1 = provide_main_line
    s1.run()
    s2 = provide_branch_line
    fluid = s2.run()
    assert fluid.flow == 0.0729
