# ALl methods for scanning and archiving files
from pathlib import Path
from datetime import datetime
from enum import IntEnum
import os
from . import Config

MONTH_MASK = {
    1: "Januari",
    2: "Februari",
    3: "Maart",
    4: "April",
    5: "Mei",
    6: "Juni",
    7: "Juli",
    8: "Augustus",
    9: "September",
    10: "Oktober",
    11: "November",
    12: "December"
}

def scanner(path, subfolders=False):
    # To just scan a folder and if necessary also subfolders
    print(path)
    print(subfolders)

def check_archive_date_dir(date):
    path = Path(date)
    filename = path.stem  # removes .jpg
    date = datetime.strptime(filename, "%Y%m%d_%H%M%S")
    return date


def archive_file(source_path, dest_path, file):
    walk_result = list(os.walk(Config.sync_folder))
    # Iterate over files in directory
    for path, folders, files in walk_result:
        print(f"Path: {path}")
        print(f"Folders: {folders}")
        print(f"Files: {files}")

        # Open file
        for filename in files:
            print(filename)
            full_path = os.path.join(path, filename)

            stat_info = os.stat(full_path)

            file_size = stat_info.st_size

            modified_time = datetime.fromtimestamp(stat_info.st_ctime)

            print(f"File: {full_path}")
            print(f"Size: {file_size} bytes")
            print(f"Modified: {modified_time}")
            print("-" * 40)


