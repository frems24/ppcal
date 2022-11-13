import csv

from .devices import Device
from .fluids import Fluid
from settings import RESULTS


def write_data(data: list[dict], dev: Device, fl: Fluid) -> None:
    """
    Write actual Device's and Fluid's parameters in data dictionary.
    :param data: List of dictionary items
    :param dev: Actual Device instance
    :param fl: Actual Fluid instance
    """
    row = dict()
    row['device'] = dev.name
    row['mass_stream'] = fl.m_flow
    row['pressure'] = round(fl.p, 6)
    row['pressure_drop'] = round(fl.dp, 6)
    row['temperature'] = fl.temp
    row['density'] = fl.rho
    row['viscosity'] = fl.mi
    data.append(row)


def save_data(process_name: str, data: list[dict]) -> None:
    """
    Save data dictionary in csv file.
    :param process_name: Name of csv file
    :param data: Actual data to write in
    """
    with open(RESULTS / f"{process_name}.csv", mode='w') as csv_file:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def read_data(process_name: str) -> list[dict]:
    """
    Read data from csv file.
    :param process_name:
    :return: List of data dictionary rows
    """
    with open(RESULTS / f"{process_name}.csv", mode='r') as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader)
