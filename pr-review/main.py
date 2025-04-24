import argparse

from openai import OpenAI
from dotenv import load_dotenv
from config import *

from review_file import review_file
from git import list_files_changed
from git import GitParams


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
  parser = argparse.ArgumentParser(
    prog='AI PR Review',
    description='Review a given PR with AI prompting',
  )
  parser.add_argument('--repo-path', help='The path of the git repo', dest="repo_path")
  parser.add_argument('--start-commit', help='The starting commit of the PR', dest="start_commit")
  parser.add_argument('--end-commit', help='The ending commit of the PR', dest="end_commit")
  args = parser.parse_args()

  git_params = GitParams(
    repo_path=args.repo_path,
    start_commit=args.start_commit,
    end_commit=args.end_commit
  )

  client = OpenAI()

  files = list_files_changed(git_params)
  print(files)
  bugs = []
  for file in files:
    file_bugs = review_file(client, file, git_params)
    for bug in file_bugs:
      bug["file"] = file
      bug["priority"] = priority_metric(bug)
      bugs.append(bug)

  bugs = sorted(bugs, key=lambda d: d['priority'])

  for bug in bugs:
    print_review_item(bug)


if __name__ == "__main__":
  main()
