from utils.application.logger import logger
from mcp.server.fastmcp import Context
from typing_extensions import Annotated
from pydantic import Field
import subprocess
import json


def execute_command_tool(
    command: Annotated[
        str,
        Field(description="The command to be executed. Ex: ls -lah /path/to/directory"),
    ],
    ctx: Context,
) -> str:
    """
    Execute a shell command on the local machine and return the output.
    This can include tasks such as interacting with the filesystem, managing Git repositories, or performing system operations.

    Request Body Parameters:
    - command (str): Required, the shell command to execute.

    Example Commands:
    - Check the status of a Git repository:
      "git status"

    - Add a file to the Git staging area:
      "git add /path/to/file"

    - Commit changes to the Git repository:
      "git commit -m 'Commit message'"

    - Push changes to a remote Git repository:
      "git push origin main"

    - Create a new directory:
      "mkdir /path/to/newdirectory"

    - List the contents of a directory:
      "ls -lah /path/to/directory"

    """
    output = []  # List to store command output

    if not command:
        return json.dumps({"error": "Missing command parameter"})

    try:
        logger.info(f"Executing command: {command}")
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Capture both stdout and stderr in real-time
        while True:
            stdout_line = process.stdout.readline()
            stderr_line = process.stderr.readline()

            if stdout_line:
                logger.info(stdout_line.strip())  # Log it
                output.append(stdout_line.strip())  # Collect stdout

            if stderr_line:
                logger.info(stderr_line.strip())  # Log it
                output.append(stderr_line.strip())  # Collect stderr

            if stdout_line == "" and stderr_line == "" and process.poll() is not None:
                break  # Process is finished

        # Check if the process failed
        return_code = process.wait()
        if return_code != 0:
            logger.error(f"Command failed with exit code {return_code}")
            output.append(f"Error: Command failed with exit code {return_code}")

    except Exception as e:
        logger.error(f"Error while executing the command: {e}")
        output.append(f"Error: {str(e)}")

    return json.dumps({"command": command, "output": output})
