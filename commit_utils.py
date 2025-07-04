import subprocess
import os
from constants import GIT_COMMANDS

def get_project_name_from_branch():
    result = subprocess.run(GIT_COMMANDS["BRANCH_NAME"], capture_output=True, text=True)
    branch_name = result.stdout.strip()
    return branch_name.replace("/", "-")  # optional: cleaner format

def get_first_changed_filename():
    result = subprocess.run(GIT_COMMANDS["CHANGED_FILES"], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')
    if lines and len(lines[0]) > 3:
        filepath = lines[0][3:]
        return os.path.splitext(os.path.basename(filepath))[0]
    return "UnknownComponent"
