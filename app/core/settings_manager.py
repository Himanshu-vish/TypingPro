from PySide6.QtCore import QSettings

from app.core.session_manager import SessionManager


class SettingsManager:

    ORGANIZATION = "TypingPro"
    APPLICATION = "TypingPro"

    DEFAULTS = {
        "default_language": "English",
        "default_duration": 5,
        "default_test_mode": "Practice Mode",
        "default_highlight_mode": "Character",
        "show_correct": True,
        "show_wrong": True,
        "show_current": True,
        "remember_last_selection": True,
        "auto_focus_typing_box": True,
        "confirm_clear_history": True,
        "confirm_delete_report": True,
    }

    def __init__(self):
        self.settings = QSettings(
            self.ORGANIZATION,
            self.APPLICATION
        )

    def _profile_key(self, key):
        return f"profiles/{SessionManager.profile_key()}/{key}"

    def get(self, key):
        default = self.DEFAULTS.get(key)

        if isinstance(default, bool):
            return self.settings.value(
                self._profile_key(key),
                default,
                type=bool
            )

        if isinstance(default, int):
            return self.settings.value(
                self._profile_key(key),
                default,
                type=int
            )

        return self.settings.value(
            self._profile_key(key),
            default
        )

    def set(self, key, value):
        self.settings.setValue(
            self._profile_key(key),
            value
        )

    def save_all(self, values):
        for key, value in values.items():
            self.set(key, value)

        self.settings.sync()

    def reset_defaults(self):
        for key, value in self.DEFAULTS.items():
            self.settings.setValue(
                self._profile_key(key),
                value
            )

        self.settings.sync()

    def all(self):
        return {
            key: self.get(key)
            for key in self.DEFAULTS
        }
