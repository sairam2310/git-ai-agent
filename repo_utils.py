# utils/repo_utils.py
import subprocess

def detect_repo_info():
    try:
        # Get origin URL
        remote_url = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True
        ).stdout.strip()

        # Get branch
        branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True
        ).stdout.strip()

        # Parse owner and repo
        repo_name = remote_url.split("/")[-1].replace(".git", "")
        owner = remote_url.split("/")[-2]

        return {
            "owner": owner,
            "repo": repo_name,
            "branch": branch
        }

    except Exception as e:
        return {"error": str(e)}
