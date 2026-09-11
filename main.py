from datetime import datetime
from app.archiver import scanner, check_archive_date_dir, archive_file, MONTH_MASK
from config import Config, basedir
import os

"""
print("testing")
print(f"Current working directory: {os.getcwd()}")
print(f"Source directory: {Config.sync_folder}")
print(f"Directory exists: {os.path.exists(Config.sync_folder)}")
print(f"Is directory: {os.path.isdir(Config.sync_folder)}")
"""

def archive_file(source_path, file, dest_path):
    print("test")





walk_result = list(os.walk(Config.sync_folder))
print(f"Walk result: {walk_result}")
print(f"Walk result length: {len(walk_result)}")

# Iterate over files in directory
for path, folders, files in walk_result:
    #for folder_name in folders:
    #    print(folder_name)
    print(f"Path: {path}")
    print(f"Folders: {folders}")
    print(f"Files: {files}")

    # Open file
    for filename in files:
        print(filename)
        date = check_archive_date_dir(filename)
        print(date.day)
        print(MONTH_MASK[date.month])
        print(date.year)
        full_path = os.path.join(path, filename)

        stat_info = os.stat(full_path)

        file_size = stat_info.st_size

        modified_time = datetime.fromtimestamp(stat_info.st_ctime)

        print(f"File: {full_path}")
        print(f"Size: {file_size} bytes")
        print(f"Modified: {modified_time}")
        archive_year = date.year
        archive_month_name = MONTH_MASK[date.month]
        dest_folder = os.path.join(Config.archive_folder, str(archive_year), archive_month_name)

        if not os.path.exists(dest_folder):
            print(f"Creating archive directory: {dest_folder}")
            os.makedirs(dest_folder)

        print(f"Archiving destination folder: {dest_folder}")

        # Prepare data for potential database entry or further processing
        file_archive_data = {
            "original_path": full_path,
            "filename": filename,
            "archive_date": date,
            "archive_year": archive_year,
            "archive_month_name": archive_month_name,
            "dest_folder": dest_folder,
            "file_size": file_size,
            "modified_time": modified_time
        }
        # In a real scenario, this 'file_archive_data' would then be used
        # to insert into a database and then move/copy the file.
        print(f"Prepared archive data for {filename}: {file_archive_data}")
        print("-" * 40)
