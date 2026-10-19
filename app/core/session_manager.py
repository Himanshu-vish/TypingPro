from PySide6.QtCore import QObject, Signal


class _SessionSignals(QObject):
    profile_changed = Signal()


class SessionManager:
    """
    TypingPro always starts as Guest.
    A signed-in user only changes the active local profile.
    """
    _current_user = None
    signals = _SessionSignals()

    @classmethod
    def login(cls, user):
        cls._current_user = dict(user)
        cls.signals.profile_changed.emit()

    @classmethod
    def logout(cls):
        cls._current_user = None
        cls.signals.profile_changed.emit()

    @classmethod
    def is_guest(cls):
        return cls._current_user is None

    @classmethod
    def current_user(cls):
        return cls._current_user

    @classmethod
    def user_id(cls):
        if cls._current_user:
            return cls._current_user.get("id")
        return None

    @classmethod
    def display_name(cls):
        if cls._current_user:
            return cls._current_user.get("name") or cls._current_user.get("username") or "User"
        return "Guest"

    @classmethod
    def profile_key(cls):
        if cls._current_user:
            return f"user_{cls._current_user.get('id')}"
        return "guest"
