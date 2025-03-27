from utils.application.logger import logger
from mcp.server.fastmcp import Context
from typing_extensions import Annotated
from pydantic import Field
import json, os


# Function to search for a string in files recursively in a given folder
def search_in_files(folder_path, search_string):
    result = []
    # Walk through all files and directories recursively
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    if search_string.lower() in content.lower():
                        # Get file size
                        file_size = os.path.getsize(file_path)
                        result.append({"path": file_path, "size": file_size})
            except Exception as e:
                logger.warning(f"Could not read file {file_path}: {e}")
                continue
    return result


def search_string_tool(
    folder_path: Annotated[
        str,
        Field(
            description="The folder path where the search will be conducted. Ex: /path/to/folder"
        ),
    ],
    search_string: Annotated[
        str,
        Field(description="The string to search for in the files. Ex: SomeComponent"),
    ],
    ctx: Context,
) -> str:
    """
    Search for a specific string within all files in a given folder.

    Request Body Parameters:
    - folder (str): Required, the path of the folder where the search will be conducted.
    - search_string (str): Required, the string to search for in the files.

    Returns:
    - 200 OK: A JSON object containing a list of files that contain the search string.
    - 400 Bad Request: If either the 'folder' or 'search_string' parameter is missing.
    - 404 Not Found: If the folder does not exist.

    Example Response (200 OK):
    {
        "files": [
            {
                "path": "/path/to/folder/file1.txt",
                "size": 1024
            },
            {
                "path": "/path/to/folder/subfolder/file2.txt",
                "size": 2048
            }
        ]
    }

    Example Response (404 Not Found):
    {
        "message": "No files found with the given search string."
    }

    Example Response (400 Bad Request):
    {
        "error": "Missing folder or search_string parameter"
    }
    """

    logger.info(
        f"Search request: folder_path={folder_path}, search_string={search_string}"
    )

    if not folder_path or not search_string:
        return json.dumps({"error": "Missing folder or search_string parameter"})
    if not os.path.exists(folder_path):
        return json.dumps({"error": "The provided folder path does not exist"})

    found_files = search_in_files(folder_path, search_string)

    # Return an empty list if no files are found
    return json.dumps({"files": found_files})
