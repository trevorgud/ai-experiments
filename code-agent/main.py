from openai import OpenAI
from dotenv import load_dotenv
from api import code_api, validate_request
from response_format import response_format
from config import *
import json

# OPENAI_API_KEY loaded here
load_dotenv()

client = OpenAI()

system_prompt = """
  You are an agent that uses a request based API to find bugs in a git repo.
  Keep requesting until you are confident you have found a bug or I tell you to stop.
  If I give back an error you can't recover from then terminate early and tell me why in the final answer.
  Sample requests: ```
  { "action": "tree", "params": {"start": "/", "depth": 2} }
  { "action": "tree", "params": {"start": "/src/components", "depth": 1} }
  { "action": "file", "params": {"path": "/src/components/WeatherIcon.js"} }
  { "action": "done", "params": {"final_answer": "<describe all potential bugs>"} }
  ```
  Use "tree" to find an initial source code file. Output the file with "file".
  Use absolute paths to reference every file. When encountering an import with relative path, infer which absolute path it referes to.
  Based on that file, decide another file you might want to see. Find its location with "tree" if needed.
  Prioritize source files: .go .cpp .hpp .js .py
"""

myinput=[
  {"role": "system", "content": system_prompt},
  {"role": "user", "content": "go ahead and search for bugs, share the first request."},
]
response = client.responses.create(
  model="gpt-4.1",
  input=myinput,
  text=response_format,
)

def json_err(e):
  f"Please reply with only JSON. Error parsing last JSON: {e}"

next_prompt = ""
count = 0
tree_count = 0
while count < max_loop:
  print("gpt: " + response.output_text)
  if "final_answer" in response.output_text:
    break
  try:
    request = json.loads(response.output_text)
    invalid_reason = validate_request(request)
    if invalid_reason:
      next_prompt = invalid_reason
    else:
      if request["action"] == "tree":
        tree_count += 1
      response = code_api(request)
      next_prompt = response
  except Exception as e:
    next_prompt = json_err(e)
  if tree_count >= 3:
    next_prompt += "\nyou have requested tree many times, please try requesting file action\n"
    tree_count = 0
  next_prompt += "\nplease continue searching for bugs"

  print("me: " + next_prompt)
  response = client.responses.create(
    model="gpt-4.1",
    input=next_prompt,
    text=response_format,
  )
  count += 1

if "final_answer" not in response.output_text:
  final_prompt = f"""
    You have exceeded the max loop: {max_loop}
    Please respond with a final answer.
  """
  response = client.responses.create(
    model="gpt-4.1",
    input=final_prompt,
    text=response_format,
  )

print("gpt(final):" + response.output_text)


# request = {
#   "action": "tree",
#   "start": "/",
#   "depth": 3,
# }
# # request = {
# #   "action": "file",
# #   "path": "/package.json",
# # }
# is_invalid = validate_request(request)
# print(is_invalid)
# response = code_api(request)
# print(response)
