# Clipboard Image Uploader

## Description
This Python project is a simple clipboard checker that periodically monitors the clipboard for image links or image data. When such content is found, it sends the image to a specified server via a POST request. The server URL and other settings are configured using an `.env` file.

## Features
- Monitors clipboard for images or image links.
- Sends images via POST request to a configurable server.
- Interval and upload settings are easily customizable via an `.env` file.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/laruss/clipboard-image-uploader.git
   ```

2. **Set up a Virtual Environment:**

   Python 3.12 is recommended for this project.

   ```bash
   cd <your-repo-folder>
   python3.12 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install the Required Packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the Environment Variables:**

   Create a `.env` file in the project root folder based on the `.env.sample` template:

   ```bash
   cp .env.sample .env
   ```

   Update the values in `.env` with your specific configuration:

   ```plaintext
   # .env example
   UPLOAD_URL=http://your-server-url/upload
   TIME_DELTA=5
   UPLOAD_FILE_KEY=file
   REQUEST_TIMEOUT=60
   ```

## Usage

To run the project, use:

```bash
python main.py
```

The script will start monitoring the clipboard at the specified interval (`TIME_DELTA`), and if it detects an image or a link to an image, it will send a POST request to the server URL specified in `UPLOAD_URL`.

## Configuration

All configuration options are set in the `.env` file. The following variables are supported:

- `UPLOAD_URL`: The server endpoint to which the image will be uploaded (required).
- `TIME_DELTA`: Time interval (in seconds) between clipboard checks. Default is 1 second.
- `UPLOAD_FILE_KEY`: The form key to be used for the image file in the POST request. Default is `'file'`.
- `REQUEST_TIMEOUT`: Timeout for the upload request (in seconds). Default is 60 seconds.

## Project Structure

```
├── .env                 # Environment configuration file
├── .env.sample          # Sample environment file
├── app_types.py         # Contains type definitions used in the app
├── clipboard.py         # Clipboard monitoring logic
├── env.py               # Environment variable handling
├── logger.py            # Logger configuration
├── main.py              # Main application entry point
├── readme.md            # Project readme file
├── requirements.txt     # Python package dependencies
├── rest.py              # Functions for handling HTTP requests
└── utils.py             # Helper utility functions
```

## Requirements
- **Python 3.12**
- Libraries specified in `requirements.txt`

## TODO
- [ ] Implement tests for all modules.
- [ ] Add support for other media types (e.g., video).
- [ ] Enhance logging and error handling.
- [ ] Add support for multiple image uploads in a single request.
- [ ] Add support for another system notifications (not only MacOS).
