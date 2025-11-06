from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file_content import write_file_content
from functions.run_python_file import run_python_file

functions = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file_content": write_file_content,
    "run_python_file": run_python_file,
}


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    print(f" - Calling function: {function_call_part.name}")

    if function_call_part.name not in functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    func_result = functions[function_call_part.name](
        "./calculator", **function_call_part.args
    )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": func_result},
            )
        ],
    )
