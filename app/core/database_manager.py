import sqlite3

from app.core.app_paths import database_path


class DatabaseManager:

    # Several TypingPro managers create DatabaseManager instances while
    # the preloaded pages are being built. Schema creation/migration only
    # needs to run once for the same database during one app process.
    _schema_ready = False
    _schema_path = None

    def __init__(self):

        self.db_path = database_path()
        current_path = str(self.db_path)

        if (
            not DatabaseManager._schema_ready
            or DatabaseManager._schema_path != current_path
        ):
            self.create_tables()
            DatabaseManager._schema_ready = True
            DatabaseManager._schema_path = current_path

    def connect(self):

        return sqlite3.connect(
            self.db_path
        )

    def create_tables(self):

        with self.connect() as conn:

            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    username TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    recovery_pin_hash TEXT,
                    created_at TEXT NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL UNIQUE,
                    default_language TEXT DEFAULT 'English',
                    default_duration INTEGER DEFAULT 5,
                    default_test_mode TEXT DEFAULT 'Practice Mode',
                    default_highlight_mode TEXT DEFAULT 'Character',
                    show_correct INTEGER DEFAULT 1,
                    show_wrong INTEGER DEFAULT 1,
                    show_current INTEGER DEFAULT 1,
                    remember_last_selection INTEGER DEFAULT 1,
                    auto_focus_typing_box INTEGER DEFAULT 1,
                    confirm_clear_history INTEGER DEFAULT 1,
                    confirm_delete_report INTEGER DEFAULT 1,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS learning_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_id TEXT NOT NULL,
                    language TEXT NOT NULL,
                    lesson_id TEXT NOT NULL,
                    completed INTEGER DEFAULT 0,
                    best_accuracy REAL DEFAULT 0,
                    best_wpm REAL DEFAULT 0,
                    stars INTEGER DEFAULT 0,
                    updated_at TEXT,
                    UNIQUE(profile_id, language, lesson_id)
                )
            """)

            # Migration for existing TypingPro installations:
            # older databases do not have recovery_pin_hash.
            cursor.execute(
                "PRAGMA table_info(users)"
            )
            user_columns = {
                row[1]
                for row in cursor.fetchall()
            }

            if "recovery_pin_hash" not in user_columns:
                cursor.execute(
                    "ALTER TABLE users ADD COLUMN recovery_pin_hash TEXT"
                )

            conn.commit()

    def total_users(self):
        """
        Return total number of registered offline users.
        Used by DashboardPage.
        """

        with self.connect() as conn:

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM users
                """
            )

            row = cursor.fetchone()

        return (
            int(row[0])
            if row
            else 0
        )

