import os
import shutil
import sqlite3
import sys
from pathlib import Path

APP_NAME = "TypingPro"


def resource_root() -> Path:
    """Read-only bundled application root (source tree or PyInstaller bundle)."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent.parent


def resource_path(*parts) -> Path:
    return resource_root().joinpath(*parts)


def user_data_dir() -> Path:
    """Writable per-user data. Survives app upgrades/uninstalls by default."""
    base = Path(os.environ.get("LOCALAPPDATA") or (Path.home() / "AppData" / "Local"))
    path = base / APP_NAME
    path.mkdir(parents=True, exist_ok=True)
    return path


def reports_path() -> Path:
    return user_data_dir() / "typing_reports.json"


def database_path() -> Path:
    return user_data_dir() / "typingpro.db"


def migrate_legacy_reports() -> None:
    """Copy legacy project-relative reports once; never overwrite newer user data."""
    target = reports_path()
    if target.exists():
        return
    candidates = [
        Path.cwd() / "data" / "typing_reports.json",
        resource_path("data", "typing_reports.json"),
    ]
    for source in candidates:
        try:
            if source.exists() and source.resolve() != target.resolve():
                shutil.copy2(source, target)
                return
        except OSError:
            pass


def migrate_legacy_database() -> None:
    """
    One-time migration of the old project/bundled TypingPro database.

    The installed app always uses %LOCALAPPDATA%\\TypingPro\\typingpro.db.
    If that database has no registered users yet, copy the legacy database
    so accounts created before packaging continue to work. Existing user
    data is never overwritten.
    """
    target = database_path()

    # Never replace a database that already contains a user account.
    if target.exists():
        try:
            with sqlite3.connect(target) as conn:
                row = conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
                ).fetchone()
                if row:
                    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
                    if int(count or 0) > 0:
                        return
        except sqlite3.Error:
            # If the target is not readable, do not destroy it automatically.
            return

    candidates = [
        Path.cwd() / "data" / "typingpro.db",
        resource_path("data", "typingpro.db"),
    ]

    for source in candidates:
        try:
            if not source.exists():
                continue
            if target.exists() and source.resolve() == target.resolve():
                continue

            # Only migrate a real legacy DB containing at least one user.
            with sqlite3.connect(source) as conn:
                row = conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
                ).fetchone()
                if not row:
                    continue
                count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
                if int(count or 0) <= 0:
                    continue

            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            return
        except (OSError, sqlite3.Error):
            continue
