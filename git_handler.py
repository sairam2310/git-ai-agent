import subprocess
from db import get_github_credentials
from stash_utils import stash_with_custom_message
from commit_utils import get_project_name_from_branch, get_first_changed_filename
from constants import GIT_COMMANDS

def pull_code():
    try:
        # 1. Get GitHub credentials
        username, token = get_github_credentials()
        if not token:
            return {
                "status": "error",
                "message": "GitHub token not found. Please authenticate first."
            }

        # 2. Set token-based remote URL
        subprocess.run(
       GIT_COMMANDS["REMOTE_SET_URL"] + [f"https://{username}:{token}@github.com/{username}/git-ai-agent.git"],
        check=True)

        # 3. Stash current changes with custom message
        stash_with_custom_message()

        # 4. Pull from remote
        subprocess.run(GIT_COMMANDS["PULL"], check=True)

        # 5. Apply most recent stash (stash@{0})
        subprocess.run(GIT_COMMANDS["STASH_APPLY"].split() + ["stash@{0}"], capture_output=True, text=True)


        # 6. Check for merge conflicts
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


def commit_code(issue_description):
    try:
        project = get_project_name_from_branch()
        component = get_first_changed_filename()

        message = f"{project} :: {component} :: {issue_description}"

        # ✅ Only stage tracked changes
        subprocess.run(GIT_COMMANDS["ADD_UPDATED"], check=True)
        subprocess.run(GIT_COMMANDS["COMMIT"] + [message], check=True)

        return {
            "status": "success",
            "message": f"Committed: {message}"
        }

    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "message": f"Commit failed: {e}"
        }


