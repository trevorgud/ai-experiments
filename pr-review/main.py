import argparse

from openai import OpenAI
from dotenv import load_dotenv

from review_file import review_file
from git import list_files_changed
from git import git_fetch_refs, git_checkout_source
from git import GitDiffCommitParams, GitDiffBranchParams


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
  parser.add_argument('--source-branch', help='The source branch of the PR (ex: feature branch)', dest="source_branch")
  parser.add_argument('--target-branch', default='main', help='The target branch of the PR (ex: main)', dest="target_branch")
  args = parser.parse_args()

  git_params = None
  if args.start_commit and args.end_commit:
    git_params = GitDiffCommitParams(
      repo_path=args.repo_path,
      start_commit=args.start_commit,
      end_commit=args.end_commit
    )
  elif args.source_branch and args.target_branch:
    git_params = GitDiffBranchParams(
      repo_path=args.repo_path,
      source_branch=args.source_branch,
      target_branch=args.target_branch
    )
    git_fetch_refs(git_params)
    git_checkout_source(git_params)
  else:
    raise Exception(f"invalid cli args: {args}")

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
