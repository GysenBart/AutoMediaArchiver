# All methods for scanning and archiving files
from pathlib import Path
from datetime import datetime
import os

from click import File
from config import Config
from app.models import ArchivedFile
import shutil
from flask_sqlalchemy import SQLAlchemy
from app import db, app

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
    # Class init nothing more
    def __init__(self, source_path, dest_path):
        self.source_path = source_path
        self.dest_path = dest_path

    # Method to scan a path for files
    def scanner(self, path, subfolders=False):
        print("Scanning path:", path)
        print("Include subfolders:", subfolders)

        files = []
        for p in Path(path).rglob('*') if subfolders else Path(path).glob('*'):
            if p.is_file():
                files.append(p)

        for file in files:
            print(file)

        return files

    # Method to check if a file exists in the database
    def file_exists_in_db(self, filename, filepath):
        with app.app_context():
            return db.session.query(ArchivedFile).filter_by(filename=filename, filepath=filepath).first() is not None

    # Method to check the date
    def check_archive_date_dir(self, date):
        path = Path(date)
        filename = path.stem  # removes .jpg
        try:
            date = datetime.strptime(filename, "%Y%m%d_%H%M%S")
            return date
        except ValueError:
            return None

    def archive_file(self):
        with app.app_context():
            walk_result = list(os.walk(self.source_path))
            for path, folders, files in walk_result:
                for filename in files:
                    print(filename)
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
                        new_file = ArchivedFile(
                            filename=filename,
                            filepath=dest_file,
                            file_size=file_size,
                            original_created=datetime.fromtimestamp(stat_info.st_mtime),
                            filehash=None  # You can set the filehash later if needed
                        )
                        print(new_file)
                        db.session.add(new_file)
                        db.session.commit()

'''

MONTHS_NL = (
    "Januari", "Februari", "Maart", "April", "Mei", "Juni",
    "Juli", "Augustus", "September", "Oktober", "November", "December",
)
FILENAME_DATE_FORMAT = "%Y%m%d_%H%M%S"


# ---------- Pure helpers (no database, reusable anywhere) ----------

def scan_files(path: Path, subfolders: bool = True) -> Iterator[Path]:
    """Yield every file in `path`, optionally including subfolders."""
    pattern = path.rglob("*") if subfolders else path.glob("*")
    return (p for p in pattern if p.is_file())


def parse_date_from_filename(path: Path) -> Optional[datetime]:
    """Return the datetime encoded in a name like 20240131_142530.jpg, else None."""
    try:
        return datetime.strptime(path.stem, FILENAME_DATE_FORMAT)
    except ValueError:
        return None


def build_destination(dest_root: Path, date: datetime, filename: str) -> Path:
    """<dest_root>/<year>/<Dutch month name>/<filename>"""
    return dest_root / str(date.year) / MONTHS_NL[date.month - 1] / filename


def hash_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    """SHA-256 of a file, read in chunks so large files don't fill memory."""
    sha = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(chunk_size):
            sha.update(chunk)
    return sha.hexdigest()


def copy_file(src: Path, dest: Path) -> Path:
    """Copy with metadata, creating folders. Raises if dest already exists."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        raise FileExistsError(dest)
    shutil.copy2(src, dest)
    return dest

# app/archiver.py (add next to the other helpers)
def resolve_path(raw: str, allowed_roots) -> Path:
    """Resolve a user-supplied path and make sure it's inside an allowed root."""
    path = Path(raw).expanduser().resolve()
    for root in allowed_roots:
        if path.is_relative_to(Path(root).resolve()):   # Python 3.9+
            return path
    raise ValueError(f"Path not allowed: {path}")

# ---------- Database layer ----------

class ArchiveRepository:
    def __init__(self, session=None):
        self.session = session or db.session

    def hash_exists(self, filehash: str) -> bool:
        return self.session.query(
            ArchivedFile.query.filter_by(filehash=filehash).exists()
        ).scalar()

    def add(self, *, filename: str, filepath: Path, size: int,
            original_created: datetime, filehash: str) -> ArchivedFile:
        record = ArchivedFile(
            filename=filename,
            filepath=str(filepath),
            file_size=size,
            original_created=original_created,
            filehash=filehash,
        )
        self.session.add(record)
        return record

    def commit(self):
        self.session.commit()


# ---------- Orchestration ----------

class Archiver:
    def __init__(self, source_path, dest_path, repo: Optional[ArchiveRepository] = None):
        self.source = Path(source_path)
        self.dest = Path(dest_path)
        self.repo = repo or ArchiveRepository()

    def archive_file(self, src: Path) -> str:
        """Archive one file. Returns 'archived', 'duplicate', 'no_date' or 'exists'."""
        date = parse_date_from_filename(src)
        if date is None:
            return "no_date"

        filehash = hash_file(src)
        if self.repo.hash_exists(filehash):
            return "duplicate"

        try:
            dest_file = copy_file(src, build_destination(self.dest, date, src.name))
        except FileExistsError:
            return "exists"

        stat = src.stat()
        self.repo.add(
            filename=src.name,
            filepath=dest_file,
            size=stat.st_size,
            original_created=datetime.fromtimestamp(stat.st_mtime),
            filehash=filehash,
        )
        return "archived"

    def run(self, subfolders: bool = True, batch_size: int = 100) -> dict:
        """Archive everything under the source path. Returns a summary count."""
        counts = {"archived": 0, "duplicate": 0, "no_date": 0, "exists": 0}
        for i, src in enumerate(scan_files(self.source, subfolders), start=1):
            counts[self.archive_file(src)] += 1
            if i % batch_size == 0:
                self.repo.commit()
        self.repo.commit()
        return counts
'''