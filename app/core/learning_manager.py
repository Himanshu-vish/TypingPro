from datetime import datetime

from app.core.database_manager import DatabaseManager
from app.core.session_manager import SessionManager


class LearningManager:

    def __init__(self):
        self.db = DatabaseManager()

    def profile_id(self):
        return SessionManager.profile_key()

    def save_progress(
        self,
        language,
        lesson_id,
        accuracy,
        wpm,
        stars,
        completed=True
    ):
        profile_id = self.profile_id()

        with self.db.connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT best_accuracy, best_wpm, stars, completed
                FROM learning_progress
                WHERE profile_id = ?
                  AND language = ?
                  AND lesson_id = ?
                """,
                (profile_id, language, lesson_id)
            )
            row = cursor.fetchone()

            best_accuracy = max(float(accuracy), float(row[0] if row else 0))
            best_wpm = max(float(wpm), float(row[1] if row else 0))
            best_stars = max(int(stars), int(row[2] if row else 0))
            was_completed = bool(row[3]) if row else False

            cursor.execute(
                """
                INSERT INTO learning_progress (
                    profile_id,
                    language,
                    lesson_id,
                    completed,
                    best_accuracy,
                    best_wpm,
                    stars,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(profile_id, language, lesson_id)
                DO UPDATE SET
                    completed = excluded.completed,
                    best_accuracy = excluded.best_accuracy,
                    best_wpm = excluded.best_wpm,
                    stars = excluded.stars,
                    updated_at = excluded.updated_at
                """,
                (
                    profile_id,
                    language,
                    lesson_id,
                    1 if (completed or was_completed) else 0,
                    best_accuracy,
                    best_wpm,
                    best_stars,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
            )
            conn.commit()

    def get_progress(self, language=None):
        query = """
            SELECT language, lesson_id, completed,
                   best_accuracy, best_wpm, stars
            FROM learning_progress
            WHERE profile_id = ?
        """
        params = [self.profile_id()]

        if language:
            query += " AND language = ?"
            params.append(language)

        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()

        return [
            {
                "language": row[0],
                "lesson_id": row[1],
                "completed": bool(row[2]),
                "best_accuracy": float(row[3] or 0),
                "best_wpm": float(row[4] or 0),
                "stars": int(row[5] or 0),
            }
            for row in rows
        ]

    def completed_count(self, language):
        return sum(
            1 for item in self.get_progress(language)
            if item["completed"]
        )


    def reset_language_progress(self, language):
        """Clear saved learning progress for current profile and language."""
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                DELETE FROM learning_progress
                WHERE profile_id = ?
                  AND language = ?
                """,
                (self.profile_id(), language)
            )
            conn.commit()
        return True


    def lesson_progress(self, language, lesson_id):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT completed, best_accuracy, best_wpm, stars
                FROM learning_progress
                WHERE profile_id = ?
                  AND language = ?
                  AND lesson_id = ?
                """,
                (
                    self.profile_id(),
                    language,
                    lesson_id
                )
            )
            row = cursor.fetchone()

        if not row:
            return {
                "completed": False,
                "best_accuracy": 0.0,
                "best_wpm": 0.0,
                "stars": 0,
            }

        return {
            "completed": bool(row[0]),
            "best_accuracy": float(row[1] or 0),
            "best_wpm": float(row[2] or 0),
            "stars": int(row[3] or 0),
        }

    def completed_lesson_ids(self, language):
        return {
            item["lesson_id"]
            for item in self.get_progress(language)
            if item["completed"]
        }

    def course_summary(self, language, total_lessons):
        progress = self.get_progress(language)

        completed = sum(
            1 for item in progress
            if item["completed"]
        )

        total_stars = sum(
            int(item["stars"])
            for item in progress
        )

        best_wpm = max(
            [float(item["best_wpm"]) for item in progress] or [0.0]
        )

        best_accuracy = max(
            [float(item["best_accuracy"]) for item in progress] or [0.0]
        )

        percent = int(
            (completed / total_lessons) * 100
        ) if total_lessons else 0

        return {
            "completed": completed,
            "total": total_lessons,
            "percent": percent,
            "stars": total_stars,
            "max_stars": total_lessons * 3,
            "best_wpm": best_wpm,
            "best_accuracy": best_accuracy,
        }
