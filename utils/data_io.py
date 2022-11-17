import csv
import tomli
import json

from .devices import Device, Tee
from .fluids import Fluid
from settings import TOML_DIR, RESULTS, SCHEMES_DIR


def write_data_row(dev: Device, fl: Fluid) -> dict:
    """
    Write actual Device's and Fluid's parameters in data dictionary.
    :param dev: Actual Device instance
    :param fl: Actual Fluid instance
    :return: Results for a device
    """
    row = dict()
    row['position'] = dev.position
    row['device'] = dev.name
    row['length'] = dev.length
    row['flow'] = round(fl.flow, 4)
    row['pressure'] = round(fl.p, 6)
    row['pressure_drop'] = round(fl.dp * 1_000, 3)
    row['temperature'] = fl.temp
    row['density'] = fl.rho
    row['viscosity'] = fl.mi
    return row


def save_data(process_name: str, data: list[dict]) -> None:
    """
    Save data dictionary in csv file.
    :param process_name: Name of csv file
    :param data: Actual data to write in
    """
    try:
        with open(TOML_DIR / "units.toml", "rb") as fp:
            units = tomli.load(fp)
    except FileNotFoundError:
        units = {}

    file_path = RESULTS / f"{process_name}.csv"
    base_dir = file_path.parent
    base_dir.mkdir(parents=True, exist_ok=True)
    with open(file_path, mode='w') as csv_file:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(units)
        writer.writerows(data)


def write_outflow_data(dev: Tee, fl: Fluid) -> dict:
    outflow_data = dict()
    outflow_data['fluid_name'] = fl.fluid_name
    outflow_data['p'] = dev.outflow_p
    outflow_data['temp'] = dev.outflow_temp
    outflow_data['flow'] = dev.outflow_m
    return outflow_data


def save_outflows_scheme(process_name: str, outflows: dict) -> None:
    with open(SCHEMES_DIR / f"{process_name}.json", 'w') as fp:
        json.dump(outflows, fp)


def read_data(process_name: str) -> list[dict]:
    """
    Read data from csv file
    :param process_name: Name of csv file
    :return: List of data dictionary rows
    """
    with open(RESULTS / f"{process_name}.csv", mode='r') as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader)
