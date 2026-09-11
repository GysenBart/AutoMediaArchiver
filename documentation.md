# Media Archiver Documentation

## Overview

The Media Archiver is a web-based application designed to manage and archive media files. This document outlines the structure, features, and usage of the application.

## Dashboard

The Dashboard provides a high-level overview of the application's current status and allows users to interact with the system.

### Key Components

1. **Stats Section**
   - Displays key metrics such as total archived files, last scan time, next scheduled scan, and active jobs.

2. **Run Scan Manually**
   - A button to manually trigger a scan of the media files.

3. **Scan Destination Folder**
   - Allows users to specify a folder to scan and an option to include subfolders.

4. **Archive Jobs**
   - A table listing all archive jobs with actions to scan or delete jobs.

5. **Add New Job**
   - A form to add new archive jobs with source folder, destination folder, and subfolder options.

6. **File List**
   - A table listing all files with options to delete selected files.

7. **Scheduler**
   - A form to update the interval at which the application runs scans.

8. **Logs**
   - A log box displaying recent application logs.

## Installation

To install the Media Archiver, follow these steps:

1. **Clone the Repository**
   ```sh
   git clone https://github.com/username/media-archiver.git
   cd media-archiver
   ```

2. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   Create a `.env` file and configure the necessary environment variables.

4. **Run the Application**
   ```sh
   python app.py
   ```

## Usage

### Basic Usage

1. **Access the Dashboard**
   Open your web browser and navigate to `http://localhost:5000`.

2. **Run a Scan**
   - Click the "Run Scan Now" button to manually trigger a scan.
   - Use the "Scan Destination Folder" form to scan a specific folder.

3. **Manage Jobs**
   - Use the "Add New Job" form to create new archive jobs.
   - Use the "Archive Jobs" table to manage existing jobs.

4. **Manage Files**
   - Use the "File List" table to delete selected files.

5. **Configure Scheduler**
   - Use the "Scheduler" form to update the scan interval.

## Contributing

Contributions to the Media Archiver are welcome! Please follow these guidelines:

1. **Fork the Repository**
   ```sh
   git clone https://github.com/username/media-archiver.git
   cd media-archiver
   ```

2. **Create a Feature Branch**
   ```sh
   git checkout -b feature-name
   ```

3. **Make Changes and Commit**
   ```sh
   git add .
   git commit -m "Add new feature"
   ```

4. **Push Changes**
   ```sh
   git push origin feature-name
   ```

5. **Open a Pull Request**

## License

The Media Archiver is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.