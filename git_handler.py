import subprocess
from db import  get_github_credentials
def pull_code():
    try:
        # Get GitHub credentials from the database
        username, token = get_github_credentials()
        if not token:
            return {"status": "error", "message": "GitHub token not found. Please authenticate first."}
       # Set token-based origin URL
        subprocess.run(["git", "remote", "set-url", "origin",
                        f"https://{username}:{token}@github.com/{username}/git-ai-agent.git"], check=True)

        # 1. Stash local changes
        subprocess.run(["git", "stash"], check=True)

        # 2. Pull from remote
        subprocess.run(["git", "pull"], check=True)

        # 3. Apply stashed changes
        stash_apply = subprocess.run(
            ["git", "stash", "apply"],
            capture_output=True, text=True
        )

        # 4. Check for conflicts
        if "CONFLICT" in stash_apply.stdout or "CONFLICT" in stash_apply.stderr:
            return {
                "status": "conflict",
                "message": "Merge conflict detected during stash apply. Please resolve manually."
            }

        return {
            "status": "success",
            "message": "Code pulled and stash applied successfully."
        }

    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "message": f"Git operation failed: {e}"
        }
