from typing import Annotated
import os
from dotenv import set_key, load_dotenv

from brb.saving.models import Session
from brb.saving.find_commands import find_commands
from brb.saving.git_utils import get_git_info, stash_dirty_files, pop_stash
from brb.llm.AgentLLM import GeminiLLM

from brb.database.database import Database

from brb.ui.display import display_session

import typer

ENV_PATH = os.path.expanduser("~/.brb/.env")
load_dotenv(ENV_PATH)
app = typer.Typer(help="CLI tool")

_db = None

def get_db() -> Database:
    global _db
    if _db is None:
        _db = Database()
        _db.init_db()
    return _db

@app.command(name="save", help="Save last work details")
def save(
        message: Annotated[str, typer.Argument(help="Last session")] = "Last session",
        limit: Annotated[int, typer.Option("--limit", help="Number of last messages to be saved")] = 10,
        aisave: Annotated[bool, typer.Option("--ai", help="Create a small text from AI to understand")] = False,
        stash: Annotated[bool, typer.Option("--stash", help="Create a stash of all dirty files from git")] = False,
) -> None:
    commands = find_commands(limit)
    branch, status = get_git_info()

    if aisave:
        gemini = GeminiLLM(os.environ.get("GEMINI_API_KEY"))
        message = gemini.createMessage(message, commands)

    sess = Session(
        folder = os.getcwd(),
        message = message,
        commands = commands,
        git_branch = branch,
        git_status = status,
    )
    sess = get_db().insert_session(sess)

    if stash:
        stash_dirty_files(sess.id)
        
    typer.echo("Session saved!")

@app.command(name="set-key", help="Set the Gemini API Key")
def setkey(
        key: Annotated[str, typer.Argument(help="Gemini API Key")]
) -> None:
    os.makedirs(os.path.dirname(ENV_PATH), exist_ok=True)
    set_key(ENV_PATH, "GEMINI_API_KEY", key)

@app.command(name="resume")
def resume(
        session_id: Annotated[int|None, typer.Argument(help="Specific session ID")] = None,
        here: Annotated[bool, typer.Option("--here", help="Resume the last session that was saved at this path")] = False,
        pop: Annotated[bool, typer.Option("--pop", help="Restore stashed files for this session")] = False,
):
    db = get_db()
    if session_id:
        session = db.fetch_session_by_id(session_id)
    elif here:
        session = db.fetch_last_session_by_folder(os.getcwd())
    else:
        session = db.fetch_last_session()

    if not session:
        print("No session found!")
        return

    display_session(session)

    if pop:
        pop_stash(session.id)

@app.command(name="list")
def list(
        limit: Annotated[int, typer.Option("--limit", help="Number of last messages to be displayed")] = 5,
        show_commands: Annotated[bool, typer.Option("--show_commands", help="Show commands")] = False
):
    listsession = get_db().fetch_all_sessions()[:limit]
    for session in listsession:
        if not show_commands:
            session.commands = []
        display_session(session)

if __name__ == "__main__":
    app()