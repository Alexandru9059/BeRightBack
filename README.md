# BeRightBack (brb)

A CLI tool to snapshot your work context before stepping away and resume it instantly when you're back.

## Installation Guide

**Requirements:** Python 3.12+

```bash
git clone <repo-url>
cd BRB

python3 -m venv .venv
source .venv/bin/activate

pip install -e .
```

### Shell setup (required for accurate history)

For `brb save` to capture your most recent commands, your shell needs to flush history to disk before each prompt.

**Bash** — add to `~/.bashrc`:
```bash
export PROMPT_COMMAND="history -a"
```

**Zsh** — add to `~/.zshrc`:
```zsh
setopt INC_APPEND_HISTORY
```

Then restart your terminal or `source` the file.

---

## How It Works

`brb` helps you safely step away from your codebase by capturing your current state. It saves your shell history, grabs your Git branch, optionally stashes your dirty (uncommitted) files, and even uses AI to summarize your progress. When you return, `brb` restores your context and optionally pops your stashed files right back into your working directory. All data is saved safely in a local SQLite database at `~/.brb/brb.db`.

### Command Reference

| Command | Usages & Options | Explanation |
| :--- | :--- | :--- |
| `brb save` | `brb save [message]`<br>`--limit <N>`<br>`--ai`<br>`--stash` | Saves your current session. Captures the last N terminal commands, current git status, and saves them to SQLite. `--stash` safely hides uncommitted files into git stash. `--ai` generates an intelligent summary using Gemini. |
| `brb resume` | `brb resume [id]`<br>`--here`<br>`--pop` | Resumes a saved session. Reprints your previous context. `--here` filters for the last session saved in the current folder. `--pop` instantly restores your stashed uncommitted files to your working directory. |
| `brb list` | `brb list`<br>`--limit <N>`<br>`--show_commands` | Lists the most recent saved sessions. `--limit` changes how many to display. `--show_commands` reveals the raw terminal history attached to each session. |
| `brb set-key` | `brb set-key <api_key>` | Stores your Google Gemini API key locally so `brb save --ai` can generate summaries. |
