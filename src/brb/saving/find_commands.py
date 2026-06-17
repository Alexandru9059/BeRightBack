import os

def find_commands(command_number: int) -> list[str]:
    shell = os.environ.get("SHELL", "")

    if "zsh" in shell:
        history_path = os.path.expanduser("~/.zsh_history")
    elif "bash" in shell:
        history_path = os.path.expanduser("~/.bash_history")
    else:
        return []

    try:
        with open(history_path, "r", errors="ignore") as f:
            lines = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []

    lines = [line for line in lines if line]

    if "zsh" in shell:
        lines = [line.split(";", 1)[-1] if ";" in line else line for line in lines]

    return lines[-command_number:]

