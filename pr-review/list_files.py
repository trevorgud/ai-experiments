import subprocess
from config import *


def list_files_changed(start_commit, end_commit):
  command = [
    "git",
    "-C",
    REPO,
    "diff",
    "--name-only",
    start_commit,
    end_commit,
  ]
  output = subprocess.run(command, capture_output=True, text=True, check=True)
  result = output.stdout
  files_changed = result.split()
  return files_changed
