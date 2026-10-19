from datetime import datetime

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QFrame,
    QPushButton,
    QProgressBar,
    QSizePolicy,
    QStyle
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont

from app.core.report_manager import ReportManager
from app.core.database_manager import DatabaseManager
from app.core.learning_manager import LearningManager


# =========================================================
# REUSABLE DASHBOARD UI COMPONENTS
# =========================================================

class SummaryCard(QFrame):

    def __init__(
        self,
        icon_text,
        title,
        value="0",
        subtitle="",
        accent="#2563EB",
        tint="#EAF2FF"
    ):
        super().__init__()

        self.setObjectName("summaryCard")
        self.setMinimumHeight(122)
        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 15, 18, 15)
        layout.setSpacing(13)

        icon = QLabel(icon_text)
        icon.setAlignment(Qt.AlignCenter)
        icon.setFixedSize(52, 52)
        icon.setStyleSheet(
            f"""
            QLabel {{
                background: {tint};
                color: {accent};
                border: 1px solid {accent}22;
                border-radius: 26px;
                font-size: 23px;
                font-weight: 700;
            }}
            """
        )

        text_box = QVBoxLayout()
        text_box.setSpacing(1)

        title_lbl = QLabel(title)
        title_lbl.setObjectName("summaryTitle")

        self.value_lbl = QLabel(str(value))
        self.value_lbl.setObjectName("summaryValue")

        subtitle_lbl = QLabel(subtitle)
        subtitle_lbl.setObjectName("summarySub")

        text_box.addWidget(title_lbl)
        text_box.addWidget(self.value_lbl)

        if subtitle:
            text_box.addWidget(subtitle_lbl)

        text_box.addStretch()

        layout.addWidget(icon)
        layout.addLayout(text_box, 1)

    def set_value(self, value):
        self.value_lbl.setText(str(value))


class LearningCard(QFrame):

    def __init__(
        self,
        title,
        value="0%",
        accent="#2563EB",
        tint="#EAF2FF"
    ):
        super().__init__()

        self.accent = accent
        self.tint = tint

        self.setObjectName("learningCard")
        self.setMinimumHeight(126)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 14, 20, 14)
        layout.setSpacing(16)

        ring = QFrame()
        ring.setFixedSize(70, 70)
        ring.setStyleSheet(
            f"""
            QFrame {{
                background: {tint};
                border: 7px solid #E8EDF3;
                border-radius: 35px;
            }}
            """
        )

        ring_layout = QVBoxLayout(ring)
        ring_layout.setContentsMargins(0, 0, 0, 0)

        self.percent_ring_lbl = QLabel(value)
        self.percent_ring_lbl.setAlignment(Qt.AlignCenter)
        self.percent_ring_lbl.setStyleSheet(
            f"""
            QLabel {{
                color: {accent};
                font-size: 20px;
                font-weight: 800;
                background: transparent;
            }}
            """
        )
        ring_layout.addWidget(self.percent_ring_lbl)

        content = QVBoxLayout()
        content.setSpacing(5)

        title_lbl = QLabel(title)
        title_lbl.setObjectName("learningTitle")

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(10)
        self.progress.setStyleSheet(
            f"""
            QProgressBar {{
                background: #E3E8EF;
                border: none;
                border-radius: 5px;
            }}
            QProgressBar::chunk {{
                background: {accent};
                border-radius: 5px;
            }}
            """
        )

        self.percent_lbl = QLabel(value)
        self.percent_lbl.setObjectName("learningPercent")

        content.addWidget(title_lbl)
        content.addWidget(self.progress)
        content.addWidget(self.percent_lbl)

        layout.addWidget(ring)
        layout.addLayout(content, 1)

    def set_value(self, value):
        text = str(value)
        self.percent_ring_lbl.setText(text)
        self.percent_lbl.setText(text)

        try:
            percent = int(
                float(
                    text.replace("%", "")
                )
            )
        except (ValueError, TypeError):
            percent = 0

        self.progress.setValue(
            max(0, min(percent, 100))
        )


class PracticeCard(QFrame):

    def __init__(
        self,
        icon_text,
        title,
        description,
        button_text,
        accent,
        tint
    ):
        super().__init__()

        self.setObjectName("practiceCard")
        self.setMinimumHeight(132)
        self.setMaximumHeight(142)
        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )

        outer = QHBoxLayout(self)
        outer.setContentsMargins(16, 14, 16, 14)
        outer.setSpacing(13)

        icon = QLabel(icon_text)
        icon.setAlignment(Qt.AlignCenter)
        icon.setFixedSize(54, 54)
        icon.setStyleSheet(
            f"""
            QLabel {{
                background: {tint};
                color: {accent};
                border: 1px solid {accent}22;
                border-radius: 27px;
                font-size: 23px;
                font-weight: 700;
            }}
            """
        )

        copy = QVBoxLayout()
        copy.setSpacing(4)

        title_lbl = QLabel(title)
        title_lbl.setObjectName("practiceTitle")

        desc_lbl = QLabel(description)
        desc_lbl.setObjectName("practiceText")
        desc_lbl.setWordWrap(True)

        copy.addWidget(title_lbl)
        copy.addWidget(desc_lbl)
        copy.addStretch()

        self.button = QPushButton(
            f"{button_text}   →"
        )
        self.button.setCursor(
            Qt.PointingHandCursor
        )
        self.button.setFixedHeight(44)
        self.button.setMinimumWidth(126)
        self.button.setMaximumWidth(150)
        self.button.setStyleSheet(
            f"""
            QPushButton {{
                background: {accent};
                color: #FFFFFF;
                border: 1px solid {accent};
                border-radius: 7px;
                padding: 6px 12px;
                font-size: 13px;
                font-weight: 700;
            }}
            QPushButton:hover {{
                background: {accent};
                border-color: {accent};
            }}
            QPushButton:pressed {{
                padding-top: 7px;
            }}
            """
        )

        outer.addWidget(
            icon,
            0,
            Qt.AlignVCenter
        )
        outer.addLayout(copy, 1)
        outer.addWidget(
            self.button,
            0,
            Qt.AlignVCenter
        )


class RecentActivityPanel(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName("recentPanel")
        self.setMinimumHeight(254)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(16, 8, 16, 8)
        self.layout.setSpacing(0)

        self.empty_lbl = QLabel(
            "No Practice History Found"
        )
        self.empty_lbl.setObjectName("emptyText")
        self.empty_lbl.setAlignment(
            Qt.AlignCenter
        )

        self.layout.addWidget(self.empty_lbl)

    def _clear(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def set_reports(self, reports):
        self._clear()

        if not reports:
            empty = QLabel(
                "No Practice History Found"
            )
            empty.setObjectName("emptyText")
            empty.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(empty)
            return

        for index, report in enumerate(reports):
            row = QFrame()
            row.setObjectName("recentRow")
            row.setMinimumHeight(44)

            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(
                5, 4, 5, 4
            )
            row_layout.setSpacing(8)

            clock = QLabel("◷")
            clock.setObjectName("recentClock")
            clock.setAlignment(Qt.AlignCenter)
            clock.setFixedWidth(26)

            date_lbl = QLabel(
                str(report.get("date", "-"))
            )
            date_lbl.setObjectName("recentDate")
            date_lbl.setMinimumWidth(185)

            language_lbl = QLabel(
                str(report.get("language", "-"))
            )
            language_lbl.setObjectName("recentCell")
            language_lbl.setMinimumWidth(95)

            mode_lbl = QLabel(
                str(report.get("mode", "-"))
            )
            mode_lbl.setObjectName("recentCell")
            mode_lbl.setMinimumWidth(135)

            wpm_lbl = QLabel(
                f"WPM: {report.get('net_wpm', 0)}"
            )
            wpm_lbl.setObjectName("recentCell")
            wpm_lbl.setMinimumWidth(110)

            accuracy_lbl = QLabel(
                f"Accuracy: {report.get('accuracy', 0)}%"
            )
            accuracy_lbl.setObjectName("recentCell")
            accuracy_lbl.setMinimumWidth(150)

            arrow = QLabel("›")
            arrow.setObjectName("recentArrow")
            arrow.setAlignment(Qt.AlignCenter)
            arrow.setFixedWidth(24)

            row_layout.addWidget(clock)
            row_layout.addWidget(date_lbl)
            row_layout.addWidget(
                self._separator()
            )
            row_layout.addWidget(language_lbl)
            row_layout.addWidget(
                self._separator()
            )
            row_layout.addWidget(mode_lbl)
            row_layout.addWidget(
                self._separator()
            )
            row_layout.addWidget(wpm_lbl)
            row_layout.addWidget(
                self._separator()
            )
            row_layout.addWidget(accuracy_lbl)
            row_layout.addStretch()
            row_layout.addWidget(arrow)

            self.layout.addWidget(row)

            if index < len(reports) - 1:
                line = QFrame()
                line.setFixedHeight(1)
                line.setStyleSheet(
                    "background:#E7ECF2;"
                )
                self.layout.addWidget(line)

        self.layout.addStretch()

    def _separator(self):
        line = QFrame()
        line.setFixedWidth(1)
        line.setFixedHeight(18)
        line.setStyleSheet(
            "background:#D7DFE8;"
        )
        return line


class DashboardPage(QWidget):

    def __init__(self):
        super().__init__()

        self.report_manager = ReportManager()
        self.database_manager = DatabaseManager()
        self.learning_manager = LearningManager()

        self.build_ui()
        self.load_dashboard_data()

    # =====================================================
    # UI
    # =====================================================

    def build_ui(self):

        self.setObjectName("dashboardPage")

        self.setStyleSheet("""
            QWidget#dashboardPage {
                background: #F6F8FC;
                font-family: "Segoe UI";
            }

            QFrame#summaryCard,
            QFrame#learningCard,
            QFrame#practiceCard,
            QFrame#recentPanel {
                background: #FFFFFF;
                border: 1px solid #DCE4ED;
                border-radius: 12px;
            }

            QLabel#summaryTitle {
                color: #243B53;
                font-size: 14px;
                font-weight: 750;
            }

            QLabel#summaryValue {
                color: #101E31;
                font-size: 24px;
                font-weight: 800;
            }

            QLabel#summarySub {
                color: #455B72;
                font-size: 12px;
                font-weight: 650;
            }

            QLabel#learningTitle {
                color: #243B53;
                font-size: 16px;
                font-weight: 750;
            }

            QLabel#learningPercent {
                color: #40566D;
                font-size: 13px;
                font-weight: 700;
            }

            QLabel#sectionAccent {
                background: #287FE8;
                border-radius: 2px;
            }

            QLabel#sectionTitle {
                color: #17304E;
                font-size: 20px;
                font-weight: 750;
            }

            QLabel#practiceTitle {
                color: #20364D;
                font-size: 16px;
                font-weight: 750;
            }

            QLabel#practiceText {
                color: #455B72;
                font-size: 13px;
                font-weight: 650;
            }

            QLabel#emptyText {
                color: #455B72;
                font-size: 15px;
                font-weight: 650;
            }

            QFrame#recentRow {
                background: transparent;
                border: none;
            }

            QLabel#recentClock {
                color: #557391;
                font-size: 20px;
                font-weight: 700;
            }

            QLabel#recentDate {
                color: #263B54;
                font-size: 14px;
                font-weight: 600;
            }

            QLabel#recentCell {
                color: #324860;
                font-size: 14px;
                font-weight: 550;
            }

            QLabel#recentArrow {
                color: #3A5D81;
                font-size: 24px;
                font-weight: 500;
            }

            QLabel#footerText {
                color: #758396;
                font-size: 12px;
                font-weight: 500;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            28, 20, 28, 16
        )
        layout.setSpacing(14)

        # =================================================
        # SUMMARY STATS — LARGE CARDS
        # =================================================

        stats_grid = QGridLayout()
        stats_grid.setHorizontalSpacing(12)
        stats_grid.setVerticalSpacing(12)

        self.total_tests_card = SummaryCard(
            "⌨",
            "Total Practice",
            "0",
            "Tests Attempted",
            "#2563EB",
            "#EAF2FF"
        )

        self.today_card = SummaryCard(
            "▣",
            "Today's Practice",
            "0",
            "Tests Attempted",
            "#17A765",
            "#E8F8EF"
        )

        self.best_wpm_card = SummaryCard(
            "↗",
            "Best WPM",
            "0",
            "WPM",
            "#7C3AED",
            "#F2EAFE"
        )

        self.accuracy_card = SummaryCard(
            "◎",
            "Accuracy",
            "0%",
            "Overall Accuracy",
            "#F07D20",
            "#FFF0E3"
        )

        self.registered_users_card = SummaryCard(
            "●●",
            "Registered Users",
            "0",
            "Total Users",
            "#E74C5C",
            "#FDEBED"
        )

        for col, card in enumerate([
            self.total_tests_card,
            self.today_card,
            self.best_wpm_card,
            self.accuracy_card,
            self.registered_users_card
        ]):
            stats_grid.addWidget(
                card, 0, col
            )

        layout.addLayout(stats_grid)

        # =================================================
        # LEARNING PROGRESS
        # =================================================

        learning_grid = QGridLayout()
        learning_grid.setHorizontalSpacing(12)

        self.english_learning_card = LearningCard(
            "English Learning",
            "0%",
            "#2563EB",
            "#EDF4FF"
        )

        self.hindi_learning_card = LearningCard(
            "Hindi Learning",
            "0%",
            "#17A765",
            "#EAF8F0"
        )

        learning_grid.addWidget(
            self.english_learning_card,
            0, 0
        )
        learning_grid.addWidget(
            self.hindi_learning_card,
            0, 1
        )

        layout.addLayout(learning_grid)

        # =================================================
        # START YOUR PRACTICE
        # =================================================

        section = self._section_header(
            "Start Your Practice"
        )
        layout.addLayout(section)

        practice_grid = QGridLayout()
        practice_grid.setHorizontalSpacing(12)
        practice_grid.setVerticalSpacing(14)

        english_card = PracticeCard(
            "⌨",
            "English Typing",
            "Practice English typing\nwith difficulty levels.",
            "Start Practice",
            "#2563EB",
            "#EAF2FF"
        )

        hindi_card = PracticeCard(
            "⌨",
            "Hindi Typing",
            "Practice Hindi typing\nwith Mangal Inscript.",
            "Start Practice",
            "#16A75F",
            "#E8F8EF"
        )

        upp_card = PracticeCard(
            "★",
            "UPP Practice",
            "UPP Computer Operator\nexam-focused typing.",
            "Start Practice",
            "#7C3AED",
            "#F2EAFE"
        )

        ssc_card = PracticeCard(
            "◎",
            "SSC Typing",
            "SSC typing practice\nwith exam targets.",
            "Start Practice",
            "#8A49E8",
            "#F1EAFE"
        )

        ccc_card = PracticeCard(
            "▥",
            "CCC Practice",
            "Practice CCC typing\nand speed building.",
            "Start Practice",
            "#E27B20",
            "#FFF0E3"
        )

        learn_card = PracticeCard(
            "◆",
            "Learn Typing",
            "Learn typing step by step\nwith guided lessons.",
            "Start Learning",
            "#F08A1A",
            "#FFF1E2"
        )

        practice_grid.addWidget(
            english_card, 0, 0
        )
        practice_grid.addWidget(
            hindi_card, 0, 1
        )
        practice_grid.addWidget(
            upp_card, 0, 2
        )

        practice_grid.addWidget(
            ssc_card, 1, 0
        )
        practice_grid.addWidget(
            ccc_card, 1, 1
        )
        practice_grid.addWidget(
            learn_card, 1, 2
        )

        # Public button attributes expected by dashboard.py.
        self.english_btn = english_card.button
        self.hindi_btn = hindi_card.button
        self.upp_btn = upp_card.button
        self.ssc_btn = ssc_card.button
        self.ccc_btn = ccc_card.button
        self.learn_btn = learn_card.button

        layout.addLayout(practice_grid)
        layout.addSpacing(8)

        # =================================================
        # RECENT ACTIVITY
        # =================================================

        layout.addLayout(
            self._section_header(
                "Recent Activity"
            )
        )

        self.recent = RecentActivityPanel()
        layout.addWidget(self.recent)

        # =================================================
        # FOOTER
        # =================================================

        footer = QHBoxLayout()
        footer.setSpacing(14)

        left = QLabel(
            "☁  100% Offline    ⚡  Fast & Lightweight    "
            "🔒  Secure & Private    ⟳  Regular Updates"
        )
        left.setObjectName("footerText")

        center = QLabel(
            "© 2026 Himanshu Vishwakarma  •  TypingPro  •  All rights reserved."
        )
        center.setObjectName("footerText")
        center.setAlignment(Qt.AlignCenter)

        right = QLabel(
            "Made with ♥ for better typing"
        )
        right.setObjectName("footerText")
        right.setAlignment(Qt.AlignRight)

        footer.addWidget(left, 1)
        footer.addWidget(center, 1)
        footer.addWidget(right, 1)

        layout.addLayout(footer)

    def _section_header(self, title):
        row = QHBoxLayout()
        row.setSpacing(8)

        accent = QLabel()
        accent.setObjectName("sectionAccent")
        accent.setFixedSize(4, 22)

        heading = QLabel(title)
        heading.setObjectName("sectionTitle")

        row.addWidget(accent)
        row.addWidget(heading)
        row.addStretch()

        return row

    # =====================================================
    # DATA
    # =====================================================

    def load_learning_data(self):

        english = (
            self.learning_manager
            .course_summary(
                "English",
                25
            )
        )

        hindi = (
            self.learning_manager
            .course_summary(
                "Hindi",
                20
            )
        )

        self.english_learning_card.set_value(
            f"{english['percent']}%"
        )

        self.hindi_learning_card.set_value(
            f"{hindi['percent']}%"
        )

    def load_dashboard_data(self):

        self.load_learning_data()

        reports = (
            self.report_manager
            .load_dashboard_reports()
        )

        total_tests = len(reports)

        # Registered users always refresh.
        self.registered_users_card.set_value(
            self.database_manager.total_users()
        )

        if total_tests == 0:

            self.today_card.set_value(0)
            self.best_wpm_card.set_value(0)
            self.accuracy_card.set_value("0%")
            self.total_tests_card.set_value(0)
            self.recent.set_reports([])

            return

        # Today's tests
        today = datetime.now().date()
        today_tests = 0

        for report in reports:
            try:
                report_date = datetime.strptime(
                    report.get("date", ""),
                    "%Y-%m-%d %H:%M:%S"
                ).date()

                if report_date == today:
                    today_tests += 1

            except (
                ValueError,
                TypeError
            ):
                pass

        # Best WPM
        wpm_values = []

        for report in reports:
            try:
                wpm_values.append(
                    float(
                        report.get(
                            "net_wpm",
                            0
                        )
                    )
                )
            except (
                ValueError,
                TypeError
            ):
                pass

        best_wpm = (
            max(wpm_values)
            if wpm_values
            else 0
        )

        # Average accuracy
        accuracy_values = []

        for report in reports:
            try:
                accuracy_values.append(
                    float(
                        report.get(
                            "accuracy",
                            0
                        )
                    )
                )
            except (
                ValueError,
                TypeError
            ):
                pass

        average_accuracy = (
            sum(accuracy_values)
            / len(accuracy_values)
            if accuracy_values
            else 0
        )

        # Update stat cards
        self.today_card.set_value(
            today_tests
        )

        self.best_wpm_card.set_value(
            f"{best_wpm:.2f}"
        )

        self.accuracy_card.set_value(
            f"{average_accuracy:.2f}%"
        )

        self.total_tests_card.set_value(
            total_tests
        )

        # Recent Activity — same reports, new visual rows.
        latest_reports = list(
            reports[-5:]
        )
        latest_reports.reverse()

        self.recent.set_reports(
            latest_reports
        )

    # =====================================================
    # AUTO REFRESH
    # =====================================================

    def showEvent(self, event):

        super().showEvent(event)
        self.load_dashboard_data()
