import datetime
import re
import pathlib
import inspect
import traceback
from typing import Union, List

import requests
from lxml import html

# SETUP PATH CONSTANTS


RAW_DATA_DIRECTORY = pathlib.Path("raw_data")
RAW_DATA_FILENAME = pathlib.Path("neodys.cat")
RAW_DATA_PATH = RAW_DATA_DIRECTORY / RAW_DATA_FILENAME

DATA_SOURCE_MAIN_PAGE_URL = "https://newton.spacedys.com/neodys/index.php?pc=1.0"
DATA_SOURCE_FILE_URL = "https://newton.spacedys.com/~neodys2/neodys.cat"


def write_log(message: str, log_dir: str = "logs",
              log_name: str = f"neo_log_{datetime.date.today()}") -> None:

    if len(inspect.stack()) > 1:
        function = inspect.stack()[1][3]
    else:
        function = ""

    if not pathlib.Path(log_dir).exists():
        pathlib.Path(log_dir).mkdir()

    with open(pathlib.Path(log_dir) / pathlib.Path(log_name), mode="a+", encoding="utf-8") as logfile:
        now = datetime.datetime.now().isoformat(timespec='seconds')
        logfile.write(f"[{now}][{function}] {message}\n")


def download_data_source_file(file_url: str, target_file_path: Union[pathlib.Path, str]) -> None:
    response = requests.get(url=file_url, timeout=10)
    write_log(message=f"Response status code when fetching file with data: {response.status_code}")

    if not response:
        write_log(message=f"No response from {file_url}")

    elif response.status_code < 200 or response.status_code > 299:
        write_log(message=f"Page responded with: {response.status_code}")

    elif 200 <= response.status_code < 300:
        write_log(message=f"Successfully fetched data: status {response.status_code}")
        with open(target_file_path, mode="wb+") as data_file:
            data_file.write(response.content)


def extract_data_from_source(source_path: Union[pathlib.Path, str]) -> Union[List[dict], None]:
    """Extract data about Near Earth Objects from specified file"""
    source_path = pathlib.Path(source_path) if isinstance(source_path, str) else source_path
    if not source_path.exists():
        write_log(message=f"Path {source_path} does not exist!")
        print(f"Path {source_path} does not exist!")
        return None

    out_data: List = []
    with open(source_path) as source_file:
        # skip header - first 6 lines
        raw_data_lines = source_file.readlines()[6:]
        for line in raw_data_lines:
            try:
                line = line.split()  # split on whitespace
                out_data.append({
                    "Name": line[0].replace("'", ""),
                    "Epoch_MJD": float(line[1]),
                    "SemMajAxis_AU": float(line[2]),
                    "Ecc": float(line[3]),
                    "Incl_deg": float(line[4]),
                    "LongAscNode_deg": float(line[5]),
                    "ArgP_deg": float(line[6]),
                    "Mean_Anom_deg": float(line[7]),
                    "AbsMag": float(line[8]),
                    "SlopeParamG": float(line[9]),
                    "Aphel_AU": (1 + float(line[3])) * float(line[2]),
                    "Perihel_AU": (1 - float(line[3])) * float(line[2])

                })

            except Exception as e:
                write_log(message=f"Exception occurred while reading data from file: {e},"
                                  f"Traceback: {traceback.format_exc}")
                continue

        return out_data


if __name__ == "__main__":

    # CREATE DATA DIRECTORY IF NOT PRESENT
    if not RAW_DATA_DIRECTORY.exists():
        write_log(message=f"Creating directory tree for raw data: {RAW_DATA_DIRECTORY}")
        RAW_DATA_DIRECTORY.mkdir()

    # 1. GET DATA FROM PAGE - IF NOT ALREADY PRESENT
    if not pathlib.Path.is_file(RAW_DATA_PATH):
        # get file containing the data
        download_data_source_file(file_url=DATA_SOURCE_FILE_URL,
                                  target_file_path=RAW_DATA_PATH)

