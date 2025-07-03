# 🤖 Git AI Agent

A smart personal assistant that helps automate Git operations like `pull`, `commit`, and `push` using natural language commands. Designed to streamline daily development workflows for individual developers.

---

## 🚀 Features

- 🔄 **Smart Pull**: Automatically stashes changes, pulls the latest code, and reapplies changes.
- 💬 **Natural Command Interface**: Use prompts like “commit UI changes” or “push my work”.
- 📝 **Structured Commits**: Follows the format: `UI :: project name :: component name`.
- 🗃️ **Command History**: Logs Git actions for audit and review.
- 🔐 **Secure Credentials**: GitHub credentials stored safely in a local database.
- 📁 **File Tracking**: Detects and lists changed files before committing.

---

## 🧠 How It Works

1. You enter a natural prompt like:  
   `"commit Login :: AuthApp :: login-page"`
2. The AI agent:
   - Detects changed files
   - Adds them to staging
   - Creates a commit message as per your format
   - Executes Git commands behind the scenes

---

## 🛠️ Tech Stack

- **Python** – Core logic and scripting
- **Git CLI** – Git operations
- **SQLite / MySQL** – Credential and history storage
- **OpenAI / LLM API** *(planned)* – For natural prompt parsing
- **Flask / CLI** – Interface layer (optional)

---

## ⚙️ Setup Instructions

```bash
# Clone the repository
git clone https://github.com/yourusername/git-ai-agent.git
cd git-ai-agent

# Install dependencies
pip install -r requirements.txt

# Run the agent
python agent.py
