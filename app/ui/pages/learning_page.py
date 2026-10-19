import time

from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QProgressBar, QPlainTextEdit, QFrame, QGridLayout, QSizePolicy, QMessageBox
)

from app.core.learning_manager import LearningManager
from app.core.session_manager import SessionManager


class LearningPage(QWidget):

    # =====================================================
    # HINDI INSCRIPT KEYBOARD
    # Same mapping used by the main Hindi Typing page.
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
        """
        Resolve Hindi InScript from the physical key state.

        Alphabet keys use the Shift modifier explicitly:
            c          -> म
            Shift + c  -> ण

        This avoids Windows/Qt/Caps Lock capitalization inconsistencies.
        """

        if event.modifiers() & (
            Qt.ControlModifier |
            Qt.AltModifier |
            Qt.MetaModifier
        ):
            return None

        key_text = event.text()

        if not key_text:
            return None

        shift_pressed = bool(
            event.modifiers()
            & Qt.ShiftModifier
        )

        if key_text.isalpha():

            physical = key_text.lower()

            if shift_pressed:
                physical = physical.upper()

            return self.INSCRIPT_MAP.get(
                physical
            )

        # For number/punctuation keys Qt gives the shifted symbol
        # directly, e.g. 1 / ! and [ / {.
        return self.INSCRIPT_MAP.get(
            key_text
        )

    def eventFilter(self, obj, event):
        if (
            obj == self.typing_box
            and event.type() == QEvent.KeyPress
            and self.language_key() == "Hindi"
        ):
            # Keep editing/navigation keys working normally.
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
                Qt.Key_Space,
            ):
                return super().eventFilter(obj, event)

            mapped = self.inscript_character(event)

            if mapped is not None:
                self.typing_box.insertPlainText(mapped)
                return True

        return super().eventFilter(obj, event)

    ENGLISH_LESSONS = [
        ("EN-01", "Finger Placement", "f j f j ff jj fj jf"),
        ("EN-02", "Home Row - F J", "f j f j fj jf ff jj"),
        ("EN-03", "Home Row - D K", "d k d k dk kd fd jk"),
        ("EN-04", "Home Row - S L", "s l s l sl ls as kl"),
        ("EN-05", "Home Row - A ;", "a ; a ; asdf jkl;"),
        ("EN-06", "Home Row Practice", "asdf jkl; sad fall ask flask"),
        ("EN-07", "Upper Row - E I", "e i e i ei ie die kid"),
        ("EN-08", "Upper Row - R U", "r u r u ru ur fur rude"),
        ("EN-09", "Upper Row - W O", "w o w o wo ow low row"),
        ("EN-10", "Upper Row - Q P", "q p q p qp pq pop quit"),
        ("EN-11", "Upper Row - T Y", "t y t y ty yt try yet"),
        ("EN-12", "Upper Row Practice", "qwerty uiop type write quiet power"),
        ("EN-13", "Lower Row - C ,", "c , c , cc ,, can come"),
        ("EN-14", "Lower Row - V M", "v m v m vm mv move vim"),
        ("EN-15", "Lower Row - X .", "x . x . xx .. extra text"),
        ("EN-16", "Lower Row - Z /", "z / z / zz // zoom zone"),
        ("EN-17", "Lower Row - B N", "b n b n bn nb ban bend"),
        ("EN-18", "Lower Row Practice", "zxcvbnm quick brown fox"),
        ("EN-19", "Capital Letters", "Typing Practice Makes Progress"),
        ("EN-20", "Numbers", "1 2 3 4 5 6 7 8 9 0"),
        ("EN-21", "Symbols", "! @ # $ % ^ & * ( )"),
        ("EN-22", "Easy Words", "computer keyboard typing speed accuracy"),
        ("EN-23", "Word Drill", "practice learning skill focus progress"),
        ("EN-24", "Sentence Drill", "Practice every day to improve typing speed."),
        ("EN-25", "Final English Lesson", "Accuracy first, speed follows with regular practice."),
    ]

    HINDI_LESSONS = [
        ("HI-01", "InScript परिचय", "क क क क र र र र"),
        ("HI-02", "स्वर अभ्यास", "अ आ इ ई उ ऊ ऋ ए ऐ ओ औ"),
        ("HI-03", "व्यंजन - 1", "क ख ग घ ङ च छ ज झ ञ"),
        ("HI-04", "व्यंजन - 2", "ट ठ ड ढ ण त थ द ध न"),
        ("HI-05", "व्यंजन - 3", "प फ ब भ म य र ल व"),
        ("HI-06", "व्यंजन - 4", "श ष स ह क्ष त्र ज्ञ श्र"),
        ("HI-07", "मात्राएँ - 1", "का कि की कु कू कृ"),
        ("HI-08", "मात्राएँ - 2", "के कै को कौ कं कँ"),
        ("HI-09", "Shift Keys", "ख घ ङ छ झ ठ ढ ण थ ध फ भ"),
        ("HI-10", "संयुक्त अक्षर", "क्ष त्र ज्ञ श्र"),
        ("HI-11", "सरल शब्द", "कमल कलम घर जल फल"),
        ("HI-12", "शब्द अभ्यास", "भारत भाषा कंप्यूटर अभ्यास"),
        ("HI-13", "मात्रा शब्द", "किताब परीक्षा सीखना टाइपिंग"),
        ("HI-14", "संयुक्त शब्द", "क्षमता ज्ञान प्रशिक्षण श्रम"),
        ("HI-15", "संख्या", "० १ २ ३ ४ ५ ६ ७ ८ ९"),
        ("HI-16", "वाक्य अभ्यास - 1", "नियमित अभ्यास से गति बढ़ती है।"),
        ("HI-17", "वाक्य अभ्यास - 2", "सही टाइपिंग के लिए शुद्धता जरूरी है।"),
        ("HI-18", "परीक्षा अभ्यास", "समय के साथ गति और शुद्धता दोनों बढ़ाइए।"),
        ("HI-19", "लंबा अभ्यास", "प्रतिदिन अभ्यास करने से टाइपिंग कौशल बेहतर होता है।"),
        ("HI-20", "Final Hindi Lesson", "पहले शुद्धता पर ध्यान दें और फिर धीरे धीरे गति बढ़ाएँ।"),
    ]

    # =====================================================
    # ON-SCREEN KEYBOARD + FINGER GUIDE
    # =====================================================

    KEYBOARD_ROWS = [
        ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "="],
        ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\"],
        ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'"],
        ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"],
    ]

    FINGER_MAP = {
        "1": "Left Little", "q": "Left Little", "a": "Left Little", "z": "Left Little",
        "2": "Left Ring", "w": "Left Ring", "s": "Left Ring", "x": "Left Ring",
        "3": "Left Middle", "e": "Left Middle", "d": "Left Middle", "c": "Left Middle",
        "4": "Left Index", "5": "Left Index", "r": "Left Index", "t": "Left Index",
        "f": "Left Index", "g": "Left Index", "v": "Left Index", "b": "Left Index",
        "6": "Right Index", "7": "Right Index", "y": "Right Index", "u": "Right Index",
        "h": "Right Index", "j": "Right Index", "n": "Right Index", "m": "Right Index",
        "8": "Right Middle", "i": "Right Middle", "k": "Right Middle", ",": "Right Middle",
        "9": "Right Ring", "o": "Right Ring", "l": "Right Ring", ".": "Right Ring",
        "0": "Right Little", "p": "Right Little", ";": "Right Little", "/": "Right Little",
        " ": "Thumb",
        "shift_left": "Left Little",
        "shift_right": "Right Little",
    }

    def physical_key_for_target(self, target_char):
        if target_char == " ":
            return " "

        if self.language_key() == "English":
            # Preserve uppercase target so the guide knows Shift is required.
            return target_char

        # Reverse lookup: Hindi output -> physical InScript key.
        # Prefer exact mapping, including Shift characters.
        for physical, output in self.INSCRIPT_MAP.items():
            if output == target_char:
                return physical

        return None

    def next_target_character(self):
        """
        Return the next target unit.

        Hindi special InScript outputs such as क्ष, त्र, ज्ञ, श्र,
        ्र and र् contain multiple Unicode code points.  The guide
        therefore chooses the longest mapped output that matches the
        remaining lesson text.
        """

        typed = self.typing_box.toPlainText()
        index = len(typed)

        if index >= len(
            self.current_target
        ):
            return None

        if self.language_key() == "Hindi":

            remaining = (
                self.current_target[
                    index:
                ]
            )

            mapped_outputs = sorted(
                set(
                    self.INSCRIPT_MAP.values()
                ),
                key=len,
                reverse=True
            )

            for output in mapped_outputs:

                if (
                    len(output) > 1
                    and remaining.startswith(
                        output
                    )
                ):
                    return output

        return self.current_target[
            index
        ]

    def update_keyboard_labels(self):
        """
        Change visible keyboard labels according to language/lesson.
        English normal lessons show lowercase keys.
        English capital targets temporarily show uppercase letter labels.
        Hindi lessons show physical key + InScript output where available.
        """
        language = self.language_key()
        target_char = self.next_target_character()

        for physical, button in self.keyboard_buttons.items():
            label = physical

            if language == "Hindi":
                normal_output = self.INSCRIPT_MAP.get(physical)
                if normal_output:
                    label = f"{normal_output}\n{physical.upper()}"
                else:
                    label = physical

                # If current Hindi target requires Shift, show the shifted
                # Hindi output on that physical key for easier learning.
                target_physical = self.physical_key_for_target(
                    target_char
                ) if target_char else None

                if (
                    target_physical
                    and target_physical != physical
                    and target_physical.lower() == physical
                ):
                    label = f"{target_char}\n{physical.upper()}"

            else:
                # English keyboard normally stays lowercase.
                label = physical

                # For a capital target, show that target key as capital.
                if (
                    target_char
                    and target_char.isalpha()
                    and target_char.isupper()
                    and physical == target_char.lower()
                ):
                    label = target_char

            button.setText(label)

    def update_keyboard_guide(self):
        target_char = self.next_target_character()
        self.update_keyboard_labels()

        # Reset all keys
        for key, button in self.keyboard_buttons.items():
            button.setStyleSheet(self.normal_key_style)

        self.space_key.setStyleSheet(self.normal_key_style)
        self.left_shift_key.setStyleSheet(self.normal_key_style)
        self.right_shift_key.setStyleSheet(self.normal_key_style)

        if target_char is None:
            self.finger_guide.setText("Lesson complete ✓")
            return

        physical = self.physical_key_for_target(target_char)

        if physical is None:
            self.finger_guide.setText(
                f"Target: {target_char}  •  Continue with the InScript key used for this character."
            )
            return

        SHIFTED_KEYS = {
            "~": "`", "!": "1", "@": "2", "#": "3", "$": "4",
            "%": "5", "^": "6", "&": "7", "*": "8", "(": "9",
            ")": "0", "_": "-", "+": "=", "{": "[", "}": "]",
            "|": "\\", ":": ";", '"': "'", "<": ",", ">": ".",
            "?": "/",
        }

        if physical.isalpha() and physical.isupper():
            is_shift = True
            lookup = physical.lower()
        elif physical in SHIFTED_KEYS:
            is_shift = True
            lookup = SHIFTED_KEYS[physical]
        else:
            is_shift = False
            lookup = physical

        finger = self.FINGER_MAP.get(lookup, "Correct finger")

        if physical == " ":
            self.space_key.setStyleSheet(self.target_key_style)
            key_name = "SPACE"
            shift_name = ""
        else:
            button = self.keyboard_buttons.get(lookup)
            if button:
                button.setStyleSheet(self.target_key_style)

            key_name = physical.upper() if physical.isalpha() else physical
            shift_name = ""

            if is_shift:
                # Standard touch-typing rule:
                # press Shift with the opposite hand from the target key.
                left_hand_fingers = {
                    "Left Little", "Left Ring", "Left Middle", "Left Index"
                }

                if finger in left_hand_fingers:
                    self.right_shift_key.setStyleSheet(self.target_key_style)
                    shift_name = "Right Shift"
                else:
                    self.left_shift_key.setStyleSheet(self.target_key_style)
                    shift_name = "Left Shift"

        if is_shift:
            self.finger_guide.setText(
                f"Next: {target_char}   •   {shift_name} + {key_name}"
                f"   •   Key Finger: {finger}"
            )
        else:
            self.finger_guide.setText(
                f"Next: {target_char}   •   Key: {key_name}"
                f"   •   Finger: {finger}"
            )

    def __init__(self):
        super().__init__()
        self.manager = LearningManager()
        self.started_at = None
        self.current_target = ""
        self.build_ui()
        self.load_lessons()

    def build_ui(self):
        # Premium UI only. Existing lesson, InScript, keyboard,
        # progress and result logic below remains unchanged.
        self.setObjectName("learningPage")
        self.setStyleSheet("""
            QWidget#learningPage {
                background:#F4F7FB;
                font-family:"Segoe UI";
                color:#122B49;
            }

            QFrame#heroPanel,
            QFrame#card {
                background:#FFFFFF;
                border:1px solid #D9E3EE;
                border-radius:14px;
            }

            QLabel#heroIcon {
                background:#E8F1FF;
                color:#1769D5;
                border-radius:25px;
                font-size:24px;
                font-weight:800;
            }
            QLabel#pageTitle {
                font-size:27px;
                font-weight:850;
                color:#102A49;
            }
            QLabel#muted {
                font-size:13px;
                font-weight:650;
                color:#536980;
            }
            QLabel#sectionTitle {
                font-size:17px;
                font-weight:800;
                color:#17324F;
            }
            QLabel#lessonTitle {
                font-size:20px;
                font-weight:850;
                color:#1266D8;
            }
            QLabel#guide {
                font-size:13.5px;
                font-weight:650;
                color:#4F647A;
            }
            QLabel#target {
                background:#F6F9FD;
                border:1px solid #DCE5EF;
                border-radius:9px;
                padding:12px 15px;
                font-size:18px;
                font-weight:750;
                color:#172B45;
            }
            QLabel#statCaption {
                font-size:12px;
                font-weight:750;
                color:#5A6F84;
            }
            QLabel#statValue,
            QLabel#metricValue {
                font-size:18px;
                font-weight:850;
                color:#132D4D;
            }

            QComboBox {
                background:#FBFDFF;
                color:#18324E;
                border:1.5px solid #B9C9DA;
                border-radius:10px;
                min-height:46px;
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

            QPushButton#backButton,
            QPushButton#secondaryButton {
                background:#FFFFFF;
                color:#1764C5;
                border:1px solid #BFD0E4;
                border-radius:9px;
                min-height:38px;
                padding:6px 16px;
                font-size:13px;
                font-weight:800;
            }
            QPushButton#backButton:hover,
            QPushButton#secondaryButton:hover {
                background:#F2F7FD;
                border-color:#7DA8D7;
            }

            QPushButton#nextButton {
                background:#116BE5;
                color:white;
                border:1px solid #116BE5;
                border-radius:9px;
                min-height:38px;
                padding:6px 20px;
                font-size:13px;
                font-weight:800;
            }
            QPushButton#nextButton:hover {background:#095FCC;}
            QPushButton#nextButton:disabled {
                background:#EDF1F6;
                color:#A7B2C0;
                border-color:#DCE3EB;
            }

            QProgressBar {
                background:#E5EBF2;
                border:none;
                border-radius:5px;
                min-height:10px;
                max-height:10px;
                color:transparent;
            }
            QProgressBar::chunk {
                background:#176FE3;
                border-radius:5px;
            }

            QPlainTextEdit#typingBox {
                background:#FFFFFF;
                border:1.5px solid #5C9CF3;
                border-radius:10px;
                padding:12px 14px;
                font-size:18px;
                color:#172B45;
            }
            QPlainTextEdit#typingBox:focus {
                border:2px solid #1670E8;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 8, 18, 8)
        layout.setSpacing(6)

        # -------------------------------------------------
        # HERO HEADER
        # -------------------------------------------------
        hero = QFrame()
        hero.setObjectName("heroPanel")
        hero_layout = QHBoxLayout(hero)
        hero_layout.setContentsMargins(14, 6, 16, 6)
        hero_layout.setSpacing(13)

        self.back_btn = QPushButton("←  Back to Dashboard")
        self.back_btn.setObjectName("backButton")
        self.back_btn.setFixedWidth(185)
        hero_layout.addWidget(self.back_btn)

        hero_icon = QLabel("🎓")
        hero_icon.setObjectName("heroIcon")
        hero_icon.setFixedSize(36, 36)
        hero_icon.setAlignment(Qt.AlignCenter)
        hero_layout.addWidget(hero_icon)

        title_box = QVBoxLayout()
        title_box.setSpacing(0)

        title = QLabel("Learn Typing")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Guided English & Hindi lessons with live keyboard and finger training")
        subtitle.setObjectName("muted")

        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        hero_layout.addLayout(title_box, 1)
        layout.addWidget(hero)

        # -------------------------------------------------
        # COURSE CONTROLS + SUMMARY
        # -------------------------------------------------
        course_card = QFrame()
        course_card.setObjectName("card")
        course = QGridLayout(course_card)
        course.setContentsMargins(13, 8, 13, 8)
        course.setHorizontalSpacing(12)
        course.setVerticalSpacing(5)

        lang_label = QLabel("Language")
        lang_label.setObjectName("sectionTitle")
        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "Hindi InScript"])
        self.language_combo.setMinimumWidth(180)

        lesson_label = QLabel("Lesson")
        lesson_label.setObjectName("sectionTitle")
        self.lesson_combo = QComboBox()
        self.lesson_combo.setMinimumWidth(330)

        course.addWidget(lang_label, 0, 0)
        course.addWidget(self.language_combo, 0, 1)
        course.addWidget(lesson_label, 0, 2)
        course.addWidget(self.lesson_combo, 0, 3, 1, 2)

        def summary_card(icon_text, caption, value, bg, fg):
            card = QFrame()
            card.setObjectName("card")
            card.setMinimumHeight(64)

            row = QHBoxLayout(card)
            row.setContentsMargins(11, 9, 12, 9)
            row.setSpacing(9)

            icon = QLabel(icon_text)
            icon.setAlignment(Qt.AlignCenter)
            icon.setFixedSize(36, 36)
            icon.setStyleSheet(
                f"background:{bg};color:{fg};border:none;border-radius:10px;"
                "font-size:19px;font-weight:800;"
            )

            box = QVBoxLayout()
            box.setSpacing(0)

            val = QLabel(value)
            val.setObjectName("statValue")
            cap = QLabel(caption)
            cap.setObjectName("statCaption")

            box.addWidget(val)
            box.addWidget(cap)

            row.addWidget(icon)
            row.addLayout(box, 1)
            return card, val

        stars_card, self.ui_stars_value = summary_card(
            "★", "Stars", "0", "#FFF7DF", "#E6A700"
        )
        wpm_card, self.ui_best_wpm_value = summary_card(
            "◴", "Best WPM", "0.0", "#EEF5FF", "#176FE3"
        )
        acc_card, self.ui_best_accuracy_value = summary_card(
            "◎", "Best Accuracy", "0.0%", "#EAF9F0", "#15A35D"
        )

        course.addWidget(stars_card, 0, 5)
        course.addWidget(wpm_card, 0, 6)
        course.addWidget(acc_card, 0, 7)

        self.progress_label = QLabel("Course Progress")
        self.progress_label.setStyleSheet(
            "font-size:13px;font-weight:750;color:#40566F;border:none;"
        )
        self.progress_percent_ui = QLabel("0%")
        self.progress_percent_ui.setAlignment(Qt.AlignRight)
        self.progress_percent_ui.setStyleSheet(
            "font-size:13px;font-weight:800;color:#40566F;border:none;"
        )

        course.addWidget(self.progress_label, 1, 0, 1, 6)
        course.addWidget(self.progress_percent_ui, 1, 6, 1, 2)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        course.addWidget(self.progress, 2, 0, 1, 8)

        layout.addWidget(course_card)

        # -------------------------------------------------
        # LESSON TARGET CARD
        # -------------------------------------------------
        lesson_card = QFrame()
        lesson_card.setObjectName("card")
        lesson_layout = QVBoxLayout(lesson_card)
        lesson_layout.setContentsMargins(12, 6, 12, 7)
        lesson_layout.setSpacing(3)

        self.lesson_title = QLabel()
        self.lesson_title.setObjectName("lessonTitle")
        self.lesson_title.setAlignment(Qt.AlignCenter)

        self.guide = QLabel()
        self.guide.setObjectName("guide")
        self.guide.setAlignment(Qt.AlignCenter)
        self.guide.setWordWrap(True)

        self.target = QLabel()
        self.target.setObjectName("target")
        self.target.setWordWrap(True)
        self.target.setTextInteractionFlags(Qt.TextSelectableByMouse)

        lesson_layout.addWidget(self.lesson_title)
        lesson_layout.addWidget(self.guide)
        lesson_layout.addWidget(self.target)
        layout.addWidget(lesson_card)

        # -------------------------------------------------
        # KEYBOARD CARD
        # -------------------------------------------------
        keyboard_frame = QFrame()
        keyboard_frame.setObjectName("card")
        keyboard_layout = QVBoxLayout(keyboard_frame)
        keyboard_layout.setContentsMargins(12, 6, 12, 7)
        keyboard_layout.setSpacing(4)

        keyboard_title = QLabel("⌨  Keyboard & Finger Guide")
        keyboard_title.setObjectName("sectionTitle")
        keyboard_title.setAlignment(Qt.AlignCenter)
        keyboard_layout.addWidget(keyboard_title)

        self.finger_guide = QLabel("Start typing...")
        self.finger_guide.setAlignment(Qt.AlignCenter)
        self.finger_guide.setMinimumHeight(38)
        self.finger_guide.setWordWrap(True)
        self.finger_guide.setStyleSheet(
            "background:#F4F8FD;border:1px solid #DCE6F1;border-radius:8px;"
            "padding:7px 10px;font-size:14px;font-weight:800;color:#1265D3;"
        )
        keyboard_layout.addWidget(self.finger_guide)

        self.keyboard_buttons = {}
        self.normal_key_style = (
            "QPushButton{background:#FFFFFF;border:1px solid #BECBD8;"
            "border-radius:6px;padding:1px;font-size:14px;font-weight:800;color:#111827;}"
        )
        self.target_key_style = (
            "QPushButton{background:#FFC83D;border:2px solid #F0A800;"
            "border-radius:6px;padding:1px;font-size:14px;font-weight:850;color:#111827;}"
        )

        def key_button(text, width=58, height=39):
            b = QPushButton(text)
            b.setEnabled(False)
            b.setFixedSize(width, height)
            b.setStyleSheet(self.normal_key_style)
            return b

        number_layout = QHBoxLayout()
        number_layout.setSpacing(5)
        number_layout.addStretch()
        for key in self.KEYBOARD_ROWS[0]:
            button = key_button(key.upper())
            self.keyboard_buttons[key] = button
            number_layout.addWidget(button)
        backspace_key = key_button("BACKSPACE", 120, 39)
        number_layout.addWidget(backspace_key)
        number_layout.addStretch()
        keyboard_layout.addLayout(number_layout)

        qwerty_layout = QHBoxLayout()
        qwerty_layout.setSpacing(5)
        qwerty_layout.addStretch()
        tab_key = key_button("TAB", 88, 39)
        qwerty_layout.addWidget(tab_key)
        for key in self.KEYBOARD_ROWS[1]:
            button = key_button(key.upper())
            self.keyboard_buttons[key] = button
            qwerty_layout.addWidget(button)
        qwerty_layout.addStretch()
        keyboard_layout.addLayout(qwerty_layout)

        home_layout = QHBoxLayout()
        home_layout.setSpacing(5)
        home_layout.addStretch()
        caps_key = key_button("CAPS", 100, 39)
        home_layout.addWidget(caps_key)
        for key in self.KEYBOARD_ROWS[2]:
            button = key_button(key.upper())
            self.keyboard_buttons[key] = button
            home_layout.addWidget(button)
        enter_key = key_button("ENTER", 104, 39)
        home_layout.addWidget(enter_key)
        home_layout.addStretch()
        keyboard_layout.addLayout(home_layout)

        shift_layout = QHBoxLayout()
        shift_layout.setSpacing(5)
        shift_layout.addStretch()
        self.left_shift_key = key_button("SHIFT", 122, 39)
        shift_layout.addWidget(self.left_shift_key)
        for key in self.KEYBOARD_ROWS[3]:
            button = key_button(key.upper())
            self.keyboard_buttons[key] = button
            shift_layout.addWidget(button)
        self.right_shift_key = key_button("SHIFT", 122, 39)
        shift_layout.addWidget(self.right_shift_key)
        shift_layout.addStretch()
        keyboard_layout.addLayout(shift_layout)

        space_layout = QHBoxLayout()
        space_layout.addStretch()
        self.space_key = key_button("SPACE", 370, 36)
        space_layout.addWidget(self.space_key)
        space_layout.addStretch()
        keyboard_layout.addLayout(space_layout)

        layout.addWidget(keyboard_frame)

        # -------------------------------------------------
        # TYPING AREA
        # -------------------------------------------------
        typing_header = QHBoxLayout()

        typing_title = QLabel("✎  Type Here")
        typing_title.setObjectName("sectionTitle")
        typing_header.addWidget(typing_title)
        typing_header.addStretch()

        typing_status = QLabel("⏱  Start typing...")
        typing_status.setObjectName("muted")
        typing_header.addWidget(typing_status)

        layout.addLayout(typing_header)

        self.typing_box = QPlainTextEdit()
        self.typing_box.setObjectName("typingBox")
        self.typing_box.installEventFilter(self)
        self.typing_box.setMinimumHeight(82)
        self.typing_box.setMaximumHeight(95)
        self.typing_box.setFont(QFont("Segoe UI", 17))
        self.typing_box.setPlaceholderText("Start typing the lesson above...")
        layout.addWidget(self.typing_box)

        # -------------------------------------------------
        # METRICS
        # -------------------------------------------------
        metrics = QHBoxLayout()
        metrics.setSpacing(9)

        def metric_card(icon_text, label_text, value_label, bg, fg):
            frame = QFrame()
            frame.setObjectName("card")
            frame.setMinimumHeight(58)

            row = QHBoxLayout(frame)
            row.setContentsMargins(9, 5, 9, 5)
            row.setSpacing(6)

            icon = QLabel(icon_text)
            icon.setAlignment(Qt.AlignCenter)
            icon.setFixedSize(34, 34)
            icon.setStyleSheet(
                f"background:{bg};color:{fg};border:none;border-radius:9px;"
                "font-size:18px;font-weight:800;"
            )

            box = QVBoxLayout()
            box.setSpacing(0)

            cap = QLabel(label_text)
            cap.setObjectName("statCaption")
            value_label.setObjectName("metricValue")

            box.addWidget(cap)
            box.addWidget(value_label)

            row.addWidget(icon)
            row.addLayout(box, 1)
            return frame

        self.accuracy_lbl = QLabel("Accuracy: 100%")
        self.wpm_lbl = QLabel("WPM: 0")
        self.mistakes_lbl = QLabel("Mistakes: 0")
        self.status_lbl = QLabel("Start typing...")

        metrics.addWidget(metric_card("◎", "Accuracy", self.accuracy_lbl, "#EAF9F0", "#15A35D"), 1)
        metrics.addWidget(metric_card("◴", "WPM", self.wpm_lbl, "#EEF5FF", "#176FE3"), 1)
        metrics.addWidget(metric_card("×", "Mistakes", self.mistakes_lbl, "#FFF0F1", "#E23D4E"), 1)
        metrics.addWidget(metric_card("⌘", "Status", self.status_lbl, "#F6EEFF", "#7A35DE"), 1)

        layout.addLayout(metrics)

        # -------------------------------------------------
        # ACTIONS
        # -------------------------------------------------
        actions = QHBoxLayout()
        actions.setSpacing(9)

        self.restart_btn = QPushButton("↻  Restart Lesson")
        self.restart_btn.setObjectName("secondaryButton")
        self.restart_btn.setMinimumWidth(150)

        self.reset_progress_btn = QPushButton("↻  Reset Course Progress")
        self.reset_progress_btn.setObjectName("secondaryButton")
        self.reset_progress_btn.setMinimumWidth(190)

        self.next_btn = QPushButton("Next Lesson   →")
        self.next_btn.setObjectName("nextButton")
        self.next_btn.setMinimumWidth(150)
        self.next_btn.setEnabled(False)

        actions.addWidget(self.restart_btn)
        actions.addWidget(self.reset_progress_btn)
        actions.addStretch()
        actions.addWidget(self.next_btn)

        layout.addLayout(actions)

        # Existing connections
        self.language_combo.currentIndexChanged.connect(self.load_lessons)
        self.lesson_combo.currentIndexChanged.connect(self.load_selected_lesson)
        self.typing_box.textChanged.connect(self.check_typing)
        self.restart_btn.clicked.connect(self.restart_lesson)
        self.reset_progress_btn.clicked.connect(self.reset_course_progress)
        self.next_btn.clicked.connect(self.next_lesson)

        self.progress.valueChanged.connect(
            lambda value: self.progress_percent_ui.setText(f"{value}%")
        )

    def lessons(self):
        if self.language_combo.currentText() == "Hindi InScript":
            return self.HINDI_LESSONS
        return self.ENGLISH_LESSONS

    @staticmethod
    def expanded_practice_target(target, minimum_chars=320):
        """Repeat each lesson's own drill until it becomes a full practice block."""
        base = " ".join(str(target).split())
        if not base:
            return ""
        parts = []
        length = 0
        while length < minimum_chars:
            parts.append(base)
            length += len(base) + 1
        return " ".join(parts).strip()

    def language_key(self):
        return "Hindi" if self.language_combo.currentText() == "Hindi InScript" else "English"

    def load_lessons(self):
        self.lesson_combo.blockSignals(True)
        self.lesson_combo.clear()
        for lesson_id, title, _target in self.lessons():
            self.lesson_combo.addItem(f"{lesson_id} • {title}")
        self.lesson_combo.blockSignals(False)
        self.lesson_combo.setCurrentIndex(0)
        self.load_selected_lesson()
        self.refresh_progress()

    def load_selected_lesson(self):
        index = self.lesson_combo.currentIndex()
        lessons = self.lessons()
        if index < 0 or index >= len(lessons):
            return

        lesson_id, title, target = lessons[index]
        target = self.expanded_practice_target(target)
        self.current_target = target
        self.lesson_title.setText(f"{lesson_id} • {title}")

        if self.language_key() == "English":
            self.guide.setText(
                "Keep fingers relaxed. Focus on accuracy first; use the correct finger for each key."
            )
        else:
            self.guide.setText(
                "Hindi InScript अभ्यास: स्क्रीन पर दिए अक्षरों को उसी क्रम में टाइप करें।"
            )

        self.target.setText(target)
        self.restart_lesson()
        self.refresh_progress()

    def restart_lesson(self):
        self.typing_box.blockSignals(True)
        self.typing_box.clear()
        self.typing_box.blockSignals(False)
        self.started_at = None
        self.typing_box.setReadOnly(False)
        self.next_btn.setEnabled(False)
        self.accuracy_lbl.setText("Accuracy: 100%")
        self.wpm_lbl.setText("WPM: 0")
        self.mistakes_lbl.setText("Mistakes: 0")
        self.status_lbl.setText("Start typing...")
        self.typing_box.setFocus()
        self.update_keyboard_guide()

    def check_typing(self):
        typed = self.typing_box.toPlainText()
        self.update_keyboard_guide()

        if typed and self.started_at is None:
            self.started_at = time.monotonic()

        correct = 0
        wrong = 0

        for index, char in enumerate(typed):
            if index < len(self.current_target) and char == self.current_target[index]:
                correct += 1
            else:
                wrong += 1

        total = correct + wrong
        accuracy = (correct / total * 100) if total else 100.0

        elapsed = max((time.monotonic() - self.started_at), 0.01) if self.started_at else 0
        wpm = ((len(typed) / 5) / (elapsed / 60)) if elapsed else 0

        self.accuracy_lbl.setText(f"Accuracy: {accuracy:.1f}%")
        self.wpm_lbl.setText(f"WPM: {wpm:.1f}")
        self.mistakes_lbl.setText(f"Mistakes: {wrong}")

        if typed == self.current_target:
            self.complete_lesson(accuracy, wpm)
        elif len(typed) >= len(self.current_target):
            self.status_lbl.setText("Some characters are wrong. Correct them to finish.")
        else:
            self.status_lbl.setText("Practice in progress...")

    def complete_lesson(self, accuracy, wpm):
        stars = 3 if accuracy >= 98 else 2 if accuracy >= 95 else 1
        lesson_id = self.lessons()[self.lesson_combo.currentIndex()][0]

        self.manager.save_progress(
            self.language_key(),
            lesson_id,
            accuracy,
            wpm,
            stars,
            True
        )

        self.status_lbl.setText(
            f"Lesson Complete ✓   {'★' * stars}{'☆' * (3 - stars)}"
        )
        self.typing_box.setReadOnly(True)
        self.next_btn.setEnabled(True)
        self.refresh_progress()

    def refresh_progress(self):
        total = len(self.lessons())
        done = self.manager.completed_count(self.language_key())
        percent = int((done / total) * 100) if total else 0
        self.progress.setValue(percent)
        self.progress_label.setText(
            f"{self.language_combo.currentText()} Progress: {done}/{total} Lessons ({percent}%)"
        )

    def reset_course_progress(self):
        answer = QMessageBox.question(
            self,
            "Reset Course Progress",
            f"Reset all saved {self.language_combo.currentText()} progress for this profile?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if answer != QMessageBox.Yes:
            return

        self.manager.reset_language_progress(
            self.language_key()
        )

        self.lesson_combo.setCurrentIndex(0)
        self.restart_lesson()
        self.refresh_progress()

        QMessageBox.information(
            self,
            "TypingPro",
            "Course progress reset successfully."
        )

    def next_lesson(self):
        index = self.lesson_combo.currentIndex()
        if index + 1 < self.lesson_combo.count():
            self.lesson_combo.setCurrentIndex(index + 1)

    def refresh_profile(self):
        self.refresh_progress()
        self.load_selected_lesson()
