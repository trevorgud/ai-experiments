import json
import subprocess

from config import *


def persona_prompt(file_contents):
  task_description = f"""
    You are an expert in software tasked with reviewing this code.
    Your task is to review the diff for this code and look for various problems.
    Here is the full code file (after change): ```\n
  """
  prompt = task_description + file_contents
  return prompt


def user_bug_prompt(diff):
  task = f"""Tell me if there are any bugs introduced in this change. If no bugs, leave an empty array. Here is the diff: ```\n"""
  prompt = task+diff
  return prompt


def issue_format(issue_type):
  return {
    "type": "json_schema",
    "name": issue_type,
    "schema": {
      "type": "object",
      "properties": {
        issue_type: {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "description":   { "type": "string" },
              "problem_code":  { "type": "string" },
              "start_line":    { "type": "integer" },
              "end_line":      { "type": "integer" },
              "severity":      { "type": "number" },
              "category":      { "type": "string" }
            },
            "required": [
              "description",
              "problem_code",
              "start_line",
              "end_line",
              "severity",
              "category"
            ],
            "additionalProperties": False
          },
        }
      },
      "required": [issue_type],
      "additionalProperties": False
    }
  }


def user_refactoring_prompt(diff):
  task = f"""Tell me if you would recommend any refactorings in this change. Here is the diff: ```\n"""
  prompt = task+diff
  return prompt

# def user_style_prompt(diff):
#   task = f"""Tell me if there are any style issues according to the style guide. Here is the diff: ```\n"""
#   prompt = task+diff
#   return prompt

# def style_guide_prompt(guide):
#   task = f"""Here is the style guide for my language: \n"""
#   prompt = task+guide
#   return prompt


# Review the given file between the diffs and return the relevant findings.
def review_file(client, file_path, start_commit, end_commit):
  b = review_bugs(client, file_path, start_commit, end_commit)
  r = review_refactorings(client, file_path, start_commit, end_commit)
  reviews = [*b, *r]
  return reviews


def review_bugs(client, file_path, start_commit, end_commit):
  print(f"handling file for bugs {file_path}")
  file_contents = ""
  with open(REPO+"/"+file_path, 'r') as file:
    file_contents = file.read()
  system_prompt = persona_prompt(file_contents)

  diff = git_diff(file_path, start_commit, end_commit)
  user_prompt = user_bug_prompt(diff)

  prompts = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt},
  ]
  response_format = {"format": issue_format("bugs")}
  response = client.responses.create(
    model="gpt-4.1",
    input=prompts,
    text=response_format,
  )
  j = json.loads(response.output_text)
  return j["bugs"]


def review_refactorings(client, file_path, start_commit, end_commit):
  print(f"handling file for refactorings {file_path}")
  file_contents = ""
  with open(REPO+"/"+file_path, 'r') as file:
    file_contents = file.read()
  system_prompt = persona_prompt(file_contents)

  diff = git_diff(file_path, start_commit, end_commit)
  user_prompt = user_refactoring_prompt(diff)

  prompts = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt},
  ]
  response_format = {"format": issue_format("refactorings")}
  response = client.responses.create(
    model="gpt-4.1",
    input=prompts,
    text=response_format,
  )
  j = json.loads(response.output_text)
  return j["refactorings"]


def git_diff(file_path, start_commit, end_commit):
  command = [
    "git",
    "-C",
    REPO,
    "diff",
    start_commit,
    end_commit,
    "--",
    file_path,
  ]
  output = subprocess.run(command, capture_output=True, text=True, check=True)
  file_diff = output.stdout
  return file_diff
