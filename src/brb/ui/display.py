from rich import print as rprint
from rich.panel import Panel

def display_session(session: dict|None) -> None:
    if session is None:
        rprint("No session found")
        return

    commands_str = "\n".join(f"  {i+1}. {c}" for i, c in enumerate(session['commands']))

    content = (
        f"[bold]Folder:[/bold]     {session['folder']}\n"
        f"[bold]Saved at:[/bold]   {session['created_at']}\n"
        f"[bold]Message:[/bold]    {session['message']}\n"
        f"[bold]Commands:[/bold]\n"
        f"{commands_str}"
    )
    rprint(Panel(content, title = "Last BRB Session", border_style = "blue"))
