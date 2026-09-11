# All methods for scanning and archiving files
from pathlib import Path
from datetime import datetime
import os

from click import File
from . import Config
import shutil
from flask_sqlalchemy import SQLAlchemy
from app import db

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

# All methods for scanning and archiving files
from pathlib import Path
from datetime import datetime
import os

from click import File
from . import Config
import shutil
from flask_sqlalchemy import SQLAlchemy
from app import db

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

class Archiver:
    def __init__(self, source_path, dest_path):
        self.source_path = source_path
        self.dest_path = dest_path
    def scanner(self, path, subfolders=False):
        # To just scan a folder and if necessary also subfolders
        print("Scanning path:", path)
        print("Include subfolders:", subfolders)

        files = []
        for p in Path(path).rglob('*') if subfolders else Path(path).glob('*'):
            if p.is_file():
                files.append(p)

        for file in files:
            print(file)

        return files

    def check_archive_date_dir(self, date):
        path = Path(date)
        filename = path.stem  # removes .jpg
        try:
            date = datetime.strptime(filename, "%Y%m%d_%H%M%S")
            return date
        except ValueError:
            return None

    def archive_file(self):
        walk_result = list(os.walk(self.source_path))
        for path, folders, files in walk_result:
            for filename in files:
                full_path = os.path.join(path, filename)
                if not os.path.isfile(full_path):
                    continue

                stat_info = os.stat(full_path)
                file_size = stat_info.st_size
                modified_time = datetime.fromtimestamp(stat_info.st_mtime)

                # Extract date from filename
                date = self.check_archive_date_dir(filename)
                if date:
                    year = date.year
                    month = MONTH_MASK[date.month]
                    month_folder = os.path.join(self.dest_path, str(year), month)
                    os.makedirs(month_folder, exist_ok=True)

                    # Copy file to the new folder
                    dest_file = os.path.join(month_folder, filename)
                    shutil.copy2(full_path, dest_file)

                    # Insert file metadata into the database
                    new_file = File(name=filename, path=dest_file, size=file_size, modified_time=modified_time)
                    db.session.add(new_file)
                    db.session.commit()