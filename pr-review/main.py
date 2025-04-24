from openai import OpenAI
from dotenv import load_dotenv
from config import *

from review_file import review_file
from git import list_files_changed


# OPENAI_API_KEY loaded here
load_dotenv()


def print_review_item(item):
  for key, value in item.items():
    # key name, then a newline, then the value
    print(f"{key}:\n{value}\n")
  print("========")


def priority_metric(item):
  severity = item["severity"]
  effort = item["effort"]
  confidence = item["confidence"]
  pad = 0.01
  pm = (severity + confidence) / (effort + pad)
  return pm


def main():
  client = OpenAI()

  # TODO: The repo path should be a CLI param
  # TODO: The commits should be CLI params
  start_commit = "417d46676057"
  end_commit = "03467aa1b66a5"

  files = list_files_changed(start_commit, end_commit)
  print(files)
  bugs = []
  for file in files:
    file_bugs = review_file(client, file, start_commit, end_commit)
    for bug in file_bugs:
      bug["file"] = file
      bug["priority"] = priority_metric(bug)
      bugs.append(bug)

  bugs = sorted(bugs, key=lambda d: d['priority'])

  for bug in bugs:
    print_review_item(bug)


if __name__ == "__main__":
  main()
