import os
import sys
import functools
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

if len(sys.argv) > 1:
    user_prompt = sys.argv[1] if sys.argv[1] != "--verbose" else sys.argv[2]
else:
    raise Exception("No prompt given. Write prompt after 'main.py' in quotes!")
    sys.exit(1)

messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
)

if "--verbose" in sys.argv:
    print(
        f"Response:  {response.text}\nUser prompt: {user_prompt}\nPrompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}"
    )
else:
    print(f"Response:  {response.text}")
