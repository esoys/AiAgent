import os
from xxlimited import Error


def write_file(working_directory, file_path, content):
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
