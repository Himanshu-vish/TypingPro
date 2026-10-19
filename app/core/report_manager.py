import os
import json
from datetime import datetime

from app.core.session_manager import SessionManager
from app.core.app_paths import reports_path, migrate_legacy_reports


_legacy_migration_done = False


class ReportManager:

    def __init__(self):
        global _legacy_migration_done

        # Disk migration is required for compatibility, but not once for
        # every ReportManager created by preloaded pages.
        if not _legacy_migration_done:
            migrate_legacy_reports()
            _legacy_migration_done = True

        self.file_path = str(reports_path())

    def _load_all_reports(self):
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    def _write_all_reports(self, reports):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(reports, file, ensure_ascii=False, indent=4)

    def _belongs_to_current_profile(self, report):
        current = SessionManager.profile_key()
        saved = report.get("profile_id")

        # Backward compatibility:
        # every old report created before accounts existed belongs to Guest.
        if saved is None:
            return current == "guest"

        return saved == current

    def save_result(
        self,
        language,
        mode,
        exam,
        duration,
        net_wpm,
        gross_wpm,
        accuracy,
        mistakes,
        correct_chars,
        wrong_chars,
        backspace,
        custom_target_wpm=None,
        custom_target_accuracy=None,
        custom_result=None
    ):
        reports = self._load_all_reports()

        report = {
            "profile_id": SessionManager.profile_key(),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "language": language,
            "mode": mode,
            "exam": exam,
            "duration": duration,
            "net_wpm": round(net_wpm, 2),
            "gross_wpm": round(gross_wpm, 2),
            "accuracy": round(accuracy, 2),
            "mistakes": mistakes,
            "correct_chars": correct_chars,
            "wrong_chars": wrong_chars,
            "backspace": backspace,
            "custom_target_wpm": custom_target_wpm,
            "custom_target_accuracy": custom_target_accuracy,
            "custom_result": custom_result
        }

        reports.append(report)
        self._write_all_reports(reports)

    def load_dashboard_reports(self):
        """
        Guest dashboard:
            Guest + all registered users on this device.

        Logged-in dashboard:
            Only the current user's own reports.

        Reports page still calls load_reports(), therefore reports
        remain separated by profile.
        """

        all_reports = self._load_all_reports()

        if SessionManager.is_guest():

            return [
                dict(report)
                for report in all_reports
            ]

        return [
            dict(report)
            for report in all_reports
            if self._belongs_to_current_profile(report)
        ]


    def load_reports(self):
        return [
            dict(report)
            for report in self._load_all_reports()
            if self._belongs_to_current_profile(report)
        ]

    def delete_report(self, index):
        all_reports = self._load_all_reports()

        matching_indexes = [
            i for i, report in enumerate(all_reports)
            if self._belongs_to_current_profile(report)
        ]

        if 0 <= index < len(matching_indexes):
            all_reports.pop(matching_indexes[index])
            self._write_all_reports(all_reports)
            return True

        return False

    def clear_reports(self):
        remaining = [
            report
            for report in self._load_all_reports()
            if not self._belongs_to_current_profile(report)
        ]
        self._write_all_reports(remaining)
        return True
