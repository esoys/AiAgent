import os
from google.genai import types
from config import FILE_MAX_CHARACTERS


def get_file_content(working_directory, file_path):
    working_abs_path = os.path.abspath(working_directory)
    file_abs_path = os.path.abspath(os.path.join(working_directory, file_path))

    try:
        if not file_abs_path.startswith(working_abs_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file_abs_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(file_abs_path, "r") as f:
            file_content = f.read()

        if len(file_content) > FILE_MAX_CHARACTERS:
            return f'[{file_content[:FILE_MAX_CHARACTERS]} "{file_path}" truncated at 10000 characters]'

        return file_content

    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Prints the content of the specified File, path is relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the file to read.",
            ),
        },
        required=["file_path"],
    ),
)
