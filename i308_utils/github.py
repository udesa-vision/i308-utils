import os
import requests


def download_from_github(
        repo_url,
        branch="main",
        relative_path="",
        output_dir=None,
        verbose=False,
):
    """
    Recursively downloads all files from a GitHub repository at a specified branch and relative path.
    Skips downloading files that already exist in the output directory.

    Args:
        repo_url (str): The GitHub repository path in the format 'username/repository'.
        branch (str, optional): The branch name to download from. Defaults to 'main'.
        relative_path (str, optional): The relative path within the repository to start downloading from.
                                      Defaults to the root of the repository (empty string).
        output_dir (str, optional): The directory where the downloaded files will be saved.
                                    Defaults to the current working directory.
        verbose (bool): indicates if it should print output

    """

    def _print(message):
        if verbose:
            print(message)

    # Set default output directory to the current working directory if not specified
    if output_dir is None:
        output_dir = os.getcwd()

    # Construct the API URL to get the repository contents
    api_url = f"https://api.github.com/repos/{repo_url}/contents/{relative_path}?ref={branch}"

    _print(f"Fetching contents from: {api_url}")

    # Make a GET request to the GitHub API
    response = requests.get(api_url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch repository contents. Status code: {response.status_code}")

    # Parse the JSON response
    contents = response.json()

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over the contents
    for item in contents:
        if item['type'] == 'file':
            # Check if the file already exists in the output directory
            file_path = os.path.join(output_dir, item['name'])
            if os.path.exists(file_path):
                _print(f"Skipping (already exists): {file_path}")
                continue

            # Download the file
            file_url = item['download_url']
            file_response = requests.get(file_url)

            if file_response.status_code == 200:
                # Save the file to the output directory
                with open(file_path, 'wb') as file:
                    file.write(file_response.content)
                _print(f"Downloaded: {file_path}")
            else:
                _print(f"Failed to download file: {item['name']}")
        elif item['type'] == 'dir':
            # Recursively download the directory
            new_relative_path = os.path.join(relative_path, item['name'])
            new_output_dir = os.path.join(output_dir, item['name'])
            download_from_github(repo_url, branch, new_relative_path, new_output_dir)
