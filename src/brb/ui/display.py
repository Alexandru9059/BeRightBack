from rich import print as rprint
from rich.panel import Panel
from brb.saving.models import Session
from brb.saving.git_utils import get_stashed_files

def display_session(session: Session|None) -> None:
    if session is None:
        rprint("[red]No session found[/red]")
        return

    git_section = ""
    if session.git_branch:
        git_section = f"[green]Git Branch:[/green] {session.git_branch}\n"
        if session.git_status:
            git_section += f"[bold magenta]Git Status:[/bold magenta]\n{session.git_status}\n"
        else:
            git_section += f"[italic]Working tree clean[/italic]\n"
    commands_str = "\n".join(f"  {i+1}. {c}" for i, c in enumerate(session.commands))

    content = (
        f"[bold]ID:[/bold]         {session.id}\n"
        f"[bold]Folder:[/bold]     {session.folder}\n"
        f"[bold]Saved at:[/bold]   {session.created_at}\n"
        f"[bold]Message:[/bold]    {session.message}\n"
        f"{git_section}"
        f"[bold]Commands:[/bold]\n"
        f"{commands_str}"
    )
    stashed_files = get_stashed_files(session.id)

    if stashed_files:
        print(f"📦 Snapshot available for {len(stashed_files)} files:")
        for file in stashed_files:
            print(f"  • {file}")

    rprint(Panel(content, title = "Last BRB Session", border_style = "blue"))
