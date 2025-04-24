from abc import ABC, abstractmethod
import subprocess

from config import *


class GitDiffParams(ABC):
  # @abstractmethod
  # def repo_path(self):
  #   pass

  @abstractmethod
  def diff_params(self):
    pass


class GitDiffCommitParams(GitDiffParams):
  def __init__(self, repo_path, start_commit, end_commit):
    self.repo_path = repo_path
    self.start_commit = start_commit
    self.end_commit = end_commit

  def diff_params(self):
    return [
      self.start_commit,
      self.end_commit,
    ]


class GitDiffBranchParams(GitDiffParams):
  def __init__(self, repo_path, source_branch, target_branch):
    self.repo_path = repo_path
    self.source_branch = source_branch
    self.target_branch = target_branch

  def diff_params(self):
    branch_expr = f"origin/{self.target_branch}...{self.source_branch}"
    return [
      branch_expr
    ]


def git_fetch_refs(params: GitDiffBranchParams):
  base_branch=params.target_branch
  pr_branch=params.source_branch
  # Remote to use, may need to be configurable later.
  remote = "origin"

  base_ref = f"refs/heads/{base_branch}:refs/remotes/{remote}/{base_branch}"
  pr_ref = f"refs/heads/{pr_branch}:refs/remotes/{remote}/{pr_branch}"

  command = [
    "git",
    "-C",
    params.repo_path,
    "fetch",
    "--prune",
    "--no-tags",
    remote,
    base_ref,
    pr_ref,
  ]
  subprocess.run(command, capture_output=True, text=True, check=True)


def git_checkout_source(params: GitDiffBranchParams):
  command = [
    "git",
    "-C",
    params.repo_path,
    "checkout",
    params.source_branch,
  ]
  subprocess.run(command, capture_output=True, text=True, check=True)


def git_diff(file_path, params):
  diff_params = params.diff_params()
  command = [
    "git",
    "-C",
    params.repo_path,
    "diff",
    # Spread the CLI params for this request in the appropriate location.
    *diff_params,
    "--",
    file_path,
  ]
  output = subprocess.run(command, capture_output=True, text=True, check=True)
  file_diff = output.stdout
  return file_diff


def list_files_changed(params):
  diff_params = params.diff_params()
  command = [
    "git",
    "-C",
    params.repo_path,
    "diff",
    "--name-only",
    # Spread the CLI params for this request in the appropriate location.
    *diff_params,
  ]
  output = subprocess.run(command, capture_output=True, text=True, check=True)
  result = output.stdout
  files_changed = result.split()

  # Invalidate certain skipped files.
  all_files = set(files_changed)
  invalid_files = set()
  for file in files_changed:
    for skip in SKIP_FILES:
      if file.endswith(skip):
        invalid_files.add(file)
  valid_files = all_files.difference(invalid_files)

  return list(valid_files)
