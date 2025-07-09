import subprocess
from db import get_github_credentials
from stash_utils import stash_with_custom_message,extract_conflicted_files
from commit_utils import get_project_name_from_branch, get_first_changed_filename
from constants import GIT_COMMANDS
from add_files_utils import list_changed_files

def pull_code():
    try:
        username, token = get_github_credentials()
        if not token:
            return {"status": "error", "message": "GitHub token not found. Please authenticate first."}

        subprocess.run(
            GIT_COMMANDS["REMOTE_SET_URL"] + [f"https://{username}:{token}@github.com/{username}/git-ai-agent.git"],
            check=True
        )

        stash_with_custom_message()

        subprocess.run(GIT_COMMANDS["PULL"], check=True)

        stash_apply = subprocess.run(
            GIT_COMMANDS["STASH_APPLY"].split() + ["stash@{0}"],
            capture_output=True, text=True
        )

        if "CONFLICT" in stash_apply.stdout or "CONFLICT" in stash_apply.stderr:
            conflicted_files = extract_conflicted_files(output)
            return {
                "status": "conflict",
                "message": "Merge conflict detected during stash apply. Please resolve manually.",
                "conflicted_files": conflicted_files
            }

        return {
            "status": "success",
            "message": "Code pulled and stash applied successfully."
        }

    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": f"Git operation failed: {e}"}

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


def commit_code(issue_description, mode):
    """
    Commits code changes with a structured message.
    mode = "tracked" -> git add -u (default)
    mode = "all"     -> git add .
    mode = "manual"  -> reserved for manual add before calling this
    """
    try:
        project = get_project_name_from_branch()
        component = get_first_changed_filename()

        message = f"{project} :: {component} :: {issue_description}"

        # Step 1: Stage files
        if mode == "tracked":
            subprocess.run(GIT_COMMANDS["ADD_UPDATED"], check=True)
        elif mode == "all":
            subprocess.run(GIT_COMMANDS["ADD_ALL"], check=True)
        elif mode == "manual":
            pass  # Assume user already staged files
    
        changed_files = list_changed_files()
        print("Files changed:\n", changed_files)
    
        # Step 2: Commit
        subprocess.run(GIT_COMMANDS["COMMIT"] + [message], check=True)

        # Optional: verify working tree is clean
        status = subprocess.run(["git", "status"], capture_output=True, text=True)
        if "nothing to commit" in status.stdout:
            msg = "Committed cleanly. Working tree is clean."
        else:
            msg = "Committed, but some files may still be untracked or unstaged."

        return {
            "status": "success",
            "message": f"{msg}\nCommit\n: {message}"
        }

    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "message": f"Commit failed: {e}"
        }

        
def push_code():
    try:
        # 1. Get credentials
        username, token = get_github_credentials()
        if not token:
            return {"status": "error", "message": "GitHub token not found. Please authenticate first."}

        # 2. Set remote URL with token
        remote_url = f"https://{username}:{token}@github.com/{username}/git-ai-agent.git"
        subprocess.run(GIT_COMMANDS["REMOTE_SET_URL"] + [remote_url], check=True)

        # 3. Push
        subprocess.run(GIT_COMMANDS["PUSH"], check=True)

        return {"status": "success", "message": "Code pushed to GitHub successfully."}

    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": f"Git push failed: {e}"}

