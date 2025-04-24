import subprocess

from config import *


# TODO: Replace each func param set with this single param object.
class GitParams():
  def __init__(self, repo_path, start_commit, end_commit):
    self.repo_path = repo_path
    self.start_commit = start_commit
    self.end_commit = end_commit

  def diff_params(self):
    return [
      self.start_commit,
      self.end_commit,
    ]


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
