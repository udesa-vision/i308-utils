import zipfile
import os
import requests
from urllib.parse import urlparse


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


def download_file(url, save_name=""):
    """
        Download a file from a URL to a local path.
    """
    # Expand "~" to the user's home directory
    save_name = os.path.expanduser(save_name)

    # If save_name is a directory or empty, guess the filename
    if os.path.isdir(save_name) or not save_name:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for bad status codes
        filename = guess_filename(url, response)
        save_name = os.path.join(save_name, filename)

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


def unzip(save_path):
    try:
        with zipfile.ZipFile(save_path) as z:
            z.extractall(os.path.split(save_path)[0])  # Unzip where downloaded.
            print("Done")
    except Exception as ex:
        print("can't uncompress: {ex}")
