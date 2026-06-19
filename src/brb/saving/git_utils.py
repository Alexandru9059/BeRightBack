import subprocess

def get_git_info() -> tuple[str|None, str|None]:
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check = True, stdout = subprocess.DEVNULL,
            stderr = subprocess.DEVNULL,
        )

        branch_proc = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output = True, text = True, check = True,
        )
        branch = branch_proc.stdout.strip() or "HEAD (detached)"

        status_proc = subprocess.run(
            ["git", "status", "--short"],
            capture_output = True, text = True, check = True,
        )
        status = status_proc.stdout.strip()

        return branch, status
    except (subprocess.CalledProcessError, FileNotFoundError):
        import sys
        print("Could not get git info. Could be due to git not being installed or the folder not being a git repo.", file=sys.stderr)
        return None, None