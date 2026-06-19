import pytest
from unittest.mock import patch, mock_open
from brb.saving.find_commands import find_commands

# We define some fake shell history content
MOCK_BASH_HISTORY = """
ls
cd src
python -m pytest
"""

MOCK_ZSH_HISTORY = """
: 1610000000:0;ls
: 1610000010:0;cd src
: 1610000020:0;brb save
"""

@patch("os.environ.get")
@patch("builtins.open", new_callable=mock_open, read_data=MOCK_BASH_HISTORY)
def test_find_commands_bash(mock_file, mock_env):
    """Test that Bash history is parsed correctly."""
    # Tell the function it's running in Bash
    mock_env.return_value = "/bin/bash"
    
    # Request the last 2 commands
    commands = find_commands(2)
    
    assert len(commands) == 2
    assert commands == ["cd src", "python -m pytest"]
    # Verify it tried to open the bash history file
    assert ".bash_history" in mock_file.call_args[0][0]

@patch("os.environ.get")
@patch("builtins.open", new_callable=mock_open, read_data=MOCK_ZSH_HISTORY)
def test_find_commands_zsh(mock_file, mock_env):
    """Test that Zsh history strips timestamps correctly."""
    # Tell the function it's running in Zsh
    mock_env.return_value = "/bin/zsh"
    
    commands = find_commands(3)
    
    assert len(commands) == 3
    # Timestamps should be gone
    assert commands == ["ls", "cd src", "brb save"]

@patch("os.environ.get")
def test_find_commands_no_shell(mock_env):
    """Test behavior when SHELL env var is missing or unknown."""
    mock_env.return_value = ""
    commands = find_commands(5)
    assert commands == []

@patch("os.environ.get")
@patch("builtins.open", side_effect=FileNotFoundError)
def test_find_commands_missing_file(mock_file, mock_env):
    """Test behavior when the history file doesn't exist."""
    mock_env.return_value = "/bin/bash"
    commands = find_commands(5)
    assert commands == []
