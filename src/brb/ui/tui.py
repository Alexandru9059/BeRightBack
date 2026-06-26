from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, ListView, ListItem, Label, Markdown
from textual.containers import Horizontal

from brb.cli import get_db

class BRBTuiApp(App):
    CSS = """
    #sidebar {
        width: 30%;
        border-right: solid green;
    }
    #details {
        width: 70%;
        padding: 1 2;
    }
    """
    BINDINGS = [
        ("q", "quit", "Quit the app"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Horizontal():
            yield ListView(id="sidebar")
            yield Markdown("Select a session on the left to see details here...", id="details")

        yield Footer()

    def on_mount(self) -> None:
        sidebar = self.query_one("#sidebar", ListView)
        sessions = get_db().fetch_all_sessions()

        if sessions:
            for session in sessions:
                timestr = session.created_at.split()[1]
                short_msg = session.message[:20] + "..." if len(session.message) > 20 else session.message
                item = ListItem(Label(f"[{session.id}] {timestr} - {short_msg}"))
                item.session_data = session
                sidebar.append(item)

    @on(ListView.Highlighted)
    def update_details_panel(self, event: ListView.Highlighted) -> None:
        session = event.item.session_data

        details_text = f"""
    # Session {session.id}
    **Time:** {session.created_at}
    **Branch:** {session.git_branch}
    **Status:** {session.git_status or 'Clean'}
  
    ## Summary
    {session.message}
  
    ## Last Commands
    ```bash
    {chr(10).join(session.commands)}
        """

        details_panel = self.query_one("#details", Markdown)
        details_panel.update(details_text)