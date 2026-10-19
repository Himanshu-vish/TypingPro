from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QRadioButton,
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QProgressBar,
    QMessageBox,
    QFrame,
    QGridLayout
)

from PySide6.QtGui import (
    QFont,
    QTextCursor,
    QTextCharFormat,
    QColor
)

from PySide6.QtCore import (
    Qt,
    QEvent
)

from app.core.paragraph_loader import ParagraphLoader
from app.core.timer import TypingTimer
from app.core.typing_engine import TypingEngine
from app.core.statistics import TypingStatistics
from app.core.highlight_engine import HighlightEngine
from app.core.result_engine import ResultEngine
from app.ui.dialogs.result_dialog import ResultDialog
from app.core.exam_analyzer import ExamAnalyzer
from app.core.report_manager import ReportManager
from app.core.settings_manager import SettingsManager
from app.ui.dialogs.custom_test_dialog import CustomTestDialog, CustomResultDialog


class EnglishPage(QWidget):

    def __init__(self):
        super().__init__()

        # ==========================
        # Core Classes
        # ==========================

        self.timer = TypingTimer()
        self.engine = TypingEngine()
        self.stats = TypingStatistics()
        self.highlight = HighlightEngine()
        self.result_engine = ResultEngine()
        self.exam_analyzer = ExamAnalyzer()
        self.report_manager = ReportManager()
        self.settings_manager = SettingsManager()

        # Default Exam
        self.selected_exam = "UPP Computer Operator"

        # ==========================
        # Variables
        # ==========================

        self.selected_minutes = 5
        self.timer_started = False
        self.backspace_count = 0
        self.previous_text_length = 0

        # Custom Test defaults
        self.custom_target_wpm = 30
        self.custom_target_accuracy = 95
        self.custom_difficulty = "Easy"

        self.show_correct = True
        self.show_wrong = True
        self.show_current = True

        # Fast highlight caches
        self.current_paragraph_text = ""
        self.current_word_spans = []

        # ==========================
        # Build UI
        # ==========================

        self.build_ui()

        # ==========================
        # Signals
        # ==========================

        self.timer.time_changed.connect(
            self.update_time
        )

        self.timer.finished.connect(
            self.time_over
        )

        self.connect_timer_buttons()

        # Apply saved Settings preferences without changing typing/highlighter logic
        self.apply_saved_settings()

        self.update_time(
            self.selected_minutes * 60
        )

        self.highlight_text()

    # =====================================================
    # Build UI
    # =====================================================

    def build_ui(self):

        # =================================================
        # HINDI-MATCHED ENGLISH PAGE UI
        # UI ONLY — timer, highlighter, reports, exam mode
        # and all English typing business logic remain unchanged.
        # =================================================

        self.setObjectName("englishPage")

        self.setStyleSheet("""
            QWidget#englishPage {
                background: #F6F8FC;
                font-family: "Segoe UI";
            }

            QFrame#pageHero,
            QFrame#configCard,
            QFrame#statCard,
            QFrame#passageCard,
            QFrame#typingCard {
                background: #FFFFFF;
                border: 1px solid #DCE4ED;
                border-radius: 12px;
            }

            QFrame#pageHero {
                min-height: 72px;
            }

            QLabel#pageTitle {
                color: #102A49;
                font-size: 24px;
                font-weight: 700;
            }

            QLabel#pageSubtitle {
                color: #66768A;
                font-size: 11px;
                font-weight: 500;
            }

            QLabel#testTitle {
                color: #172E4B;
                font-size: 20px;
                font-weight: 700;
            }

            QLabel#configTitle {
                color: #17324F;
                font-size: 15px;
                font-weight: 700;
            }

            QLabel#fieldLabel {
                color: #41566E;
                font-size: 11px;
                font-weight: 700;
            }

            QLabel#cardHeading {
                color: #183450;
                font-size: 14px;
                font-weight: 700;
            }

            QLabel#cardHint {
                color: #7B8899;
                font-size: 9.5px;
                font-weight: 500;
            }

            QPushButton#backButton {
                background: #FFFFFF;
                color: #244B73;
                border: 1px solid #CFDBE8;
                border-radius: 8px;
                min-height: 34px;
                padding: 5px 13px;
                font-size: 10.5px;
                font-weight: 650;
            }

            QPushButton#backButton:hover {
                background: #F2F7FC;
                border-color: #9FB9D2;
            }

            QRadioButton {
                color: #30465E;
                spacing: 6px;
                padding: 5px 7px;
                font-size: 10.5px;
                font-weight: 600;
            }

            QRadioButton::indicator {
                width: 16px;
                height: 16px;
            }

            QCheckBox {
                color: #30465E;
                spacing: 6px;
                padding: 4px 3px;
                font-size: 10.5px;
                font-weight: 600;
            }

            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }

            QComboBox {
                background: #FFFFFF;
                color: #223B55;
                border: 1px solid #C9D5E2;
                border-radius: 8px;
                min-height: 38px;
                padding: 5px 31px 5px 11px;
                font-size: 11px;
                font-weight: 600;
            }

            QComboBox:hover {
                border-color: #9BB5CF;
            }

            QComboBox:focus {
                border: 1px solid #7B61E8;
            }

            QComboBox:disabled {
                background: #F0F3F7;
                color: #98A4B3;
            }

            QComboBox::drop-down {
                width: 29px;
                border: none;
            }

            QLabel#statCaption {
                color: #64768B;
                font-size: 9.5px;
                font-weight: 700;
            }

            QLabel#statValue {
                color: #142D49;
                font-size: 17px;
                font-weight: 750;
            }

            QLabel#timeValue {
                color: #1766C6;
                font-size: 17px;
                font-weight: 750;
            }

            QLabel#accuracyValue {
                color: #18A563;
                font-size: 17px;
                font-weight: 750;
            }

            QLabel#mistakeValue {
                color: #D93E4A;
                font-size: 17px;
                font-weight: 750;
            }

            QTextEdit#practicePassage {
                background: #FFFFFF;
                color: #111827;
                border: none;
                padding: 13px 15px;
                font-family: "Consolas";
                font-size: 20pt;
                font-weight: 500;
            }

            QTextEdit#typingInput {
                background: #FFFFFF;
                color: #111827;
                border: none;
                padding: 13px 15px;
                font-family: "Consolas";
                font-size: 20pt;
                font-weight: 500;
            }

            QFrame#typingCard {
                border: 1px solid #8A6CF0;
            }

            QPushButton#restartButton {
                background: #FFFFFF;
                color: #6B4ED8;
                border: 1px solid #A995ED;
                border-radius: 8px;
                min-height: 40px;
                padding: 6px 16px;
                font-size: 11px;
                font-weight: 700;
            }

            QPushButton#restartButton:hover {
                background: #F7F4FF;
                border-color: #8467DF;
            }

            QPushButton#nextButton {
                background: #6C35E4;
                color: #FFFFFF;
                border: 1px solid #6C35E4;
                border-radius: 8px;
                min-height: 40px;
                padding: 6px 18px;
                font-size: 11px;
                font-weight: 700;
            }

            QPushButton#nextButton:hover {
                background: #5E2DCB;
            }

            QProgressBar {
                background: #E8EDF3;
                border: none;
                border-radius: 4px;
                min-height: 8px;
                max-height: 8px;
                color: transparent;
            }

            QProgressBar::chunk {
                background: #6C35E4;
                border-radius: 4px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 14, 22, 16)
        layout.setSpacing(10)

        # =================================================
        # PAGE HERO
        # =================================================

        page_hero = QFrame()
        page_hero.setObjectName("pageHero")

        hero_layout = QHBoxLayout(page_hero)
        hero_layout.setContentsMargins(14, 10, 16, 10)
        hero_layout.setSpacing(13)

        self.back_btn = QPushButton("←  Back to Dashboard")
        self.back_btn.setObjectName("backButton")
        self.back_btn.setFixedWidth(155)

        title_box = QVBoxLayout()
        title_box.setSpacing(1)

        title = QLabel("English Typing")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Practice English typing with speed, accuracy and exam-ready practice"
        )
        subtitle.setObjectName("pageSubtitle")

        title_box.addWidget(title)
        title_box.addWidget(subtitle)

        hero_layout.addWidget(self.back_btn)
        hero_layout.addLayout(title_box)
        hero_layout.addStretch()

        layout.addWidget(page_hero)

        # =================================================
        # CENTERED TEST TITLE
        # =================================================

        test_title_row = QHBoxLayout()
        test_title_row.addStretch()

        test_title = QLabel("⌨  English Typing Test")
        test_title.setObjectName("testTitle")
        test_title.setAlignment(Qt.AlignCenter)

        test_title_row.addWidget(test_title)
        test_title_row.addStretch()

        layout.addLayout(test_title_row)

        # =================================================
        # CONFIGURATION CARD
        # =================================================

        config = QFrame()
        config.setObjectName("configCard")

        config_grid = QGridLayout(config)
        config_grid.setContentsMargins(16, 13, 16, 13)
        config_grid.setHorizontalSpacing(14)
        config_grid.setVerticalSpacing(12)

        duration_lbl = QLabel("◷  Select Test Duration")
        duration_lbl.setObjectName("configTitle")

        config_grid.addWidget(
            duration_lbl,
            0, 0, 1, 8
        )

        self.time_group = QButtonGroup(self)
        self.time_buttons = {}

        duration_row = QHBoxLayout()
        duration_row.setSpacing(12)

        for minute in [
            1, 2, 3, 5, 10, 15, 20, 25, 30
        ]:
            button = QRadioButton(
                f"{minute} Min"
            )

            if minute == 5:
                button.setChecked(True)

            self.time_group.addButton(button)
            self.time_buttons[minute] = button
            duration_row.addWidget(button)

        duration_row.addStretch()

        config_grid.addLayout(
            duration_row,
            1, 0, 1, 8
        )

        # =================================================
        # LIVE STATS IN LARGE CARDS
        # =================================================

        self.time_lbl = QLabel(
            "Remaining Time : 05:00"
        )
        self.paragraph_info_lbl = QLabel("")
        self.wpm_lbl = QLabel("WPM : 0")
        self.acc_lbl = QLabel("Accuracy : 100%")
        self.mistake_lbl = QLabel("Mistakes : 0")

        def make_stat_card(
            caption,
            value_label,
            kind
        ):
            card = QFrame()
            card.setObjectName("statCard")
            card.setMinimumHeight(72)

            card_layout = QHBoxLayout(card)
            card_layout.setContentsMargins(
                12, 8, 12, 8
            )
            card_layout.setSpacing(9)

            icon_map = {
                "time": "◷",
                "paragraph": "▤",
                "wpm": "◉",
                "accuracy": "◎",
                "mistake": "×"
            }

            color_map = {
                "time": ("#EAF3FF", "#1768D4"),
                "paragraph": ("#EBF7FB", "#17A3C3"),
                "wpm": ("#EEF4FB", "#315E8B"),
                "accuracy": ("#E9F8F0", "#159A59"),
                "mistake": ("#FDECEF", "#D83D4C")
            }

            bg, fg = color_map[kind]

            icon = QLabel(icon_map[kind])
            icon.setAlignment(Qt.AlignCenter)
            icon.setFixedSize(38, 38)
            icon.setStyleSheet(
                f"""
                QLabel {{
                    background:{bg};
                    color:{fg};
                    border-radius:19px;
                    font-size:17px;
                    font-weight:700;
                }}
                """
            )

            copy = QVBoxLayout()
            copy.setSpacing(0)

            caption_lbl = QLabel(caption)
            caption_lbl.setObjectName("statCaption")

            if kind == "time":
                value_label.setObjectName("timeValue")
            elif kind == "accuracy":
                value_label.setObjectName("accuracyValue")
            elif kind == "mistake":
                value_label.setObjectName("mistakeValue")
            else:
                value_label.setObjectName("statValue")

            copy.addWidget(caption_lbl)
            copy.addWidget(value_label)

            card_layout.addWidget(icon)
            card_layout.addLayout(copy, 1)

            return card

        stats = [
            make_stat_card(
                "REMAINING TIME",
                self.time_lbl,
                "time"
            ),
            make_stat_card(
                "PARAGRAPH",
                self.paragraph_info_lbl,
                "paragraph"
            ),
            make_stat_card(
                "WPM",
                self.wpm_lbl,
                "wpm"
            ),
            make_stat_card(
                "ACCURACY",
                self.acc_lbl,
                "accuracy"
            ),
            make_stat_card(
                "MISTAKES",
                self.mistake_lbl,
                "mistake"
            ),
        ]

        for col, card in enumerate(stats):
            config_grid.addWidget(
                card,
                2, col,
                1, 1
            )

        # Dedicated breathing space between stats and selectors.
        # This fixes Highlight Mode / Test Mode / Select Exam labels
        # visually touching the stat cards above.
        config_grid.setRowMinimumHeight(3, 16)

        # =================================================
        # MODE / EXAM / LEVEL / COLORS
        # =================================================

        highlight_lbl = QLabel("Highlight Mode")
        highlight_lbl.setObjectName("fieldLabel")

        self.highlight_mode_combo = QComboBox()
        self.highlight_mode_combo.addItems([
            "Character",
            "Word"
        ])
        self.highlight_mode_combo.setMinimumWidth(175)

        test_mode_lbl = QLabel("Test Mode")
        test_mode_lbl.setObjectName("fieldLabel")

        self.test_mode_combo = QComboBox()
        self.test_mode_combo.addItems([
            "Practice Mode",
            "Exam Mode",
            "Custom Test"
        ])
        self.test_mode_combo.setMinimumWidth(185)

        exam_lbl = QLabel("Select Exam")
        exam_lbl.setObjectName("fieldLabel")

        self.exam_combo = QComboBox()
        self.exam_combo.addItems(
            self.exam_analyzer.exam_names()
        )
        self.exam_combo.setCurrentText(
            self.selected_exam
        )
        self.exam_combo.setMinimumWidth(220)

        self.exam_combo.currentTextChanged.connect(
            self.change_exam
        )

        practice_lbl = QLabel("Practice")
        practice_lbl.setObjectName("fieldLabel")

        self.category_combo = QComboBox()
        self.category_combo.addItems([
            "Easy",
            "Medium",
            "Hard"
        ])
        self.category_combo.setMinimumWidth(150)

        colors_lbl = QLabel("Highlight Colors")
        colors_lbl.setObjectName("fieldLabel")

        colors_row = QHBoxLayout()
        colors_row.setSpacing(18)

        self.correct_check = QCheckBox("Green")
        self.correct_check.setChecked(True)

        self.wrong_check = QCheckBox("Red")
        self.wrong_check.setChecked(True)

        self.current_check = QCheckBox("Yellow")
        self.current_check.setChecked(True)

        colors_row.addWidget(self.correct_check)
        colors_row.addWidget(self.wrong_check)
        colors_row.addWidget(self.current_check)
        colors_row.addStretch()

        config_grid.addWidget(
            highlight_lbl, 4, 0
        )
        config_grid.addWidget(
            test_mode_lbl, 4, 1
        )
        config_grid.addWidget(
            exam_lbl, 4, 2
        )
        config_grid.addWidget(
            practice_lbl, 4, 3
        )
        config_grid.addWidget(
            colors_lbl, 4, 4
        )

        config_grid.addWidget(
            self.highlight_mode_combo,
            5, 0
        )
        config_grid.addWidget(
            self.test_mode_combo,
            5, 1
        )
        config_grid.addWidget(
            self.exam_combo,
            5, 2
        )
        config_grid.addWidget(
            self.category_combo,
            5, 3
        )
        config_grid.addLayout(
            colors_row,
            5, 4
        )

        layout.addWidget(config)

        # =================================================
        # PRACTICE PASSAGE — LARGE & READABLE
        # =================================================

        passage_card = QFrame()
        passage_card.setObjectName("passageCard")
        passage_card.setFixedHeight(190)

        passage_layout = QVBoxLayout(
            passage_card
        )
        passage_layout.setContentsMargins(
            0, 0, 0, 0
        )
        passage_layout.setSpacing(0)

        passage_header = QFrame()
        passage_header.setStyleSheet(
            "background:#FAFBFD;"
            "border:none;"
            "border-bottom:1px solid #E5EAF0;"
            "border-top-left-radius:12px;"
            "border-top-right-radius:12px;"
        )

        passage_header_layout = QHBoxLayout(
            passage_header
        )
        passage_header_layout.setContentsMargins(
            14, 8, 14, 8
        )

        passage_title = QLabel(
            "▣  Practice Passage"
        )
        passage_title.setObjectName(
            "cardHeading"
        )

        passage_hint = QLabel(
            "Read carefully and type exactly as shown"
        )
        passage_hint.setObjectName(
            "cardHint"
        )

        passage_header_layout.addWidget(
            passage_title
        )
        passage_header_layout.addStretch()
        passage_header_layout.addWidget(
            passage_hint
        )

        self.paragraph = QTextEdit()
        self.paragraph.setObjectName(
            "practicePassage"
        )
        self.paragraph.setReadOnly(True)

        # Bigger than the generated image for comfortable Hindi reading.
        self.paragraph.setFixedHeight(146)

        self.paragraph.setFont(
            QFont(
                "Consolas",
                20
            )
        )

        self.current_paragraph_text = (
            ParagraphLoader.get_paragraph(
                language="english",
                level="easy"
            )
        )

        self.current_word_spans = (
            self._build_word_spans(
                self.current_paragraph_text
            )
        )

        self.paragraph.setPlainText(
            self.current_paragraph_text
        )

        self.paragraph.setAlignment(
            Qt.AlignJustify
        )

        passage_layout.addWidget(
            passage_header
        )
        passage_layout.addWidget(
            self.paragraph
        )

        layout.addWidget(
            passage_card,
            1
        )

        # =================================================
        # TYPING AREA — LARGE & READABLE
        # =================================================

        typing_card = QFrame()
        typing_card.setObjectName("typingCard")
        typing_card.setFixedHeight(185)

        typing_layout = QVBoxLayout(
            typing_card
        )
        typing_layout.setContentsMargins(
            0, 0, 0, 0
        )
        typing_layout.setSpacing(0)

        typing_header = QFrame()
        typing_header.setStyleSheet(
            "background:#FAFBFD;"
            "border:none;"
            "border-bottom:1px solid #E5EAF0;"
            "border-top-left-radius:12px;"
            "border-top-right-radius:12px;"
        )

        typing_header_layout = QHBoxLayout(
            typing_header
        )
        typing_header_layout.setContentsMargins(
            14, 8, 14, 8
        )

        typing_title = QLabel(
            "✎  Typing Area"
        )
        typing_title.setObjectName(
            "cardHeading"
        )

        typing_hint = QLabel(
            "Start typing — timer begins automatically"
        )
        typing_hint.setObjectName(
            "cardHint"
        )

        typing_header_layout.addWidget(
            typing_title
        )
        typing_header_layout.addStretch()
        typing_header_layout.addWidget(
            typing_hint
        )

        self.typing_box = QTextEdit()
        self.typing_box.setObjectName(
            "typingInput"
        )

        self.typing_box.installEventFilter(
            self
        )

        self.typing_box.setFixedHeight(141)

        self.typing_box.setFont(
            QFont(
                "Consolas",
                20
            )
        )

        self.typing_box.setPlaceholderText(
            "Click here and start typing the passage..."
        )

        typing_layout.addWidget(
            typing_header
        )
        typing_layout.addWidget(
            self.typing_box
        )

        layout.addWidget(
            typing_card,
            1
        )

        # =================================================
        # PROGRESS + ACTIONS
        # =================================================

        footer = QHBoxLayout()
        footer.setSpacing(10)

        progress_label = QLabel("Progress")
        progress_label.setObjectName("cardHint")

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setMinimumWidth(340)

        self.progress_percent_lbl = QLabel("0%")
        self.progress_percent_lbl.setObjectName(
            "cardHint"
        )
        self.progress_percent_lbl.setFixedWidth(34)
        self.progress_percent_lbl.setAlignment(
            Qt.AlignRight | Qt.AlignVCenter
        )

        self.restart_btn = QPushButton(
            "↻  Restart"
        )
        self.restart_btn.setObjectName(
            "restartButton"
        )
        self.restart_btn.setMinimumWidth(116)

        self.next_btn = QPushButton(
            "Next Paragraph  →"
        )
        self.next_btn.setObjectName(
            "nextButton"
        )
        self.next_btn.setMinimumWidth(158)

        footer.addWidget(progress_label)
        footer.addWidget(self.progress, 1)
        footer.addWidget(
            self.progress_percent_lbl
        )
        footer.addSpacing(8)
        footer.addWidget(self.restart_btn)
        footer.addWidget(self.next_btn)

        layout.addLayout(footer)

        # =================================================
        # EXISTING SIGNALS — SAME FUNCTIONALITY
        # =================================================

        self.typing_box.textChanged.connect(
            self.on_typing
        )

        self.restart_btn.clicked.connect(
            self.restart_test
        )

        self.next_btn.clicked.connect(
            self.next_paragraph
        )

        self.category_combo.currentIndexChanged.connect(
            self.change_category
        )

        self.test_mode_combo.currentIndexChanged.connect(
            self.change_test_mode
        )

        self.correct_check.toggled.connect(
            lambda _checked:
            self.highlight_text()
        )

        self.wrong_check.toggled.connect(
            lambda _checked:
            self.highlight_text()
        )

        self.current_check.toggled.connect(
            lambda _checked:
            self.highlight_text()
        )

        self.highlight_mode_combo.currentIndexChanged.connect(
            self.highlight_text
        )

        self.progress.valueChanged.connect(
            lambda value:
            self.progress_percent_lbl.setText(
                f"{value}%"
            )
        )

    def apply_saved_settings(self):
        """
        Apply UI/default preferences only.
        IMPORTANT: this method does NOT modify the typing or highlighting
        algorithm. It only sets the existing controls.
        """
        data = self.settings_manager.all()

        # Duration
        try:
            minute = int(data.get("default_duration", 5))
        except (TypeError, ValueError):
            minute = 5

        if minute in self.time_buttons:
            self.time_buttons[minute].setChecked(True)
            self.selected_minutes = minute
            self.timer.reset(minute)
            self.update_time(minute * 60)

        # Test mode
        mode = str(data.get("default_test_mode", "Practice Mode"))
        if self.test_mode_combo.findText(mode) >= 0:
            self.test_mode_combo.blockSignals(True)
            self.test_mode_combo.setCurrentText(mode)
            self.test_mode_combo.blockSignals(False)

        # Preserve the existing enable/disable behaviour without triggering restart.
        if mode == "Exam Mode":
            self.category_combo.setEnabled(False)
            self.exam_combo.setEnabled(True)
        else:
            self.category_combo.setEnabled(True)
            self.exam_combo.setEnabled(False)

        # Highlight mode
        highlight_mode = str(
            data.get("default_highlight_mode", "Character")
        )
        if self.highlight_mode_combo.findText(highlight_mode) >= 0:
            self.highlight_mode_combo.blockSignals(True)
            self.highlight_mode_combo.setCurrentText(highlight_mode)
            self.highlight_mode_combo.blockSignals(False)

        # Existing Green / Red / Yellow controls
        self.correct_check.setChecked(
            bool(data.get("show_correct", True))
        )
        self.wrong_check.setChecked(
            bool(data.get("show_wrong", True))
        )
        self.current_check.setChecked(
            bool(data.get("show_current", True))
        )

        # Refresh only through the page's existing highlighter.
        self.highlight_text()

    def refresh_settings(self):
        """Called when the page is shown so newly saved Settings take effect."""
        self.apply_saved_settings()

        if self.settings_manager.get("auto_focus_typing_box"):
            self.typing_box.setFocus()

    def showEvent(self, event):
        super().showEvent(event)
        self.refresh_settings()

    # =====================================================
    # Timer Methods
    # =====================================================

    def update_time(
        self,
        seconds
    ):

        minutes = seconds // 60

        secs = seconds % 60

        self.time_lbl.setText(
            f"Remaining Time : "
            f"{minutes:02}:{secs:02}"
        )

    # =====================================================
    # Time Over
    # =====================================================

    def time_over(self):

        self.timer.stop()

        self.stats.stop()

        self.typing_box.setReadOnly(
            True
        )

        self.time_lbl.setText(
            "Time Over"
        )

        # =====================================
        # Generate Result
        # =====================================

        elapsed_seconds = (
            self.selected_minutes * 60
        )

        self.result_engine.generate(
            correct_chars=self.engine.correct_chars,
            wrong_chars=self.engine.wrong_chars,
            elapsed_seconds=elapsed_seconds,
            backspace_count=self.backspace_count
        )

        # =====================================
        # Prepare Result Data
        # =====================================

        result = {

            "gross_wpm":
                self.result_engine.gross_wpm,

            "net_wpm":
                self.result_engine.net_wpm,

            "accuracy":
                self.result_engine.accuracy,

            "correct_chars":
                self.result_engine.correct_chars,

            "wrong_chars":
                self.result_engine.wrong_chars,

            "backspace":
                self.result_engine.backspace,

            "total_keystrokes":
                self.result_engine.total_keystrokes

        }

        self.report_manager.save_result(
        language="English",
        mode=self.test_mode_combo.currentText(),
        exam=self.selected_exam,
        duration=self.selected_minutes,
        net_wpm=self.result_engine.net_wpm,
        gross_wpm=self.result_engine.gross_wpm,
        accuracy=self.result_engine.accuracy,
        mistakes=self.result_engine.wrong_chars,
        correct_chars=self.result_engine.correct_chars,
        wrong_chars=self.result_engine.wrong_chars,
        backspace=self.result_engine.backspace,
        custom_target_wpm=(
            self.custom_target_wpm
            if self.test_mode_combo.currentText() == "Custom Test"
            else None
        ),
        custom_target_accuracy=(
            self.custom_target_accuracy
            if self.test_mode_combo.currentText() == "Custom Test"
            else None
        ),
        custom_result=self.custom_result_status(result)
    )

        # =====================================
        # Show Result Dialog
        # =====================================

        self.show_final_result(result)

    # =====================================================
    # Paragraph Completed
    # =====================================================

    def paragraph_completed(self):

        # ==========================
        # Stop Timer
        # ==========================

        self.timer.stop()

        self.timer_started = False

        # ==========================
        # Stop Statistics
        # ==========================

        self.stats.stop()

        # ==========================
        # Lock Typing
        # ==========================

        self.typing_box.setReadOnly(
            True
        )

        # ==========================
        # Progress
        # ==========================

        self.progress.setValue(
            100
        )

        # ==========================
        # Calculate Elapsed Time
        # ==========================

        elapsed_seconds = (
            self.selected_minutes * 60
            - self.timer.remaining_seconds
        )

        if elapsed_seconds <= 0:

            elapsed_seconds = 1

        # ==========================
        # Generate Result
        # ==========================

        self.result_engine.generate(
            correct_chars=self.engine.correct_chars,
            wrong_chars=self.engine.wrong_chars,
            elapsed_seconds=elapsed_seconds,
            backspace_count=self.backspace_count
        )

        # ==========================
        # Result Data
        # ==========================

        result = {

            "gross_wpm":
                self.result_engine.gross_wpm,

            "net_wpm":
                self.result_engine.net_wpm,

            "accuracy":
                self.result_engine.accuracy,

            "correct_chars":
                self.result_engine.correct_chars,

            "wrong_chars":
                self.result_engine.wrong_chars,

            "backspace":
                self.result_engine.backspace,

            "total_keystrokes":
                self.result_engine.total_keystrokes

        }

        self.report_manager.save_result(
        language="English",
        mode=self.test_mode_combo.currentText(),
        exam=self.selected_exam,
        duration=self.selected_minutes,
        net_wpm=self.result_engine.net_wpm,
        gross_wpm=self.result_engine.gross_wpm,
        accuracy=self.result_engine.accuracy,
        mistakes=self.result_engine.wrong_chars,
        correct_chars=self.result_engine.correct_chars,
        wrong_chars=self.result_engine.wrong_chars,
        backspace=self.result_engine.backspace,
        custom_target_wpm=(
            self.custom_target_wpm
            if self.test_mode_combo.currentText() == "Custom Test"
            else None
        ),
        custom_target_accuracy=(
            self.custom_target_accuracy
            if self.test_mode_combo.currentText() == "Custom Test"
            else None
        ),
        custom_result=self.custom_result_status(result)
    )


        # ==========================
        # Show Result
        # ==========================

        self.show_final_result(result)

    # =====================================================
    # Timer Buttons
    # =====================================================

    def connect_timer_buttons(self):

        for minute, button in self.time_buttons.items():

            button.toggled.connect(
                lambda checked, m=minute:
                self.change_time(
                    m,
                    checked
                )
            )

    # =====================================================
    # Change Time
    # =====================================================

    def change_time(
        self,
        minute,
        checked
    ):

        if not checked:
            return

        self.selected_minutes = minute

        self.timer.reset(
            minute
        )

        self.timer_started = False

        self.typing_box.clear()

        self.backspace_count = 0

        self.previous_text_length = 0

        self.typing_box.setReadOnly(
            False
        )

        self.engine.reset()

        self.stats.reset()

        self.update_time(
            minute * 60
        )

        self.progress.setValue(
            0
        )


        self.progress.setMaximum(
            1000
        )

        self.progress.setValue(
            0
        )

        self.progress.setFormat(
            "0.0%"
        )

        self.highlight_text()

    # =====================================================
    # Typing
    # =====================================================

    def on_typing(self):

        text = (
            self.typing_box.toPlainText()
        )

        # ==========================
        # Backspace Detection
        # ==========================

        current_length = len(text)

        if (
            current_length
            <
            self.previous_text_length
        ):

            self.backspace_count += (
                self.previous_text_length
                -
                current_length
            )

        self.previous_text_length = (
            current_length
        )

        # ==========================
        # Start Timer
        # ==========================

        if (
            not self.timer_started
            and len(text) > 0
        ):

            self.timer.start(
                self.selected_minutes
            )

            self.stats.start()

            self.timer_started = True

        # ==========================
        # Original Paragraph
        # ==========================

        original = self.current_paragraph_text

        # ==========================
        # Typing Engine
        # ==========================

        self.engine.check(
            original,
            text
        )

        # ==========================
        # Statistics
        # ==========================

        self.stats.update(
            self.engine.correct_chars,
            self.engine.wrong_chars
        )

        self.wpm_lbl.setText(
            f"WPM : "
            f"{self.stats.wpm()}"
        )

        self.acc_lbl.setText(
            f"Accuracy : "
            f"{self.stats.accuracy()}%"
        )

        self.mistake_lbl.setText(
            f"Mistakes : "
            f"{self.stats.mistakes()}"
        )

        # ==========================
        # Highlight
        # ==========================

        self.highlight_text()

        # Keep the currently typed/highlighted position visible in the
        # read-only practice passage. This only moves the passage viewport;
        # it does not change typing/highlight calculations.
        self._follow_highlight_scroll(len(text))

        # ==========================
        # Progress
        # ==========================

        original_length = len(
            original
        )

        typed_length = len(
            text
        )

        if original_length > 0:

            ratio = min(
                typed_length
                / original_length,
                1.0
            )

            # Use 0-1000 so the bar visibly moves even
            # with very long paragraph files.
            self.progress.setMaximum(
                1000
            )

            self.progress.setValue(
                int(
                    ratio * 1000
                )
            )

            self.progress.setFormat(
                f"{ratio * 100:.1f}%"
            )

        # ==========================
        # Paragraph Complete
        # ==========================

        if (
            typed_length
            ==
            original_length
            and
            text
            ==
            original
        ):

            self.paragraph_completed()

    # =====================================================
    # Restart Test
    # =====================================================

    def restart_test(self):

        self.timer.stop()

        self.timer.reset(
            self.selected_minutes
        )

        self.timer_started = False

        self.engine.reset()

        self.stats.reset()

        self.typing_box.clear()
        # Clear old Green / Red / Yellow highlights
        self.paragraph.setExtraSelections([])

        self.typing_box.setReadOnly(
            False
        )

        self.update_time(
            self.selected_minutes * 60
        )

        self.wpm_lbl.setText(
            "WPM : 0"
        )

        self.acc_lbl.setText(
            "Accuracy : 100%"
        )

        self.mistake_lbl.setText(
            "Mistakes : 0"
        )

        self.progress.setValue(
            0
        )

        self.backspace_count = 0

        self.previous_text_length = 0


        self.progress.setMaximum(
            1000
        )

        self.progress.setValue(
            0
        )

        self.progress.setFormat(
            "0.0%"
        )

        self.highlight_text()

    # =====================================================
    # Next Paragraph
    # =====================================================

    def next_paragraph(self):

        self.restart_test()

        level = (
            self.category_combo
            .currentText()
            .lower()
        )

        self.current_paragraph_text = (
            ParagraphLoader.get_paragraph(
                language="english",
                level=level
            )
        )

        self.current_word_spans = self._build_word_spans(
            self.current_paragraph_text
        )

        self.paragraph.setPlainText(
            self.current_paragraph_text
        )

        self.paragraph.setExtraSelections([])

        self.paragraph.setAlignment(
            Qt.AlignJustify
        )


        self.update_paragraph_info()

        self.progress.setValue(
            0
        )

        self.highlight_text()

    # =====================================================
    # Change Category
    # =====================================================

    def change_category(self):

        self.restart_test()

        level = (
            self.category_combo
            .currentText()
            .lower()
        )

        self.current_paragraph_text = (
            ParagraphLoader.get_paragraph(
                language="english",
                level=level
            )
        )

        self.current_word_spans = self._build_word_spans(
            self.current_paragraph_text
        )

        self.paragraph.setPlainText(
            self.current_paragraph_text
        )
        self.paragraph.setExtraSelections([])

        self.update_paragraph_info()

        self.progress.setValue(
            0
        )

        self.highlight_text()

    # =====================================================
    # Exam Selection
    # =====================================================

    def change_exam(
        self,
        exam_name
    ):

        self.selected_exam = (
            exam_name
        )

    # =====================================================
    # Custom Test
    # =====================================================

    def configure_custom_test(self):

        dialog = CustomTestDialog(
            self,
            duration=self.selected_minutes,
            target_wpm=self.custom_target_wpm,
            target_accuracy=self.custom_target_accuracy,
            difficulty=self.category_combo.currentText()
        )

        if dialog.exec() != dialog.Accepted:
            return False

        values = dialog.values()

        self.custom_target_wpm = values["target_wpm"]
        self.custom_target_accuracy = values["target_accuracy"]
        self.custom_difficulty = values["difficulty"]

        minute = values["duration"]

        # Custom Test timer must always use the exact custom duration.
        # Do not depend on the normal preset timer radio buttons.
        self.selected_minutes = minute

        # Clear preset timer selection first so a custom value like
        # 7 Min does not visually leave 5 Min selected.
        self.time_group.setExclusive(False)

        for button in self.time_buttons.values():
            button.setChecked(False)

        self.time_group.setExclusive(True)

        # If the custom duration matches a normal preset, show it selected.
        if minute in self.time_buttons:

            self.time_buttons[minute].blockSignals(True)
            self.time_buttons[minute].setChecked(True)
            self.time_buttons[minute].blockSignals(False)

        self.timer.stop()
        self.timer.reset(minute)

        self.timer_started = False

        self.typing_box.clear()
        self.typing_box.setReadOnly(False)

        self.engine.reset()
        self.stats.reset()

        self.backspace_count = 0
        self.previous_text_length = 0

        self.update_time(
            minute * 60
        )

        self.progress.setValue(
            0
        )

        self.category_combo.setCurrentText(
            self.custom_difficulty
        )

        return True


    def show_final_result(self, result):

        if self.test_mode_combo.currentText() == "Custom Test":

            dialog = CustomResultDialog(
                result,
                self.custom_target_wpm,
                self.custom_target_accuracy,
                self
            )

        else:

            dialog = ResultDialog(
                result,
                self,
                self.selected_exam
            )

        dialog.exec()


    def custom_result_status(self, result):

        if self.test_mode_combo.currentText() != "Custom Test":
            return None

        return CustomResultDialog.status(
            result,
            self.custom_target_wpm,
            self.custom_target_accuracy
        )


    # =====================================================
    # Test Mode
    # =====================================================

    def change_test_mode(self):

        mode = (
            self.test_mode_combo
            .currentText()
        )

        # =====================================
        # Practice Mode
        # =====================================

        if mode == "Practice Mode":

            self.category_combo.setEnabled(
                True
            )

            self.exam_combo.setEnabled(
                False
            )

        # =====================================
        # Exam Mode
        # =====================================

        elif mode == "Exam Mode":

            self.category_combo.setEnabled(
                False
            )

            self.exam_combo.setEnabled(
                True
            )

        # =====================================
        # Custom Test
        # =====================================

        elif mode == "Custom Test":

            self.category_combo.setEnabled(
                True
            )

            self.exam_combo.setEnabled(
                False
            )

            if not self.configure_custom_test():

                self.test_mode_combo.blockSignals(
                    True
                )

                self.test_mode_combo.setCurrentText(
                    "Practice Mode"
                )

                self.test_mode_combo.blockSignals(
                    False
                )

                self.category_combo.setEnabled(
                    True
                )

                self.exam_combo.setEnabled(
                    False
                )

                return

        # =====================================
        # Reset Test
        # =====================================

        self.restart_test()

    # =====================================================
    # Highlight Helpers
    # =====================================================

    def _build_word_spans(self, text):

        spans = []
        i = 0
        length = len(text)

        while i < length:

            while (
                i < length
                and text[i].isspace()
            ):
                i += 1

            if i >= length:
                break

            start = i

            while (
                i < length
                and not text[i].isspace()
            ):
                i += 1

            spans.append(
                (
                    start,
                    i,
                    text[start:i]
                )
            )

        return spans


    def _add_extra_selection(
        self,
        selections,
        start,
        end,
        foreground=None,
        background=None
    ):

        if start >= end:
            return

        selection = QTextEdit.ExtraSelection()

        cursor = self.paragraph.textCursor()
        cursor.setPosition(start)
        cursor.setPosition(
            end,
            QTextCursor.KeepAnchor
        )

        selection.cursor = cursor

        fmt = QTextCharFormat()

        if foreground is not None:
            fmt.setForeground(foreground)

        if background is not None:
            fmt.setBackground(background)

        selection.format = fmt

        selections.append(selection)


    # =====================================================
    # FINAL STABLE HIGHLIGHT
    #
    # Character:
    # correct = dark green
    # wrong   = dark red
    # current = yellow
    #
    # Word:
    # completed correct = dark green
    # completed wrong   = dark red
    # current correct   = black on yellow
    # current wrong     = dark red on yellow
    #
    # IMPORTANT:
    # No global matching / no SequenceMatcher / no pointer jump.
    # =====================================================

    def highlight_text(self):

        mode = (
            self.highlight_mode_combo
            .currentText()
        )

        original = (
            self.paragraph.toPlainText()
        )

        typed = (
            self.typing_box.toPlainText()
        )

        if mode == "Character":

            self.highlight.highlight(
                self.paragraph,
                original,
                typed,
                self.correct_check.isChecked(),
                self.wrong_check.isChecked(),
                self.current_check.isChecked()
            )

        elif mode == "Word":

            self.highlight.highlight_words(
                self.paragraph,
                original,
                typed,
                self.correct_check.isChecked(),
                self.wrong_check.isChecked(),
                self.current_check.isChecked()
            )

    def _follow_highlight_scroll(self, typed_length):
        """Keep the active character/word visible in the practice passage."""
        try:
            doc = self.paragraph.document()
            max_pos = max(0, doc.characterCount() - 1)
            pos = max(0, min(int(typed_length), max_pos))
            cursor = QTextCursor(doc)
            cursor.setPosition(pos)
            self.paragraph.setTextCursor(cursor)
            self.paragraph.ensureCursorVisible()
        except (TypeError, ValueError, RuntimeError):
            pass

    # =====================================================
    # Paragraph Information
    # =====================================================

    def update_paragraph_info(self):

        current, total = (
            ParagraphLoader.paragraph_info()
        )

        self.paragraph_info_lbl.setText(

            f"Paragraph : "
            f"{current} / {total}"

        )

    # =====================================================
    # Live Stats
    # =====================================================

    def update_live_stats(self):

        self.wpm_lbl.setText(
            f"WPM : "
            f"{self.result_engine.net_wpm}"
        )

        self.acc_lbl.setText(
            f"Accuracy : "
            f"{self.result_engine.accuracy}%"
        )

        self.mistake_lbl.setText(
            f"Mistakes : "
            f"{self.result_engine.wrong_chars}"
        )

        self.update_paragraph_info()

    # =====================================================
    # Event Filter
    # =====================================================

    def eventFilter(
        self,
        obj,
        event
    ):

        if obj == self.typing_box:

            if event.type() == QEvent.KeyPress:

                if event.key() == Qt.Key_Backspace:

                    self.backspace_count += 1

        return super().eventFilter(
            obj,
            event
        )