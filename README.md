# BeRightBack (brb)

A CLI tool to snapshot your work context before stepping away and resume it instantly when you're back.

## What it does

- `brb save` — captures your current folder, last N terminal commands, and an optional note, then stores it in a local SQLite database
- `brb resume` — reprints your last saved session so you can pick up where you left off
- `brb set-key` — stores your Gemini API key for AI-generated session summaries

## Installation

**Requirements:** Python 3.12+

```bash
git clone <repo-url>
cd BRB

python3 -m venv .venv
source .venv/bin/activate

pip install -e .
```

## Shell setup (required for accurate history)

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

## Usage

```bash
# Save current context
brb save

# Save with a note describing what you were doing
brb save "working on auth module"

# Save with a custom number of commands (default: 10)
brb save "fixing the login bug" --limit 15

# Save with an AI-generated summary (requires API key)
brb save "refactoring db layer" --ai

# Resume last saved session
brb resume

# Set your Gemini API key
brb set-key <your-api-key>
```

## Data storage

All data is stored locally at `~/.brb/`:
```
~/.brb/
├── brb.db   # SQLite database of saved sessions
└── .env     # Gemini API key (never committed to git)
```

## Project structure

```
src/brb/
├── cli.py               # CLI commands (typer)
├── saving/
│   ├── models.py        # Abstract session model
│   ├── save_message.py  # Concrete session implementation
│   └── find_commands.py # Shell history reader
├── database/
│   └── database.py      # SQLite repository
├── llm/
│   ├── BaseLLM.py       # Abstract LLM interface
│   ├── AgentLLM.py      # Gemini implementation
│   └── errors.py        # Custom exceptions
└── ui/
    └── display.py       # Rich terminal output
```

## Dependencies

- [typer](https://typer.tiangolo.com/) — CLI framework
- [python-dotenv](https://pypi.org/project/python-dotenv/) — `.env` file support
- [google-genai](https://pypi.org/project/google-genai/) — Gemini API client
- [rich](https://rich.readthedocs.io/) — terminal formatting
