import os
from google.genai import types


def write_file_content(working_directory, file_path, content):
    working_abs_path = os.path.abspath(working_directory)
    file_abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    dir_name = os.path.dirname(file_abs_path)

    try:
        if not file_abs_path.startswith(working_abs_path):
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)

        with open(file_abs_path, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {e}"


schema_write_file_content = types.FunctionDeclaration(
    name="write_file_content",
    description="Overwrites the contents of a specified File. Creates File and Directory if they don't exist, path is relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the file to write.",
            ),
            "content": types.Schema(
                type=types.Type.STRING, description="The Content to write in the File."
            ),
        },
        required=["file_path", "content"],
    ),
)
