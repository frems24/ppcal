import pytest

from solver import Runner
from utils import data_io


@pytest.fixture(scope="function")
def provide_lines():
    system_name = "sys/test_sup_branch_ret"
    r = Runner(system_name)
    process_lines = r.get_lines()
    return process_lines


def test_runner_can_make_system_to_solve(provide_lines):
    assert len(provide_lines) == 3
    assert provide_lines[0].line_name == "main_supply"
    assert provide_lines[1].line_name == "branch_from_main"
    assert provide_lines[2].line_name == "reversed-vent"


def test_solver_uses_fluid_from_source(provide_lines):
    process_line = provide_lines[0]
    fluid = process_line.run()
    assert process_line.fluid.p > 0
    assert fluid.fluid_name == "He"
    assert fluid.props_pkg == "coolprop"


def test_solver_can_make_route_from_shape(provide_lines):
    s = provide_lines[0]
    s.run()
    assert s.route[0].position == "START"
    assert s.route[1].name == "Pipe DN50"
    assert s.route[1].number == 1
    assert s.route[2].name == "T-conn DN50"
    assert s.route[4].name == "Elbow DN50"
    assert s.route[5].name == "Elbow DN50"
    assert s.route[4].number == 1
    assert s.route[5].number == 3


def test_csv_file_contains_data_with_units(provide_lines):
    s = provide_lines[0]
    data = data_io.read_data(s.process_name)
    assert "device" in data[0].keys()
    assert data[1]["device"] == "Source"
    assert data[0]["pressure"] == "bar(a)"


def test_outflows(provide_lines):
    s = provide_lines[0]
    s.run()
    assert s.outflows['HWR']['flow'] > 0


def test_branch_line(provide_lines):
    s1 = provide_lines[0]
    s2 = provide_lines[1]
    s1.run()
    fluid = s2.run()
    assert s2.route[2].name == "Valve DN15"
    assert fluid.flow == 0.0108
