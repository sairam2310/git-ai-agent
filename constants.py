# constants.py

GIT_COMMANDS = {
    "ADD_UPDATED": ["git", "add", "-u"],
    "ADD_ALL": ["git", "add", "."],
    "COMMIT": ["git", "commit", "-m"],
    "PULL": ["git", "pull"],
    "PUSH": ["git", "push"],
    "REMOTE_SET_URL": ["git", "remote", "set-url", "origin"],
    "BRANCH_NAME": ["git", "rev-parse", "--abbrev-ref", "HEAD"],
    "CHANGED_FILES": ["git", "status", "--porcelain"],
    "STASH_PUSH": ["git", "stash", "push", "-m"],
    "STASH_LIST": ["git", "stash", "list"],
    "STASH_APPLY": "git stash apply",  # base command (use with stash@{0})
    "STASH_SHOW": "git stash show"     # base command (add stash@{0} and --name-only)
}
