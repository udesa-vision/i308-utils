import io
import zipfile
import os
import requests
from urllib.parse import urlparse
from contextlib import contextmanager


def guess_filename(url, response=None):
    """
        Guess the filename from the URL or HTTP headers.
        If response is None, only the URL is used to guess the filename.
    """
    # Guess filename from URL
    filename = os.path.basename(urlparse(url).path)
    default = "downloaded"
    if not filename and response is not None:
        # If URL doesn't contain a filename and response is provided, try to get it from headers
        content_disposition = response.headers.get('Content-Disposition')
        if content_disposition:
            filename = content_disposition.split("filename=")[-1].strip('"\'')
        else:
            filename = default
    elif not filename:
        # If URL doesn't contain a filename and no response is provided, use a default name
        filename = default
    return filename


def download(url, save_name="", re_download=False):
    """
    Download a file from a URL to a local path.

    Args:
        url (str): The URL of the file to download.
        save_name (str, optional): The local path to save the file. If empty or a directory, the filename is guessed.
        re_download (bool, optional): If False, skips the download if the file already exists. Defaults to False.
    """
    # Expand "~" to the user's home directory
    save_name = os.path.expanduser(save_name)

    # Use HEAD request to get headers and guess the filename
    response = requests.head(url)
    response.raise_for_status()  # Raise an error for bad status codes

    # If save_name is a directory or empty, guess the filename
    assume_dir = os.path.isdir(save_name) or "." not in save_name
    if assume_dir or not save_name:
        filename = guess_filename(url, response.headers)
        save_name = os.path.join(save_name, filename)

    # Skip download if the file already exists and skip_if_exists is True
    if not re_download and os.path.exists(save_name):
        print(f"File already exists, skipping download: {save_name}")
        return

    # Create intermediate directories if they don't exist
    dir_name = os.path.dirname(save_name)
    if dir_name != "":
        os.makedirs(dir_name, exist_ok=True)

    # Download the file
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an error for bad status codes

    with open(save_name, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

    print(f"Downloaded: {save_name}")



@contextmanager
def file_like(file):
    """
    Normalizes the input file into a file-like object.
    Handles str (file path), bytes, and io.BytesIO inputs.

    Args:
        file (str, bytes, or io.BytesIO): The input file.

    Yields:
        A file-like object ready for extraction.

    Raises:
        ValueError: If the input type is not supported.
    """
    if isinstance(file, bytes):
        yield io.BytesIO(file)  # Convert bytes to BytesIO
    elif isinstance(file, io.BytesIO):
        yield file  # Use the BytesIO object directly
    elif isinstance(file, str):
        with open(file, 'rb') as f:  # Open the file in binary mode
            yield f  # Yield the file object
    else:
        raise ValueError(
            "file must be a file path (str), raw zip data (bytes), or a file-like object (io.BytesIO).")


def unzip(zip_file, target_dir=None):
    """
    Extracts the contents of a zip file to a specified directory.

    Args:
        zip_file (str): Path to the zip file to be extracted.
        target_dir (str, optional): Directory where the contents will be extracted.
            If not provided, the contents will be extracted to the same directory
            as the zip file.

    """

    if not target_dir:
        # target_dir = os.path.dirname(zip_file)
        target_dir = os.getcwd()

    # Create the target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)

    with file_like(zip_file) as file:
        with zipfile.ZipFile(file, 'r') as z:
            z.extractall(target_dir)  # Extract to the specified target directory
            print(f"Extraction done to: {target_dir}")
