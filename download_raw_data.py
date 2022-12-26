import re
import pathlib

import requests
import sqlite3
from lxml import html

# SETUP PATH CONSTANTS



RAW_DATA_DIRECTORY = pathlib.Path("raw_data")
RAW_DATA_FILENAME = pathlib.Path("neodys.cat")
RAW_DATA_PATH = RAW_DATA_DIRECTORY / RAW_DATA_FILENAME

DATA_SOURCE_MAIN_PAGE_URL = "https://newton.spacedys.com/neodys/index.php?pc=1.0"
DATA_SOURCE_FILE_URL = "https://newton.spacedys.com/~neodys2/neodys.cat"
#%%

if __name__ == "__main__":

    if not RAW_DATA_DIRECTORY.exists():
        RAW_DATA_DIRECTORY.mkdir()

    # 1. GET DATA FROM PAGE

    # check if main page responds correctly
    response = requests.get(url=DATA_SOURCE_MAIN_PAGE_URL, timeout=10)

    if not response:
        print(f"Failed to connect to page {DATA_SOURCE_MAIN_PAGE_URL}")
    else:
        print(f"Page responded with {response.status_code} status code")
        page_tree = html.fromstring(response.text)
        current_neos: str = page_tree.xpath("//p[@align='center']/b/text()")[0]
        current_neos_number: int = int(re.sub('\D', '', current_neos))
        print(f"Current number of known NEOs: {current_neos_number}")

    # get file containing the data
    response = requests.get(url=DATA_SOURCE_FILE_URL, timeout=10)
    print(f"Response status code when fetching file with data: {response.status_code}")

    if not response:
        print(f"No response from {DATA_SOURCE_FILE_URL}")

    elif response.status_code < 200 or response.status_code > 299:
        print(f"Page responded with: {response.status_code}")

    elif 200 <= response.status_code < 300:
        print(f"Successfully fetched data: status {response.status_code}")
        with open(RAW_DATA_PATH, mode="wb+") as data_file:
            data_file.write(response.content)
