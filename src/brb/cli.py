from typing import Annotated
import os
from dotenv import set_key, load_dotenv
from rich import print as rprint
from rich.panel import Panel
from rich.pretty import pprint

from brb.saving.find_commands import find_commands
from brb.saving.save_message import Saving
from brb.llm.AgentLLM import GeminiLLM

import typer

ENV_PATH = os.path.expanduser("~/.brb/.env")
load_dotenv(ENV_PATH)
app = typer.Typer(help="CLI tool")

@app.command(name="save", help="Save last work details")
def save(
        message: Annotated[str, typer.Argument(help="Last session")] = "Last session",
        limit: Annotated[int, typer.Option("--limit", help="Number of last messages to be saved")] = 10,
        aisave: Annotated[bool, typer.Option("--ai", help="Create a small text from AI to understand")] = False
) -> None:
    geminiapikey = os.environ.get("GEMINI_API_KEY")
    msg = Saving(message, find_commands(limit), GeminiLLM(geminiapikey) if aisave else None)
    pass

@app.command(name="set-key", help="Set the Gemini API Key")
def setkey(
    key: Annotated[str, typer.Argument(help="Gemini API Key")]
) -> None:
    os.makedirs(os.path.dirname(ENV_PATH), exist_ok=True)
    set_key(ENV_PATH, "GEMINI_API_KEY", key)

@app.command(name="resume")
def resume():
    print("resume")

if __name__ == "__main__":
    app()