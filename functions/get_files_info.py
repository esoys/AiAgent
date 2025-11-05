import os


def get_files_info(working_directory, directory="."):
    working_abs_path = os.path.abspath(working_directory)
    target_abs_path = os.path.abspath(os.path.join(working_directory, directory))

    try:
        if not os.path.isdir(target_abs_path):
            return f'Error: "{directory}" is not a directory'

        if target_abs_path == working_abs_path or target_abs_path.startswith(
            working_abs_path + os.sep
        ):
            file_list = f"Result for '{directory}' directory:\n"
            for file in os.listdir(target_abs_path):
                file_list += f"- {file}: files_size={os.path.getsize(target_abs_path + os.sep + file)}, is_dir={os.path.isdir(target_abs_path + os.sep + file)}\n"

            return file_list

        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    except Exception as e:
        return f"Error: {e}"
