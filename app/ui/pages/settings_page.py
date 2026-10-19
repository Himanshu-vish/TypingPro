from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QCheckBox,
    QPushButton,
    QGroupBox,
    QFormLayout,
    QMessageBox,
    QScrollArea,
    QGridLayout,
    QFrame
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from app.core.settings_manager import SettingsManager


class SettingsPage(QWidget):

    def __init__(self):
        super().__init__()

        self.settings_manager = SettingsManager()

        self.build_ui()
        self.load_settings()

    def build_ui(self):

        self.setObjectName("settingsPage")
        self.setStyleSheet("""
            QWidget#settingsPage {
                background:#F4F7FB;
                font-family:"Segoe UI";
            }

            QFrame#heroPanel {
                background:#FFFFFF;
                border:1px solid #DCE5EF;
                border-radius:16px;
            }
            QLabel#heroIcon {
                background:#E8F1FF;
                color:#1769D5;
                border-radius:26px;
                font-size:25px;
                font-weight:800;
            }
            QLabel#pageTitle {
                color:#102A49;
                font-size:28px;
                font-weight:800;
            }
            QLabel#pageSubtitle {
                color:#455B72;
                font-size:14px;
                font-weight:650;
            }

            QFrame#settingsCard {
                background:#FFFFFF;
                border:1px solid #D9E3EE;
                border-radius:14px;
            }
            QLabel#cardTitle {
                color:#17324F;
                font-size:19px;
                font-weight:800;
            }
            QLabel#cardSubtitle {
                color:#4D6177;
                font-size:13px;
                font-weight:650;
            }
            QLabel#sectionIcon {
                border-radius:22px;
                min-width:44px;
                min-height:44px;
                max-width:44px;
                max-height:44px;
                font-size:19px;
                font-weight:800;
            }
            QLabel#fieldTitle {
                color:#20364D;
                font-size:15px;
                font-weight:750;
            }
            QLabel#fieldHelp {
                color:#566B80;
                font-size:12.5px;
                font-weight:600;
            }

            QComboBox {
                background:#FBFDFF;
                color:#18324E;
                border:1.5px solid #B9C9DA;
                border-radius:10px;
                min-height:44px;
                padding:5px 44px 5px 14px;
                font-size:15px;
                font-weight:700;
            }
            QComboBox:hover {
                background:#FFFFFF;
                border-color:#6D9BD0;
            }
            QComboBox:focus {
                background:#FFFFFF;
                border:2px solid #2879D8;
            }
            QComboBox::drop-down {
                subcontrol-origin:padding;
                subcontrol-position:top right;
                width:40px;
                border-left:1px solid #D5DFEA;
                background:#EFF5FB;
                border-top-right-radius:9px;
                border-bottom-right-radius:9px;
            }
            QComboBox QAbstractItemView {
                background:#FFFFFF;
                color:#17324F;
                border:1px solid #BFCEDF;
                selection-background-color:#E7F1FF;
                selection-color:#102A49;
                padding:8px;
                font-size:15px;
                font-weight:650;
                outline:0;
            }

            QCheckBox {
                color:#20364D;
                spacing:10px;
                font-size:14px;
                font-weight:700;
                min-height:34px;
            }
            QCheckBox::indicator {
                width:20px;
                height:20px;
            }

            QPushButton#primaryButton,
            QPushButton#secondaryButton {
                min-height:44px;
                border-radius:10px;
                padding:7px 20px;
                font-size:14px;
                font-weight:800;
            }
            QPushButton#primaryButton {
                background:#1268E0;
                color:#FFFFFF;
                border:1px solid #1268E0;
            }
            QPushButton#primaryButton:hover { background:#0D5EC9; }
            QPushButton#secondaryButton {
                background:#FFFFFF;
                color:#175FC4;
                border:1px solid #BCD0E4;
            }
            QPushButton#secondaryButton:hover {
                background:#F2F7FD;
                border-color:#83A8CE;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 14, 24, 14)
        main_layout.setSpacing(10)

        # ---------------- HERO ----------------
        hero = QFrame()
        hero.setObjectName("heroPanel")
        hero_l = QHBoxLayout(hero)
        hero_l.setContentsMargins(18, 11, 18, 11)
        hero_l.setSpacing(14)

        hero_icon = QLabel("⚙")
        hero_icon.setObjectName("heroIcon")
        hero_icon.setFixedSize(48, 48)
        hero_icon.setAlignment(Qt.AlignCenter)

        hero_copy = QVBoxLayout()
        hero_copy.setSpacing(1)
        title = QLabel("Settings")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Customize TypingPro exactly the way you want")
        subtitle.setObjectName("pageSubtitle")
        hero_copy.addWidget(title)
        hero_copy.addWidget(subtitle)

        hero_l.addWidget(hero_icon)
        hero_l.addLayout(hero_copy, 1)
        main_layout.addWidget(hero)

        def divider():
            line = QFrame()
            line.setFixedHeight(1)
            line.setStyleSheet("background:#E6ECF3;border:none;")
            return line

        def make_card(icon_text, title_text, subtitle_text, bg, fg):
            card = QFrame()
            card.setObjectName("settingsCard")
            outer = QVBoxLayout(card)
            outer.setContentsMargins(16, 13, 16, 14)
            outer.setSpacing(10)

            head = QHBoxLayout()
            head.setSpacing(12)

            icon = QLabel(icon_text)
            icon.setObjectName("sectionIcon")
            icon.setAlignment(Qt.AlignCenter)
            icon.setStyleSheet(
                f"background:{bg};color:{fg};border:1px solid {fg}22;border-radius:22px;"
                "font-size:19px;font-weight:800;"
            )

            copy = QVBoxLayout()
            copy.setSpacing(1)
            h = QLabel(title_text)
            h.setObjectName("cardTitle")
            sub = QLabel(subtitle_text)
            sub.setObjectName("cardSubtitle")
            copy.addWidget(h)
            copy.addWidget(sub)

            head.addWidget(icon)
            head.addLayout(copy, 1)
            outer.addLayout(head)
            outer.addWidget(divider())
            return card, outer

        def control_block(title_text, help_text, control):
            block = QVBoxLayout()
            block.setSpacing(7)
            h = QLabel(title_text)
            h.setObjectName("fieldTitle")
            help_lbl = QLabel(help_text)
            help_lbl.setObjectName("fieldHelp")
            help_lbl.setWordWrap(True)
            block.addWidget(h)
            block.addWidget(help_lbl)
            block.addWidget(control)
            return block

        grid = QGridLayout()
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(10)

        # ---------------- GENERAL ----------------
        general, gl = make_card(
            "◉", "General Preferences",
            "Default language, duration and test mode",
            "#E8F1FF", "#1769D5"
        )

        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "Hindi"])
        self.language_combo.setMinimumWidth(250)

        self.duration_combo = QComboBox()
        self.duration_combo.addItems(["1", "2", "3", "5", "10", "15", "20", "25", "30"])
        self.duration_combo.setMinimumWidth(250)

        self.test_mode_combo = QComboBox()
        self.test_mode_combo.addItems(["Practice Mode", "Exam Mode", "Custom Test"])
        self.test_mode_combo.setMinimumWidth(250)

        row = QHBoxLayout()
        row.setSpacing(14)
        row.addLayout(control_block("Default Language", "Language selected when TypingPro opens.", self.language_combo), 1)
        row.addLayout(control_block("Default Duration", "Default typing test duration in minutes.", self.duration_combo), 1)
        row.addLayout(control_block("Default Test Mode", "Practice, exam or custom test mode.", self.test_mode_combo), 1)
        gl.addLayout(row)
        grid.addWidget(general, 0, 0, 1, 2)

        # ---------------- HIGHLIGHT ----------------
        highlight, hl = make_card(
            "✎", "Typing Highlight",
            "Control live typing feedback and highlight behaviour",
            "#E6F8EE", "#169457"
        )

        self.highlight_mode_combo = QComboBox()
        self.highlight_mode_combo.addItems(["Character", "Word"])
        hl.addLayout(control_block(
            "Default Highlight Mode",
            "Choose whether TypingPro highlights one character or one word at a time.",
            self.highlight_mode_combo
        ))

        self.correct_check = QCheckBox("Correct = Green")
        self.wrong_check = QCheckBox("Wrong = Red")
        self.current_check = QCheckBox("Current = Yellow")

        feedback_title = QLabel("Highlight Colors")
        feedback_title.setObjectName("fieldTitle")
        hl.addWidget(feedback_title)

        feedback_row = QHBoxLayout()
        feedback_row.setSpacing(14)
        feedback_row.addWidget(self.correct_check)
        feedback_row.addWidget(self.wrong_check)
        feedback_row.addWidget(self.current_check)
        feedback_row.addStretch()
        hl.addLayout(feedback_row)
        grid.addWidget(highlight, 1, 0)

        # ---------------- BEHAVIOUR ----------------
        behaviour, bl = make_card(
            "◆", "Application Behaviour",
            "Control how TypingPro behaves while you practice",
            "#F0E9FF", "#673CC8"
        )

        self.remember_check = QCheckBox("Remember last selected typing options")
        self.focus_check = QCheckBox("Automatically focus typing box when a typing page opens")

        bl.addWidget(self.remember_check)
        helper = QLabel("Restore your previous language, duration and practice options.")
        helper.setObjectName("fieldHelp")
        helper.setWordWrap(True)
        bl.addWidget(helper)
        bl.addWidget(divider())
        bl.addWidget(self.focus_check)
        helper2 = QLabel("Start typing immediately without clicking inside the typing box.")
        helper2.setObjectName("fieldHelp")
        helper2.setWordWrap(True)
        bl.addWidget(helper2)
        grid.addWidget(behaviour, 1, 1)

        # ---------------- REPORT SAFETY ----------------
        report_card, rl = make_card(
            "▣", "Reports & Data Safety",
            "Prevent accidental removal of typing history",
            "#FFF0DD", "#D9780B"
        )

        self.confirm_clear_check = QCheckBox("Ask before clearing full report history")
        self.confirm_delete_check = QCheckBox("Ask before deleting a selected report")

        safety_row = QHBoxLayout()
        safety_row.setSpacing(24)

        clear_box = QVBoxLayout()
        clear_box.setSpacing(3)
        clear_box.addWidget(self.confirm_clear_check)
        r1 = QLabel("Confirm before removing all saved reports.")
        r1.setObjectName("fieldHelp")
        clear_box.addWidget(r1)

        delete_box = QVBoxLayout()
        delete_box.setSpacing(3)
        delete_box.addWidget(self.confirm_delete_check)
        r2 = QLabel("Confirm before deleting a selected report.")
        r2.setObjectName("fieldHelp")
        delete_box.addWidget(r2)

        safety_row.addLayout(clear_box, 1)
        safety_row.addLayout(delete_box, 1)
        rl.addLayout(safety_row)
        grid.addWidget(report_card, 2, 0, 1, 2)

        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        main_layout.addLayout(grid, 1)

        # ---------------- ACTION BAR ----------------
        actions = QHBoxLayout()
        actions.setSpacing(10)

        self.save_btn = QPushButton("✓  Save Settings")
        self.save_btn.setObjectName("primaryButton")
        self.save_btn.setMinimumWidth(190)

        self.reset_btn = QPushButton("↻  Reset to Default")
        self.reset_btn.setObjectName("secondaryButton")
        self.reset_btn.setMinimumWidth(185)

        self.reload_btn = QPushButton("↻  Reload")
        self.reload_btn.setObjectName("secondaryButton")
        self.reload_btn.setMinimumWidth(135)

        actions.addStretch()
        actions.addWidget(self.reload_btn)
        actions.addWidget(self.reset_btn)
        actions.addWidget(self.save_btn)
        main_layout.addLayout(actions)

        self.save_btn.clicked.connect(self.save_settings)
        self.reset_btn.clicked.connect(self.reset_settings)
        self.reload_btn.clicked.connect(self.load_settings)

    def load_settings(self):

        data = self.settings_manager.all()

        self.language_combo.setCurrentText(
            data["default_language"]
        )

        self.duration_combo.setCurrentText(
            str(data["default_duration"])
        )

        self.test_mode_combo.setCurrentText(
            data["default_test_mode"]
        )

        self.highlight_mode_combo.setCurrentText(
            data["default_highlight_mode"]
        )

        self.correct_check.setChecked(
            data["show_correct"]
        )

        self.wrong_check.setChecked(
            data["show_wrong"]
        )

        self.current_check.setChecked(
            data["show_current"]
        )

        self.remember_check.setChecked(
            data["remember_last_selection"]
        )

        self.focus_check.setChecked(
            data["auto_focus_typing_box"]
        )

        self.confirm_clear_check.setChecked(
            data["confirm_clear_history"]
        )

        self.confirm_delete_check.setChecked(
            data["confirm_delete_report"]
        )

    def save_settings(self):

        values = {
            "default_language":
                self.language_combo.currentText(),

            "default_duration":
                int(
                    self.duration_combo.currentText()
                ),

            "default_test_mode":
                self.test_mode_combo.currentText(),

            "default_highlight_mode":
                self.highlight_mode_combo.currentText(),

            "show_correct":
                self.correct_check.isChecked(),

            "show_wrong":
                self.wrong_check.isChecked(),

            "show_current":
                self.current_check.isChecked(),

            "remember_last_selection":
                self.remember_check.isChecked(),

            "auto_focus_typing_box":
                self.focus_check.isChecked(),

            "confirm_clear_history":
                self.confirm_clear_check.isChecked(),

            "confirm_delete_report":
                self.confirm_delete_check.isChecked()
        }

        self.settings_manager.save_all(
            values
        )

        QMessageBox.information(
            self,
            "Settings Saved",
            "Settings saved successfully."
        )

    def reset_settings(self):

        reply = QMessageBox.question(
            self,
            "Reset Settings",
            "Reset all settings to default values?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        self.settings_manager.reset_defaults()
        self.load_settings()

        QMessageBox.information(
            self,
            "Settings Reset",
            "All settings have been reset to default."
        )

    def showEvent(
        self,
        event
    ):

        super().showEvent(event)
        self.load_settings()
