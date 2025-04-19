import subprocess
from config import *

def validate_request(request):
  action = request.get("action")
  if action is None:
    return "must specify an action to perform"

  params = request.get("params")
  if params is None or type(params) != dict:
    return "invalid params specified for this action"

  if action == "tree":
    start = params.get("start")
    if start is None:
      return "tree action must have a start (path)"
    depth = params.get("depth")
    if depth is None:
      return "tree action must have a depth"
  elif action == "file":
    path = params.get("path")
    if path is None:
      return "file action must have a path"
  elif action == "done":
    final_answer = params.get("final_answer")
    if final_answer is None:
      return "done action must have a final_answer"
  else:
    return "invalid action type"

  return None


def code_api(request):
  response = ""
  action = request["action"]
  params = request["params"]
  if action == "tree":
    response = handle_tree_req(params)
  elif action == "file":
    response = handle_file_req(params)
  elif action == "done":
    response = "we are done, thanks!"
  else:
    response = f"invalid action: {action} respond with only `tree` or `file`"
  return response


def handle_tree_req(request):
  response = ""
  start = request["start"]
  depth = request["depth"]

  if start.startswith("."):
    return f"ERROR: please use absolute paths. Try to infer absolute source import path from previous tree requests."

  full_path = start
  if not full_path.startswith(git_path):
    full_path = git_path + full_path

  command = ["tree", "-fi", full_path, "-L", f"{depth}"]

  result = ""
  try:
    output = subprocess.run(command, capture_output=True, text=True, check=True)
    result = output.stdout
  except Exception as e:
    result = f"ERROR: failed finding tree path={full_path} depth={depth}: {e}"

  if len(result) > max_response:
    result = result[0:max_response]
    response += f"NOTE: truncating to {max_response} chars.\n"

  response += "RESPONSE: ```\n"
  response += result
  response += "```\n"

  return response


def handle_file_req(request):
  response = ""
  path = request["path"]

  if path.startswith("."):
    return f"ERROR: please use absolute paths. Try to infer absolute source import path from previous tree requests."

  full_path = path
  if not full_path.startswith(git_path):
    full_path = git_path + full_path
  result = ""
  try:
    with open(full_path, 'r') as file:
      result = file.read()
  except Exception as e:
    result = f"ERROR: failed finding file path={full_path}: {e}"

  if len(result) > max_response:
    result = result[0:max_response]
    response += f"NOTE: truncating to {max_response} chars.\n"

  response += "RESPONSE: ```\n"
  response += result

  return response
