import os
import subprocess
import functools
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    working_abs_path = os.path.abspath(working_directory)
    file_abs_path = os.path.abspath(os.path.join(working_directory, file_path))

    try:
        if not file_abs_path.startswith(working_abs_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(file_abs_path):
            return f'Error: File "{file_path}" not found.'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        completed_process = subprocess.run(
            ["python", file_path] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
            cwd=working_abs_path,
            text=True,
        )

        if not completed_process.stdout and not completed_process.stderr:
            return "No output produced."

        return f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}{f' Process exited with code {completed_process.returncode}' if completed_process.returncode != 0 else ''}"

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a given Python File, path is relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the file to execute.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Additional argumets to pass to the function",
            ),
        },
        required=["file_path"],
    ),
)
