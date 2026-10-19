import hashlib
import secrets
from datetime import datetime

from app.core.database_manager import DatabaseManager


class AuthManager:

    def __init__(self):

        self.db = DatabaseManager()

    def _hash_password(
        self,
        password,
        salt=None
    ):

        if salt is None:

            salt = secrets.token_hex(
                16
            )

        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            120000
        )

        return (
            f"{salt}:"
            f"{digest.hex()}"
        )

    def _verify_password(
        self,
        password,
        stored_hash
    ):

        try:

            salt, saved_digest = (
                stored_hash.split(
                    ":",
                    1
                )
            )

        except ValueError:

            return False

        new_hash = (
            self._hash_password(
                password,
                salt
            )
        )

        return (
            new_hash
            ==
            stored_hash
        )

    def signup(
        self,
        name,
        username,
        password,
        recovery_pin=None
    ):

        name = name.strip()
        username = username.strip()
        recovery_pin = (
            recovery_pin.strip()
            if recovery_pin is not None
            else ""
        )

        if not name:
            return (
                False,
                "Name is required."
            )

        if not username:
            return (
                False,
                "Username is required."
            )

        if len(password) < 4:
            return (
                False,
                "Password must be at least 4 characters."
            )

        if recovery_pin:
            if (
                not recovery_pin.isdigit()
                or not 4 <= len(recovery_pin) <= 6
            ):
                return (
                    False,
                    "Recovery PIN must be 4 to 6 digits."
                )

        password_hash = self._hash_password(
            password
        )

        recovery_pin_hash = (
            self._hash_password(
                recovery_pin
            )
            if recovery_pin
            else None
        )

        try:

            with self.db.connect() as conn:

                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO users (
                        name,
                        username,
                        password_hash,
                        recovery_pin_hash,
                        created_at
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        name,
                        username,
                        password_hash,
                        recovery_pin_hash,
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                    )
                )

                user_id = cursor.lastrowid

                cursor.execute(
                    """
                    INSERT INTO user_settings (
                        user_id
                    )
                    VALUES (?)
                    """,
                    (
                        user_id,
                    )
                )

                conn.commit()

            return (
                True,
                "Account created successfully."
            )

        except Exception as error:

            if (
                "UNIQUE constraint failed"
                in str(error)
            ):
                return (
                    False,
                    "Username already exists."
                )

            return (
                False,
                str(error)
            )


    def has_recovery_pin(
        self,
        username
    ):

        username = username.strip()

        if not username:
            return False

        with self.db.connect() as conn:

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT recovery_pin_hash
                FROM users
                WHERE username = ?
                """,
                (
                    username,
                )
            )

            row = cursor.fetchone()

        return bool(
            row
            and row[0]
        )


    def reset_password(
        self,
        username,
        recovery_pin,
        new_password
    ):

        username = username.strip()
        recovery_pin = recovery_pin.strip()

        if not username:
            return (
                False,
                "Username is required."
            )

        if (
            not recovery_pin.isdigit()
            or not 4 <= len(recovery_pin) <= 6
        ):
            return (
                False,
                "Enter your 4 to 6 digit Recovery PIN."
            )

        if len(new_password) < 4:
            return (
                False,
                "New password must be at least 4 characters."
            )

        with self.db.connect() as conn:

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT recovery_pin_hash
                FROM users
                WHERE username = ?
                """,
                (
                    username,
                )
            )

            row = cursor.fetchone()

            if row is None:
                return (
                    False,
                    "Username not found."
                )

            stored_pin_hash = row[0]

            if not stored_pin_hash:
                return (
                    False,
                    "This older account has no Recovery PIN. "
                    "Create/set a Recovery PIN first."
                )

            if not self._verify_password(
                recovery_pin,
                stored_pin_hash
            ):
                return (
                    False,
                    "Incorrect Recovery PIN."
                )

            new_password_hash = self._hash_password(
                new_password
            )

            cursor.execute(
                """
                UPDATE users
                SET password_hash = ?
                WHERE username = ?
                """,
                (
                    new_password_hash,
                    username
                )
            )

            conn.commit()

        return (
            True,
            "Password reset successfully."
        )


    def login(
        self,
        username,
        password
    ):

        username = username.strip()

        with self.db.connect() as conn:

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    name,
                    username,
                    password_hash
                FROM users
                WHERE username = ?
                """,
                (
                    username,
                )
            )

            row = cursor.fetchone()

        if row is None:

            return (
                False,
                None,
                "Invalid username or password."
            )

        user_id, name, username, stored_hash = row

        if not self._verify_password(
            password,
            stored_hash
        ):

            return (
                False,
                None,
                "Invalid username or password."
            )

        user = {
            "id": user_id,
            "name": name,
            "username": username
        }

        return (
            True,
            user,
            "Login successful."
        )
