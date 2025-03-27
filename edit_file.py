from utils.application.logger import logger
from pydantic import BaseModel, Field, root_validator

# from mcp.server.fastmcp import Context
from typing_extensions import Annotated
from pydantic import Field
import json


class FileToolParams(BaseModel):
    file_path: Annotated[
        str, Field(description="The full file path of the file to be edited.")
    ]
    new_content: Annotated[
        str, Field(description="The new content to be written to the file.")
    ]

    # Log the params before validation
    # @root_validator(pre=True)
    # def log_params_during_validation(cls, values):
    #    logger.debug(
    #        f"Validating parameters: {values}"
    #    )  # Log the parameters being validated
    #    return values


def edit_file_tool(params: FileToolParams) -> str:
    """
    Edit an existing file or create a new one if it doesn't exist.
    The file's content is replaced entirely with the new content,
    while preserving its structure intact (e.g., line endings and formatting).

    Request Body Parameters:
    - file_path (str): The full file path of the file to be edited.
    - new_content (str): The new content to be written to the file.

    Example Request Body:
    {
        "file_path": "/home/user/file.txt",
        "new_content": "This is the new content of the file."
    }
    """
    if not params.file_path or not params.new_content:
        logger.error("file_path and new_content are required!")
        return json.dumps({"error": "file_path and new_content are required"})

    logger.info(f"Editing file: {params.file_path} with new content.")

    try:
        # Open file (create if missing)
        with open(params.file_path, "w+", encoding="utf-8") as f:
            f.write(params.new_content)  # Write new content
            f.truncate()  # Ensure no leftover content

        logger.info(f"File updated successfully: {params.file_path}")
        return (
            json.dumps(
                {"message": "File updated successfully", "file_path": params.file_path}
            ),
        )

    except Exception as e:
        logger.error(
            f"Failed to update file: {params.file_path}, error: {str(e)}", exc_info=True
        )
        return json.dumps({"error": f"Failed to update file: {str(e)}"})
