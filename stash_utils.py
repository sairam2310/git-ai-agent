import subprocess
import os
import datetime

def list_stashes():
    result = subprocess.run(["git", "stash", "list"], capture_output=True, text=True)
    return result.stdout.strip().split('\n')

def get_files_in_stash(index=0):
    result = subprocess.run(
        ["git", "stash", "show", f"stash@{{{index}}}", "--name-only"],
        capture_output=True, text=True
    )
    return result.stdout.strip().split('\n')

def get_changed_files():
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')
    return [line[3:] for line in lines if line]

def extract_filename(filepath):
    return os.path.splitext(os.path.basename(filepath))[0]

def create_stash_message():
    changed_files = get_changed_files()
    if not changed_files:
        return None

    filename = extract_filename(changed_files[0])  # Use first changed file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%I%M%p")

    return f"{filename}_{timestamp}"

def stash_with_custom_message():
    message = create_stash_message()
    if message:
        subprocess.run(["git", "stash", "push", "-m", f"Modified {message}"], check=True)
        print(f"✅ Stashed: Modified {message}")
    else:
        print("⚠️ No changes to stash.")

def extract_conflicted_files(output):
    conflicted = []
    for line in output.splitlines():
        if "CONFLICT (content)" in line:
            parts = line.split(" in ")
            if len(parts) == 2:
                conflicted.append(parts[1].strip())
    return conflicted

