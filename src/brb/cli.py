from typing import Annotated
import os

from brb.saving.find_commands import find_commands
from brb.saving.save_message import Saving

import typer

app = typer.Typer(help="CLI tool")

@app.command(name="save", help="Save last work details")
def save(
        message: Annotated[str, typer.Argument(help="Last session")] = "Last session",
        limit: Annotated[int, typer.Option("--limit", help="Number of last messages to be saved")] = 10,
        aisave: Annotated[bool, typer.Option("--ai", help="Create a small text from AI to understand")] = False
) -> None:
    msg = Saving(message, find_commands(limit), None)
    print(msg.converttodict())

@app.command(name="set-key", help="Set the API Key")
def setkey(
    key: Annotated[str, typer.Argument(help="API Key")]
) -> None:
    pass

@app.command(name="resume")
def resume():
    print("resume")

if __name__ == "__main__":
    app()