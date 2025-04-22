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

  # Invalidate certain skipped files.
  all_files = set(files_changed)
  invalid_files = set()
  for file in files_changed:
    for skip in SKIP_FILES:
      if file.endswith(skip):
        invalid_files.add(file)
  valid_files = all_files.difference(invalid_files)

  return list(valid_files)
