import csv
import tomllib
import json

from .devices import Device
from .fluids import Fluid
from settings import BASE_DIR, RESULTS, SYSTEMS_DIR


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
    row['number'] = dev.number
    if dev.device == 'Pipe':
        row['length'] = round(dev.length - dev.bell_l, 3)
        row['bell_l'] = round(dev.bell_l, 3) if dev.bell_l else None
    else:
        row['length'] = round(dev.length, 3) if dev.length else None
        row['bell_l'] = None
    row['flow'] = round(fl.flow, 4)
    row['pressure'] = round(fl.p, 6)
    row['dp'] = round(fl.dp * 1_000, 4)
    row['dp_total'] = round(fl.dp_total * 1_000, 4)
    row['temperature'] = fl.temp
    row['density'] = round(fl.rho, 3)
    # row['viscosity'] = fl.mi
    return row


def save_data(process_name: str, data: list[dict]) -> None:
    """
    Save data dictionary in csv file.
    :param process_name: Name of csv file
    :param data: Actual data to write in
    """
    try:
        with open(BASE_DIR / "utils" / "units.toml", "rb") as fp:
            units = tomllib.load(fp)
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


def write_outflow_data(outflow_fl: Fluid) -> dict:
    """
    Write actual Tee outflow parameters in data dictionary.
    :param outflow_fl: Actual branched Fluid instance
    :return: Branched fluid parameters in Tee outflow
    """
    outflow_data = dict()
    outflow_data['fluid_name'] = outflow_fl.fluid_name
    outflow_data['p'] = outflow_fl.p
    outflow_data['temp'] = outflow_fl.temp
    outflow_data['flow'] = outflow_fl.flow
    return outflow_data


def save_outflows_scheme(process_name: str, outflows: dict) -> None:
    """
    Save branched fluids parameters from each Tee outflow in json file.
    :param process_name: Name of file
    :param outflows: Actual data to write in
    """
    with open(SYSTEMS_DIR / f"{process_name}.json", 'w') as fp:
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
