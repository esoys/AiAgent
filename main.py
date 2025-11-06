import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file_content import schema_write_file_content, write_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file_content,
    ]
)


if len(sys.argv) > 1:
    user_prompt = sys.argv[1] if sys.argv[1] != "--verbose" else sys.argv[2]
else:
    raise Exception("No prompt given. Write prompt after 'main.py' in quotes!")
    sys.exit(1)

messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    ),
)

if response.function_calls:
    verbose = "--verbose" in sys.argv

    for function_call_part in response.function_calls:
        function_result = call_function(function_call_part, verbose=verbose)

        if (
            not function_result.parts
            or not getattr(function_result.parts[0], "function_response", None)
            or not function_result.parts[0].function_response.response
        ):
            raise RuntimeError(
                "Function call did not return a function_response with a response"
            )

        if verbose:
            print(f"-> {function_result.parts[0].function_response.response}")
        # print(f"Calling function: {function_call_part.name}({function_call_part.args})")
else:
    if "--verbose" in sys.argv:
        print(
            f"Response:  {response.text}\nUser prompt: {user_prompt}\nPrompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}"
        )
    else:
        print(f"Response:  {response.text}")
