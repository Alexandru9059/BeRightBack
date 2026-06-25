import pytest
from brb.database.database import Database
from brb.saving.models import Session

# --- FIXTURES ---

@pytest.fixture
def memory_db():
    """Creates a fresh, in-memory database for each test."""
    # Override the path to use SQLite's special in-memory mode
    db = Database(db_path=":memory:")
    db.init_db()
    return db

# --- TESTS ---

def test_insert_and_fetch_session(memory_db):
    """Test saving a basic session and fetching it back."""
    s_id = memory_db.insert_session(
        folder="/fake/path", 
        message="Testing DB", 
        git_branch="main", 
        git_status="M file.py"
    )
    
    session = memory_db.fetch_session_by_id(s_id)
    
    assert session is not None
    assert session.folder == "/fake/path"
    assert session.message == "Testing DB"
    assert session.git_branch == "main"
    assert session.git_status == "M file.py"

def test_insert_saving_with_commands(memory_db):
    """Test the full save method including commands."""
    memory_db.insert_saving(
        path="/test",
        message="Full save",
        lastcommands=["ls", "git status", "pytest"],
        git_branch=None,
        git_status=None
    )
    
    session = memory_db.fetch_last_session()
    
    assert session is not None
    assert session.commands == ["ls", "git status", "pytest"]
    assert len(session.commands) == 3

def test_fetch_all_sessions(memory_db):
    """Test retrieving multiple sessions."""
    memory_db.insert_session("/path1", "First")
    memory_db.insert_session("/path2", "Second")
    
    sessions = memory_db.fetch_all_sessions()
    
    assert sessions is not None
    assert len(sessions) == 2
    # The list should be ordered DESC (newest first)
    assert sessions[0].message == "Second"
    assert sessions[1].message == "First"


def test_display_session_no_commands(capsys):
    from brb.ui.display import display_session
    session = Session(
        id=1,
        folder="/fake/path",
        message="No commands test",
        created_at="2026-06-19 12:00:00",
        commands=[],
        git_branch="main",
        git_status="M file.py"
    )
    display_session(session)
    captured = capsys.readouterr()
    assert "No commands test" in captured.out
    assert "main" in captured.out


def test_display_session_with_commands(capsys):
    from brb.ui.display import display_session
    session = Session(
        id=2,
        folder="/fake/path",
        message="With commands test",
        created_at="2026-06-19 12:00:00",
        commands=["git status", "pytest"],
        git_branch=None,
        git_status=None
    )
    display_session(session)
    captured = capsys.readouterr()
    assert "With commands test" in captured.out
    assert "git status" in captured.out
    assert "pytest" in captured.out


def test_display_session_none(capsys):
    from brb.ui.display import display_session
    display_session(None)
    captured = capsys.readouterr()
    assert "No session found" in captured.out


def test_fetch_last_session_by_folder(memory_db):
    """Test retrieving the last session matching a specific folder."""
    memory_db.insert_session("/path1", "First in path1")
    memory_db.insert_session("/path2", "First in path2")
    memory_db.insert_session("/path1", "Second in path1")
    
    session = memory_db.fetch_last_session_by_folder("/path1")
    assert session is not None
    assert session.folder == "/path1"
    assert session.message == "Second in path1"
    
    session_other = memory_db.fetch_last_session_by_folder("/path_unknown")
    assert session_other is None
