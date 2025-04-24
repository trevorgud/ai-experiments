import json
import subprocess

from config import *
from git import git_diff


def persona_prompt(file_contents):
  task_description = f"""
    You are an expert in software tasked with reviewing this code.
    Your task is to review the diff for this code and look for various problems.
    Here is the full code file (after change): ```\n
  """
  prompt = task_description + file_contents
  return prompt


def format_prompt():
  return """
    Respond with a list of objects, or empty list if nothing found.
    Each item will have these fields:
    - description: a description of the findings
    - code_snippet: the snippet of code this entry refers to
    - start_line: the line in the file where the current snippet starts
    - end_line: the line in the file where the current snippet ends
    - confidence: how confident are you that this is a real finding (0-10)
    - severity: what is the severity of the finding (0-10)
    - effort: how much effort would be required to resolve (0-10)
    - category: give the finding a categorization
  """


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
              "code_snippet":  { "type": "string" },
              "start_line":    { "type": "integer" },
              "end_line":      { "type": "integer" },
              "confidence":    { "type": "number" },
              "severity":      { "type": "number" },
              "effort":        { "type": "number" },
              "category":      { "type": "string" }
            },
            "required": [
              "description",
              "code_snippet",
              "start_line",
              "end_line",
              "confidence",
              "severity",
              "effort",
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
def review_file(client, file_path, params):
  b = review_bugs(client, file_path, params)
  r = review_refactorings(client, file_path, params)
  reviews = [*b, *r]
  return reviews


def review_bugs(client, file_path, params):
  print(f"handling file for bugs {file_path}")
  file_contents = ""
  with open(params.repo_path+"/"+file_path, 'r') as file:
    file_contents = file.read()
  system_prompt = persona_prompt(file_contents)

  diff = git_diff(file_path, params)
  user_prompt = user_bug_prompt(diff)

  fp = format_prompt()

  prompts = [
    {"role": "system", "content": system_prompt},
    {"role": "system", "content": fp},
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


def review_refactorings(client, file_path, params):
  print(f"handling file for refactorings {file_path}")
  file_contents = ""
  with open(params.repo_path+"/"+file_path, 'r') as file:
    file_contents = file.read()
  system_prompt = persona_prompt(file_contents)

  diff = git_diff(file_path, params)
  user_prompt = user_refactoring_prompt(diff)

  fp = format_prompt()

  prompts = [
    {"role": "system", "content": system_prompt},
    {"role": "system", "content": fp},
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
