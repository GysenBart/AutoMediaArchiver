from config import sync_folder, dest_folder
import os

print("testing")
print(f"Current working directory: {os.getcwd()}")
print(f"Source directory: {sync_folder}")
print(f"Directory exists: {os.path.exists(sync_folder)}")
print(f"Is directory: {os.path.isdir(sync_folder)}")

walk_result = list(os.walk(sync_folder))
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



"""
if __name__ == '__main__':
    print("--------------------------- AUTO MEDIA ARCHIVER ---------------------------")
    Main.main()
"""""