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
    QGridLayout,
    QSizePolicy,
    QLayout
)

from PySide6.QtGui import (
    QFont,
    QTextCursor,
    QTextCharFormat,
    QColor
)
from PySide6.QtCore import Qt, QEvent, QTimer

from app.core.paragraph_loader import ParagraphLoader
from app.core.timer import TypingTimer
from app.core.typing_engine import TypingEngine
from app.core.statistics import TypingStatistics
from app.core.highlight_engine import HighlightEngine
from app.core.result_engine import ResultEngine
from app.core.exam_analyzer import ExamAnalyzer
from app.ui.dialogs.result_dialog import ResultDialog
from app.core.report_manager import ReportManager
from app.core.settings_manager import SettingsManager
from app.ui.dialogs.custom_test_dialog import CustomTestDialog, CustomResultDialog

class HindiPage(QWidget):

    # =====================================================
    # INTERNAL HINDI INSCRIPT KEYBOARD
    # =====================================================

    INSCRIPT_MAP = {
        # Normal keys
        "x": "ं", "d": "्", "e": "ा", "f": "ि",
        "r": "ी", "g": "ु", "t": "ू", "=": "ृ",
        "@": "ॅ", "s": "े", "w": "ै", "\\": "ॉ",
        "a": "ो", "q": "ौ",
        "k": "क", "i": "ग", ";": "च", "p": "ज",
        "'": "ट", "[": "ड", "}": "ञ",
        "c": "म", "v": "न", "b": "व", "n": "ल",
        "m": "स", "/": "य", "j": "र", "<": "ष",
        "u": "ह", "o": "द", "h": "प", "y": "ब", "l": "त",

        # Shift keys
        "X": "ँ", "D": "अ", "E": "आ", "F": "इ",
        "R": "ई", "G": "उ", "T": "ऊ", "+": "ऋ",
        "!": "ऍ", "S": "ए", "W": "ऐ", "|": "ऑ",
        "A": "ओ", "Q": "औ",
        "K": "ख", "I": "घ", "U": "ङ", ":": "छ",
        "P": "झ", '"': "ठ", "{": "ढ", "C": "ण",
        "L": "थ", "O": "ध", "H": "फ", "Y": "भ",
        "J": "ऱ", "M": "श", ">": "।",

        # Hindi digits
        "0": "०", "1": "१", "2": "२", "3": "३", "4": "४",
        "5": "५", "6": "६", "7": "७", "8": "८", "9": "९",

        # Special InScript combinations
        "#": "्र", "$": "र्", "%": "ज्ञ",
        "^": "त्र", "&": "क्ष", "*": "श्र",
        "]": "़",
    }

    def inscript_character(self, event):
        key_text = event.text()

        if not key_text:
            return None

        if event.modifiers() & (
            Qt.ControlModifier |
            Qt.AltModifier |
            Qt.MetaModifier
        ):
            return None

        return self.INSCRIPT_MAP.get(key_text)

    def handle_inscript_key(self, event):
        if self.typing_box.isReadOnly():
            return False

        if event.key() in (
            Qt.Key_Backspace,
            Qt.Key_Delete,
            Qt.Key_Left,
            Qt.Key_Right,
            Qt.Key_Up,
            Qt.Key_Down,
            Qt.Key_Home,
            Qt.Key_End,
            Qt.Key_PageUp,
            Qt.Key_PageDown,
            Qt.Key_Return,
            Qt.Key_Enter,
            Qt.Key_Tab,
        ):
            return False

        mapped = self.inscript_character(event)

        if mapped is None:
            return False
        # Hindi-only input path. Do not write this page's geometry here:
        # it is owned by the shared QStackedWidget.
        cursor = self.typing_box.textCursor()
        cursor.insertText(mapped)
        self.typing_box.setTextCursor(cursor)
        return True

    def __init__(self):
        super().__init__()

        # This page lives inside DashboardWindow's shared QStackedWidget.
        # Ignore this page's large vertical sizeHint so typing/highlighting
        # cannot enlarge or displace the parent stack and all other pages.
        self.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Ignored
        )
        self.setMinimumHeight(0)

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

        # ==========================
        # Build UI
        # ==========================

        self.build_ui()

        # ==========================
        # Timer Signals
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

        self.update_paragraph_info()

    # =====================================================
    # Build UI
    # =====================================================

    def build_ui(self):

        # =================================================
        # IMAGE-MATCHED HINDI PAGE UI
        # UI ONLY — InScript mapping, timer, highlighter,
        # reports, exam mode and all business logic remain
        # in the existing methods below this function.
        # =================================================

        self.setObjectName("hindiPage")

        self.setStyleSheet("""
            QWidget#hindiPage {
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
                font-family: "Nirmala UI";
                font-size: 20pt;
                font-weight: 500;
            }

            QTextEdit#typingInput {
                background: #FFFFFF;
                color: #111827;
                border: none;
                padding: 13px 15px;
                font-family: "Nirmala UI";
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
        layout.setSizeConstraint(QLayout.SetNoConstraint)
        layout.setContentsMargins(22, 10, 22, 24)
        layout.setSpacing(7)

        # =================================================
        # PAGE HERO
        # =================================================

        page_hero = QFrame()
        page_hero.setObjectName("pageHero")
        # Compact hero so the typing test keeps enough vertical room even if
        # Qt recalculates the Hindi page after typing starts.
        page_hero.setFixedHeight(86)

        hero_layout = QHBoxLayout(page_hero)
        hero_layout.setContentsMargins(14, 10, 16, 10)
        hero_layout.setSpacing(13)

        self.back_btn = QPushButton("←  Back to Dashboard")
        self.back_btn.setObjectName("backButton")
        self.back_btn.setFixedWidth(155)

        title_box = QVBoxLayout()
        title_box.setSpacing(1)

        title = QLabel("Hindi Typing Test")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Practice Hindi typing with InScript keyboard support"
        )
        subtitle.setObjectName("pageSubtitle")

        title_box.addWidget(title)
        title_box.addWidget(subtitle)

        hero_layout.addWidget(self.back_btn)
        hero_layout.addLayout(title_box)
        hero_layout.addStretch()

        layout.addWidget(page_hero)

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
        passage_card.setFixedHeight(178)

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
            14, 5, 14, 5
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
        self.paragraph.setFixedHeight(134)

        self.paragraph.setFont(
            QFont(
                "Nirmala UI",
                20
            )
        )

        self.current_paragraph_text = (
            ParagraphLoader.get_paragraph(
                language="hindi",
                level="easy"
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
            passage_card
        )

        # =================================================
        # TYPING AREA — LARGE & READABLE
        # =================================================

        typing_card = QFrame()
        typing_card.setObjectName("typingCard")
        typing_card.setFixedHeight(178)

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
            14, 5, 14, 5
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

        self.typing_box.setFixedHeight(134)

        self.typing_box.setFont(
            QFont(
                "Nirmala UI",
                20
            )
        )

        self.typing_box.setPlaceholderText(
            "यहाँ टाइप करना शुरू करें..."
        )

        typing_layout.addWidget(
            typing_header
        )
        typing_layout.addWidget(
            self.typing_box
        )

        layout.addWidget(
            typing_card
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

        # Safety space: even if the parent view nudges the Hindi page after
        # typing starts, the action buttons remain comfortably above the edge.
        layout.addSpacing(22)

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
    # Timer
    # =====================================================

    def update_time(self, seconds):

        minutes = seconds // 60
        secs = seconds % 60

        self.time_lbl.setText(
            f"Remaining Time : {minutes:02}:{secs:02}"
        )

    def time_over(self):

        self.timer.stop()

        self.stats.stop()

        self.typing_box.setReadOnly(
            True
        )

        self.time_lbl.setText(
            "Time Over"
        )

        elapsed_seconds = (
            self.selected_minutes * 60
        )

        self.result_engine.generate(
            correct_chars=self.engine.correct_chars,
            wrong_chars=self.engine.wrong_chars,
            elapsed_seconds=elapsed_seconds,
            backspace_count=self.backspace_count
        )

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
        language="Hindi",
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

        self.show_final_result(result)

    # =====================================================
    # Paragraph Completed
    # =====================================================

    def paragraph_completed(self):

        self.timer.stop()

        self.timer_started = False

        self.stats.stop()

        self.typing_box.setReadOnly(
            True
        )

        self.progress.setValue(
            100
        )

        elapsed_seconds = (
            self.selected_minutes * 60
            - self.timer.remaining_seconds
        )

        if elapsed_seconds <= 0:
            elapsed_seconds = 1

        self.result_engine.generate(
            correct_chars=self.engine.correct_chars,
            wrong_chars=self.engine.wrong_chars,
            elapsed_seconds=elapsed_seconds,
            backspace_count=self.backspace_count
        )

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
        language="Hindi",
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

        self.show_final_result(result)

    # =====================================================
    # Timer Buttons
    # =====================================================

    def connect_timer_buttons(self):

        for minute, button in self.time_buttons.items():

            button.toggled.connect(
                lambda checked, m=minute:
                self.change_time(m, checked)
            )

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

    # =====================================================
    # Typing
    # =====================================================

        self.highlight_text()

    def on_typing(self):

        text = self.typing_box.toPlainText()

        current_length = len(text)

        if current_length < self.previous_text_length:

            self.backspace_count += (
                self.previous_text_length
                - current_length
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
        # Original
        # ==========================

        original = self.current_paragraph_text

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
            f"WPM : {self.stats.wpm()}"
        )

        self.acc_lbl.setText(
            f"Accuracy : {self.stats.accuracy()}%"
        )

        self.mistake_lbl.setText(
            f"Mistakes : {self.stats.mistakes()}"
        )

        # ==========================
        # Highlight
        # ==========================

        self.highlight_text()
       
        # Keep the currently typed/highlighted position visible in the
        # read-only practice passage. This only moves the passage viewport;
        # it does not change typing/highlight calculations.
        # Do not move any cursor/viewport here; it can trigger parent geometry/focus scrolling.

        # ==========================
        # Progress
        # ==========================

        original_length = len(original)

        typed_length = len(text)

        if original_length > 0:

            progress = int(
                (
                    typed_length
                    / original_length
                ) * 100
            )

            self.progress.setValue(
                min(progress, 100)
            )

        # ==========================
        # Complete
        # ==========================

        if (
            typed_length == original_length
            and text == original
        ):

            self.paragraph_completed()

    def _debug_min_sizes(self):
        window = self.window()

        print("\n========== HINDI CHILD SIZE DEBUG ==========")

        print(
            "WINDOW:",
            "minHint=",
            window.minimumSizeHint().width(),
            window.minimumSizeHint().height(),
            "min=",
            window.minimumWidth(),
            window.minimumHeight(),
            "size=",
            window.width(),
            window.height()
        )

        for child in self.findChildren(QWidget):

            hint = child.minimumSizeHint()

            if (
                hint.height() > 100
                or child.minimumHeight() > 100
                or hint.width() > 500
            ):
                print(
                    type(child).__name__,
                    "name=", child.objectName(),
                    "minHint=", hint.width(), hint.height(),
                    "min=", child.minimumWidth(), child.minimumHeight(),
                    "size=", child.width(), child.height()
                )

        print("============================================\n")

    # =====================================================
    # Restart
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

    # =====================================================
    # Next Paragraph
    # =====================================================

        self.highlight_text()

    def next_paragraph(self):

        self.restart_test()

        level = (
            self.category_combo
            .currentText()
            .lower()
        )

        self.paragraph.setPlainText(
            ParagraphLoader.get_paragraph(
                language="hindi",
                level=level
            )
        )

        self.update_paragraph_info()

        self.progress.setValue(
            0
        )

    # =====================================================
    # Category
    # =====================================================

    # =====================================================
    # Exam Selection
    # =====================================================

        self.highlight_text()

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

        if mode == "Practice Mode":

            self.category_combo.setEnabled(
                True
            )

            self.exam_combo.setEnabled(
                False
            )

        elif mode == "Exam Mode":

            self.category_combo.setEnabled(
                False
            )

            self.exam_combo.setEnabled(
                True
            )

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

        self.restart_test()

    def change_category(self):

        self.restart_test()

        level = (
            self.category_combo
            .currentText()
            .lower()
        )

        self.paragraph.setPlainText(
            ParagraphLoader.get_paragraph(
                language="hindi",
                level=level
            )
        )

        self.update_paragraph_info()

        self.progress.setValue(
            0
        )

    # =====================================================
    # Highlight
    # =====================================================

        self.highlight_text()

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
        # Intentionally disabled: the practice passage has its own scrollbar.
        # Moving its QTextCursor can make Qt reposition surrounding widgets.
        return

    # =====================================================
    # Paragraph Info
    # =====================================================

    def update_paragraph_info(self):

        current, total = (
            ParagraphLoader.paragraph_info()
        )

        self.paragraph_info_lbl.setText(
            f"Paragraph : {current} / {total}"
        )

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

                if self.handle_inscript_key(event):
                    return True

                if event.key() == Qt.Key_Backspace:
                    self.backspace_count += 1

        return super().eventFilter(
            obj,
            event
        )
