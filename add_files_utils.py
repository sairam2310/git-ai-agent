import subprocess
import os

def list_changed_files():
    """Returns a list of modified, deleted, and untracked files."""
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')
    
    changed_files = []
    for line in lines:
        if not line.strip():
            continue
        file_path = line[3:].strip()
        changed_files.append(file_path)

    return changed_files



