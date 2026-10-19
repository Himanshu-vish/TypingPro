from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QComboBox,
    QFileDialog,
    QMessageBox
)

from PySide6.QtGui import (
    QFont
)

from PySide6.QtCore import (
    Qt,
    QDateTime
)

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from app.core.exam_analyzer import ExamAnalyzer


class ResultDialog(QDialog):

    def __init__(
    self,
    result_data,
    parent=None,
    selected_exam=None
    ):

        super().__init__(parent)

        self.result = result_data
        self.exam_analyzer = ExamAnalyzer()

        # Last exam analysis
        self.exam_result = None
        self.selected_exam = selected_exam
        self.readiness_value = 0
        self.qualification_message = ""

        self.setWindowTitle(
            "Typing Test Result"
        )

        self.setMinimumSize(
            700,
            650
        )

        self.resize(
            760,
            700
        )

        self.build_ui()

    # =====================================
    # Build UI
    # =====================================

    def build_ui(self):

        self.main_layout = QVBoxLayout(self)

        self.main_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        self.main_layout.setSpacing(15)

        # =====================================
        # Title
        # =====================================

        self.title = QLabel(
            "TYPING TEST RESULT"
        )

        self.title.setAlignment(
            Qt.AlignCenter
        )

        self.title.setFont(
            QFont(
                "Segoe UI",
                22,
                QFont.Bold
            )
        )

        self.main_layout.addWidget(
            self.title
        )

        line = QFrame()

        line.setFrameShape(
            QFrame.HLine
        )

        self.main_layout.addWidget(
            line
        )

        # =====================================
        # Result Information
        # =====================================

        info_frame = QFrame()

        info_layout = QVBoxLayout(
            info_frame
        )

        info_layout.setSpacing(10)

        font_value = QFont(
            "Segoe UI",
            11
        )

        self.gross_lbl = QLabel(
            f"Gross WPM : "
            f"{self.result.get('gross_wpm', 0)}"
        )

        self.gross_lbl.setFont(
            font_value
        )

        info_layout.addWidget(
            self.gross_lbl
        )

        self.net_lbl = QLabel(
            f"Net WPM : "
            f"{self.result.get('net_wpm', 0)}"
        )

        self.net_lbl.setFont(
            font_value
        )

        info_layout.addWidget(
            self.net_lbl
        )

        self.acc_lbl = QLabel(
            f"Accuracy : "
            f"{self.result.get('accuracy', 0)}%"
        )

        self.acc_lbl.setFont(
            font_value
        )

        info_layout.addWidget(
            self.acc_lbl
        )

        self.correct_lbl = QLabel(
            f"Correct Characters : "
            f"{self.result.get('correct_chars', 0)}"
        )

        self.correct_lbl.setFont(
            font_value
        )

        info_layout.addWidget(
            self.correct_lbl
        )

        self.wrong_lbl = QLabel(
            f"Wrong Characters : "
            f"{self.result.get('wrong_chars', 0)}"
        )

        self.wrong_lbl.setFont(
            font_value
        )

        info_layout.addWidget(
            self.wrong_lbl
        )

        self.backspace_lbl = QLabel(
            f"Backspace : "
            f"{self.result.get('backspace', 0)}"
        )

        self.backspace_lbl.setFont(
            font_value
        )

        info_layout.addWidget(
            self.backspace_lbl
        )

        self.key_lbl = QLabel(
            f"Total Keystrokes : "
            f"{self.result.get('total_keystrokes', 0)}"
        )

        self.key_lbl.setFont(
            font_value
        )

        info_layout.addWidget(
            self.key_lbl
        )

        self.main_layout.addWidget(
            info_frame
        )

        # =====================================
        # Exam Selection
        # =====================================

        exam_frame = QFrame()

        exam_layout = QHBoxLayout(
            exam_frame
        )

        exam_title = QLabel(
            "Select Exam"
        )

        exam_title.setFont(
            QFont(
                "Segoe UI",
                11,
                QFont.Bold
            )
        )

        self.exam_combo = QComboBox()

        self.exam_combo.setMinimumHeight(
            36
        )

        self.exam_combo.setFont(
            QFont(
                "Segoe UI",
                10
            )
        )

        self.exam_combo.addItems(
            self.exam_analyzer.exam_names()
        )

        if self.selected_exam:

            index = self.exam_combo.findText(
                self.selected_exam
            )

            if index >= 0:

                self.exam_combo.setCurrentIndex(
                    index
                )

        exam_layout.addWidget(
            exam_title
        )

        exam_layout.addWidget(
            self.exam_combo
        )

        self.main_layout.addWidget(
            exam_frame
        )

        self.exam_combo.currentTextChanged.connect(
        self.change_exam
        )

        # =====================================
        # Grade & Status
        # =====================================

        status_frame = QFrame()

        status_layout = QVBoxLayout(
            status_frame
        )

        status_layout.setSpacing(
            10
        )

        grade = self.exam_analyzer.grade(
            self.result.get(
                "accuracy",
                0
            )
        )

        self.grade_lbl = QLabel(
            f"Grade : {grade}"
        )

        self.grade_lbl.setFont(
            QFont(
                "Segoe UI",
                13,
                QFont.Bold
            )
        )

        status_layout.addWidget(
            self.grade_lbl
        )

        self.status_lbl = QLabel(
            "Status : Ready for Exam Analysis"
        )

        self.status_lbl.setWordWrap(
            True
        )

        self.status_lbl.setFont(
            QFont(
                "Segoe UI",
                12,
                QFont.Bold
            )
        )

        status_layout.addWidget(
            self.status_lbl
        )

        self.main_layout.addWidget(
            status_frame
        )

        # =====================================
        # Buttons
        # =====================================

        button_layout = QHBoxLayout()

        self.analyze_btn = QPushButton(
            "Analyze for Exam"
        )

        self.restart_btn = QPushButton(
            "Restart Test"
        )

        self.pdf_btn = QPushButton(
            "Save PDF"
        )

        self.close_btn = QPushButton(
            "Close"
        )

        for btn in (
            self.analyze_btn,
            self.restart_btn,
            self.pdf_btn,
            self.close_btn
        ):

            btn.setMinimumHeight(
                42
            )

            btn.setFont(
                QFont(
                    "Segoe UI",
                    10,
                    QFont.Bold
                )
            )

            button_layout.addWidget(
                btn
            )

        self.main_layout.addLayout(
            button_layout
        )

        self.connect_buttons()

        # =====================================================
    # Exam Selection
    # =====================================================

    def change_exam(self, exam_name):

        self.selected_exam = exam_name

        # Previous analysis clear
        self.exam_result = None
        self.readiness_value = 0
        self.qualification_message = ""

        self.status_lbl.setText(
            f"Selected Exam : {exam_name}\n"
            "Click 'Analyze for Exam' to check qualification."
        )

    # =====================================
    # Analyze Exam
    # =====================================

    def analyze_exam(self):

        exam = self.exam_combo.currentText()

        result = self.exam_analyzer.analyze(

            exam_name=exam,

            net_wpm=self.result[
                "net_wpm"
            ],

            accuracy=self.result[
                "accuracy"
            ]

        )

        readiness = self.exam_analyzer.readiness(

            exam,

            self.result[
                "net_wpm"
            ],

            self.result[
                "accuracy"
            ]

        )

        # Save analysis for PDF

        self.exam_result = result

        self.selected_exam = exam

        self.readiness_value = readiness

        # =====================================
        # Qualified
        # =====================================

        if result["qualified"]:

            message = (
                "🎉 Congratulations!\n\n"
                f"You are Qualified for {exam}.\n\n"
                "Your hard work is paying off! "
                "Keep practicing and aim even higher. "
                "You are getting closer to your goal! 💪🏆"
            )

            self.qualification_message = message

            self.status_lbl.setText(

                f"✅ QUALIFIED — {exam}\n"
                f"Readiness : {readiness}%\n\n"
                f"{message}"

            )

        # =====================================
        # Not Qualified
        # =====================================

        else:

            if (
                result["need_wpm"] > 0
                and result["need_accuracy"] > 0
            ):

                message = (
                    "💪 Not Qualified Yet.\n\n"
                    "Don't give up! Improve your speed "
                    "and accuracy step by step.\n"
                    "Every practice session makes you better! 🔥"
                )

            elif result["need_wpm"] > 0:

                message = (
                    "💪 Not Qualified Yet.\n\n"
                    "Your accuracy is good, but your "
                    "typing speed needs improvement.\n"
                    "Keep practicing—you are getting "
                    "closer! 🚀"
                )

            else:

                message = (
                    "💪 Not Qualified Yet.\n\n"
                    "Your speed is good, but improve "
                    "your typing accuracy.\n"
                    "Accuracy first, speed will follow! 🎯"
                )

            self.qualification_message = message

            # Accuracy display

            if result["required_accuracy"] == 0:

                accuracy_text = (
                    "Accuracy Requirement : "
                    "Not specified"
                )

            else:

                accuracy_text = (
                    f"Need Accuracy : "
                    f"{result['need_accuracy']}%"
                )

            self.status_lbl.setText(

                f"❌ NOT QUALIFIED — {exam}\n"
                f"Need WPM : "
                f"{result['need_wpm']}\n"
                f"{accuracy_text}\n\n"
                f"{message}"

            )

    # =====================================
    # Restart Test
    # =====================================

    def restart_test(self):

        self.accept()

    # =====================================
    # Save PDF
    # =====================================

    def save_pdf(self):

        # =====================================
        # Ask User To Analyze Exam First
        # =====================================

        if self.exam_result is None:

            QMessageBox.information(

                self,

                "Exam Analysis Required",

                "Please select an exam and click "
                "\"Analyze for Exam\" before saving "
                "the PDF report."

            )

            return

        # =====================================
        # File Name
        # =====================================

        current_time = QDateTime.currentDateTime()

        timestamp = current_time.toString(
            "yyyy-MM-dd_HH-mm-ss"
        )

        default_name = (
            f"TypingPro_Result_{timestamp}.pdf"
        )

        file_path, _ = QFileDialog.getSaveFileName(

            self,

            "Save Typing Result PDF",

            default_name,

            "PDF Files (*.pdf)"

        )

        if not file_path:

            return

        try:

            self.create_pdf(
                file_path
            )

            QMessageBox.information(

                self,

                "PDF Saved",

                "Typing test result PDF "
                "has been saved successfully."

            )

        except Exception as error:

            QMessageBox.critical(

                self,

                "PDF Error",

                f"Unable to create PDF.\n\n"
                f"{error}"

            )

    # =====================================
    # Create PDF
    # =====================================

    def create_pdf(
        self,
        file_path
    ):

        doc = SimpleDocTemplate(

            file_path,

            pagesize=A4,

            rightMargin=40,

            leftMargin=40,

            topMargin=40,

            bottomMargin=40

        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(

            "ReportTitle",

            parent=styles["Title"],

            fontName="Helvetica-Bold",

            fontSize=20,

            alignment=TA_CENTER,

            spaceAfter=15

        )

        heading_style = ParagraphStyle(

            "Heading",

            parent=styles["Heading2"],

            fontName="Helvetica-Bold",

            fontSize=13,

            spaceBefore=10,

            spaceAfter=8

        )

        normal_style = ParagraphStyle(

            "NormalText",

            parent=styles["Normal"],

            fontSize=10,

            leading=14

        )

        story = []

        # =====================================
        # Header
        # =====================================

        story.append(
            Paragraph(
                "TYPINGPRO",
                title_style
            )
        )

        story.append(
            Paragraph(
                "English Typing Test Result Report",
                ParagraphStyle(
                    "SubTitle",
                    parent=normal_style,
                    alignment=TA_CENTER,
                    fontSize=12
                )
            )
        )

        story.append(
            Spacer(
                1,
                15
            )
        )

        # =====================================
        # Date & Time
        # =====================================

        report_time = QDateTime.currentDateTime().toString(
            "dd-MM-yyyy hh:mm:ss AP"
        )

        story.append(
            Paragraph(
                f"<b>Date & Time:</b> "
                f"{report_time}",
                normal_style
            )
        )

        story.append(
            Spacer(
                1,
                10
            )
        )

        # =====================================
        # Typing Result
        # =====================================

        story.append(
            Paragraph(
                "Typing Performance",
                heading_style
            )
        )

        performance_data = [

            [
                "Metric",
                "Result"
            ],

            [
                "Gross WPM",
                str(
                    self.result.get(
                        "gross_wpm",
                        0
                    )
                )
            ],

            [
                "Net WPM",
                str(
                    self.result.get(
                        "net_wpm",
                        0
                    )
                )
            ],

            [
                "Accuracy",
                f"{self.result.get('accuracy', 0)}%"
            ],

            [
                "Correct Characters",
                str(
                    self.result.get(
                        "correct_chars",
                        0
                    )
                )
            ],

            [
                "Wrong Characters",
                str(
                    self.result.get(
                        "wrong_chars",
                        0
                    )
                )
            ],

            [
                "Backspace",
                str(
                    self.result.get(
                        "backspace",
                        0
                    )
                )
            ],

            [
                "Total Keystrokes",
                str(
                    self.result.get(
                        "total_keystrokes",
                        0
                    )
                )
            ],

            [
                "Grade",
                self.exam_analyzer.grade(
                    self.result.get(
                        "accuracy",
                        0
                    )
                )
            ]

        ]

        performance_table = Table(

            performance_data,

            colWidths=[
                260,
                180
            ]

        )

        performance_table.setStyle(

            TableStyle([

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(
                        "#2C3E50"
                    )
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),

                (
                    "FONTNAME",
                    (0, 1),
                    (-1, -1),
                    "Helvetica"
                ),

                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    10
                ),

                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )

            ])

        )

        story.append(
            performance_table
        )

        story.append(
            Spacer(
                1,
                15
            )
        )

        # =====================================
        # Exam Analysis
        # =====================================

        story.append(
            Paragraph(
                "Exam Qualification",
                heading_style
            )
        )

        exam = self.exam_result

        qualification_status = (
            "QUALIFIED"
            if exam["qualified"]
            else "NOT QUALIFIED"
        )

        exam_data = [

            [
                "Exam",
                self.selected_exam
            ],

            [
                "Required WPM",
                str(
                    exam["required_wpm"]
                )
            ],

            [
                "Your WPM",
                str(
                    exam["your_wpm"]
                )
            ],

            [
                "Required Accuracy",
                (
                    "Not specified"
                    if exam["required_accuracy"] == 0
                    else f"{exam['required_accuracy']}%"
                )
            ],

            [
                "Your Accuracy",
                f"{exam['your_accuracy']}%"
            ],

            [
                "Status",
                qualification_status
            ],

            [
                "Readiness",
                f"{self.readiness_value}%"
            ]

        ]

        exam_table = Table(

            exam_data,

            colWidths=[
                180,
                260
            ]

        )

        exam_table.setStyle(

            TableStyle([

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold"
                ),

                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )

            ])

        )

        story.append(
            exam_table
        )

        story.append(
            Spacer(
                1,
                15
            )
        )

        # =====================================
        # Motivation
        # =====================================

        story.append(
            Paragraph(
                "Message",
                heading_style
            )
        )

        safe_message = (
            self.qualification_message
            .replace(
                "🎉",
                ""
            )
            .replace(
                "💪",
                ""
            )
            .replace(
                "🏆",
                ""
            )
            .replace(
                "🔥",
                ""
            )
            .replace(
                "🚀",
                ""
            )
            .replace(
                "🎯",
                ""
            )
        )

        safe_message = safe_message.replace(
            "\n",
            "<br/>"
        )

        story.append(
            Paragraph(
                safe_message,
                normal_style
            )
        )

        story.append(
            Spacer(
                1,
                25
            )
        )

        # =====================================
        # Footer
        # =====================================

        story.append(
            Paragraph(
                "Generated by TypingPro "
                "— English Typing Practice Software",
                ParagraphStyle(
                    "Footer",
                    parent=normal_style,
                    alignment=TA_CENTER,
                    fontSize=9
                )
            )
        )

        doc.build(
            story
        )

    # =====================================
    # Connect Buttons
    # =====================================

    def connect_buttons(self):

        self.close_btn.clicked.connect(
            self.close
        )

        self.restart_btn.clicked.connect(
            self.restart_test
        )

        self.pdf_btn.clicked.connect(
            self.save_pdf
        )

        self.analyze_btn.clicked.connect(
            self.analyze_exam
        )