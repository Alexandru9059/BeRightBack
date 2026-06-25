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


def stash_dirty_files(id: int):
    try:
        stat_proc = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output = True, text = True
        )
        stat = stat_proc.stdout.strip()
        if not stat:
            return

        subprocess.run(
            ["git", "stash", "push", "-u", "-m", f"brb-session-{id}"],
            check = True
        )

    except (subprocess.CalledProcessError, Exception) as e:
        print("Error in stashing dirty files from git")
        pass


def get_stashed_files(session_id: int) -> list[str] | None:
    try:
        list_proc = subprocess.run(
            ["git", "stash", "list"],
            capture_output=True,
            text=True,
            check=True
        )

        stash_ref = None
        for line in list_proc.stdout.splitlines():
            if f"brb-session-{session_id}" in line:
                stash_ref = line.split(":")[0].strip()
                break

        if not stash_ref:
            return None

        show_proc = subprocess.run(
            ["git", "stash", "show", "--name-only", stash_ref],
            capture_output=True,
            text=True,
            check=True
        )

        files = [f.strip() for f in show_proc.stdout.splitlines() if f.strip()]
        return files

    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def pop_stash(session_id: int):
    try:
        list_proc = subprocess.run(
            ["git", "stash", "list"],
            capture_output=True,
            text=True,
            check=True
        )

        stash_ref = None
        for line in list_proc.stdout.splitlines():
            if f"brb-session-{session_id}" in line:
                stash_ref = line.split(":")[0].strip()
                break

        if stash_ref:
            subprocess.run(
                ["git", "stash", "pop", stash_ref],
                check=True
            )
            print(f"📦 Successfully restored stashed files from {stash_ref}!")
        else:
            print(f"No stash found for session {session_id}.")

    except subprocess.CalledProcessError:
        print("Failed to pop the stash. You might have merge conflicts to resolve.")
