import os
from utils.application.logger import logger
from typing import List, Dict
from pydantic import Field
from typing_extensions import Annotated


def get_file_contents_tool(
    files: Annotated[
        List[str],
        Field(
            description='A list of files with full paths to retrieve the contents from. Ex: ["/path/to/file1.txt", "/path/to/file2.txt"]'
        ),
    ],
) -> Dict:
    """
    Retrieve the contents of specified files. Send multiple files at once as list. Ex: ["/path/to/file1.txt", "/path/to/file2.txt"]

    Request Body Parameters:
    - files (list of str): Required, a list of file paths for which to retrieve contents.

    Returns:
    - 200 OK: A JSON object containing the contents of the specified files.
    - 400 Bad Request: If the 'files' parameter is missing or not a list.
    - 404 Not Found: If any of the provided file paths do not exist.
    """
    file_contents = {}
    file_not_found_errors = []

    for file_path in files:
        # Expand the user path (i.e., ~) to the full home directory path
        file_path = os.path.expanduser(file_path)

        # Check if the file exists; if not, add to the error list
        if not os.path.exists(file_path):
            file_not_found_errors.append({"file": file_path, "error": "File not found"})
            continue  # Skip to the next file

        # Read the contents of the file and store it in the dictionary
        try:
            # Try reading with UTF-8 first
            with open(file_path, "r", encoding="utf-8") as file:
                file_contents[file_path] = file.read()
        except UnicodeDecodeError:
            try:
                # If UTF-8 fails, try another encoding (ISO-8859-1 or latin1)
                with open(file_path, "r", encoding="ISO-8859-1") as file:
                    file_contents[file_path] = file.read()
            except Exception as e:
                file_not_found_errors.append({"file": file_path, "error": str(e)})
        except Exception as e:
            file_not_found_errors.append({"file": file_path, "error": str(e)})

    response = {"data": file_contents}

    # If there were any errors, include them in the response
    if file_not_found_errors:
        response["errors"] = file_not_found_errors

    return response
