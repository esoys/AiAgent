import os
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

        if len(file_content) > 10000:
            return (
                f'[{file_content[:10000]} "{file_path}" truncated at 10000 characters]'
            )

        return file_content

    except Exception as e:
        return f"Error: {e}"
