import csv
from datetime import datetime, timedelta

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QFrame,
    QPushButton,
    QMessageBox,
    QFileDialog
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor, QBrush

from app.core.report_manager import ReportManager
from app.core.exam_analyzer import ExamAnalyzer


class ReportsPage(QWidget):

    def __init__(self):
        super().__init__()

        self.report_manager = ReportManager()
        self.exam_analyzer = ExamAnalyzer()

        self.all_reports = []
        self.filtered_reports = []

        self.build_ui()
        self.load_reports()

    # =====================================================
    # Build UI
    # =====================================================

    def build_ui(self):

        self.setObjectName("reportsPage")
        self.setStyleSheet("""
            QWidget#reportsPage {
                background:#F4F7FB;
                font-family:"Segoe UI";
            }
            QFrame#heroPanel,
            QFrame#summaryCard,
            QFrame#filterCard,
            QFrame#tableCard {
                background:#FFFFFF;
                border:1px solid #D9E3EE;
                border-radius:14px;
            }
            QLabel#heroIcon {
                background:#E8F1FF;
                color:#1769D5;
                border-radius:26px;
                font-size:24px;
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
            QLabel#summaryCaption {
                color:#40566D;
                font-size:13px;
                font-weight:750;
            }
            QLabel#summaryValue {
                color:#102A49;
                font-size:28px;
                font-weight:850;
            }
            QLabel#summarySub {
                color:#60758B;
                font-size:12px;
                font-weight:650;
            }
            QLabel#filterTitle {
                color:#17324F;
                font-size:17px;
                font-weight:800;
            }
            QLabel#filterLabel {
                color:#31475E;
                font-size:13px;
                font-weight:750;
            }

            QComboBox {
                background:#FBFDFF;
                color:#18324E;
                border:1.5px solid #B9C9DA;
                border-radius:10px;
                min-height:48px;
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

            QTableWidget {
                background:#FFFFFF;
                alternate-background-color:#F8FBFF;
                border:none;
                gridline-color:#E2E8F0;
                color:#243B53;
                font-size:13.5px;
                font-weight:600;
                selection-background-color:#E7F1FF;
                selection-color:#102A49;
            }
            QHeaderView::section {
                background:#EEF4FB;
                color:#17324F;
                border:none;
                border-right:1px solid #DCE5EF;
                border-bottom:1px solid #D5DFEA;
                padding:12px 8px;
                font-size:13.5px;
                font-weight:800;
            }

            QPushButton#detailsButton,
            QPushButton#deleteButton,
            QPushButton#exportButton,
            QPushButton#refreshButton,
            QPushButton#clearButton {
                min-height:44px;
                border-radius:9px;
                padding:6px 15px;
                font-size:13px;
                font-weight:800;
            }
            QPushButton#detailsButton, QPushButton#refreshButton {
                background:#FFFFFF;color:#1765C7;border:1px solid #B7CCE2;
            }
            QPushButton#detailsButton:hover, QPushButton#refreshButton:hover {background:#F1F7FE;}
            QPushButton#deleteButton {
                background:#FFF5F5;color:#D83D4A;border:1px solid #F0C7CB;
            }
            QPushButton#deleteButton:hover {background:#FFECEC;}
            QPushButton#exportButton {
                background:#EEF9F2;color:#188B4E;border:1px solid #BFE3CD;
            }
            QPushButton#exportButton:hover {background:#E5F6EC;}
            QPushButton#clearButton {
                background:#FFF8EC;color:#D9780B;border:1px solid #EFD3A7;
            }
            QPushButton#clearButton:hover {background:#FFF1DD;}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 18, 26, 18)
        layout.setSpacing(13)

        # HERO
        hero = QFrame()
        hero.setObjectName("heroPanel")
        hero_l = QHBoxLayout(hero)
        hero_l.setContentsMargins(20, 14, 20, 14)
        hero_l.setSpacing(14)

        hero_icon = QLabel("▤")
        hero_icon.setObjectName("heroIcon")
        hero_icon.setFixedSize(52, 52)
        hero_icon.setAlignment(Qt.AlignCenter)

        hero_copy = QVBoxLayout()
        hero_copy.setSpacing(1)
        title = QLabel("Reports & Performance")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Review your typing history, progress, speed and accuracy")
        subtitle.setObjectName("pageSubtitle")
        hero_copy.addWidget(title)
        hero_copy.addWidget(subtitle)

        hero_l.addWidget(hero_icon)
        hero_l.addLayout(hero_copy, 1)
        layout.addWidget(hero)

        # SUMMARY
        summary_layout = QHBoxLayout()
        summary_layout.setSpacing(12)

        def make_summary_card(icon_text, caption, subtitle_text, bg, fg):
            card = QFrame()
            card.setObjectName("summaryCard")
            card.setMinimumHeight(116)

            row = QHBoxLayout(card)
            row.setContentsMargins(16, 14, 16, 14)
            row.setSpacing(13)

            icon = QLabel(icon_text)
            icon.setAlignment(Qt.AlignCenter)
            icon.setFixedSize(56, 56)
            icon.setStyleSheet(
                f"background:{bg};color:{fg};border-radius:14px;"
                "font-size:23px;font-weight:800;"
            )

            copy = QVBoxLayout()
            copy.setSpacing(1)
            caption_lbl = QLabel(caption)
            caption_lbl.setObjectName("summaryCaption")
            value_lbl = QLabel("0")
            value_lbl.setObjectName("summaryValue")
            sub_lbl = QLabel(subtitle_text)
            sub_lbl.setObjectName("summarySub")
            copy.addWidget(caption_lbl)
            copy.addWidget(value_lbl)
            copy.addWidget(sub_lbl)

            row.addWidget(icon)
            row.addLayout(copy, 1)
            summary_layout.addWidget(card, 1)
            return value_lbl

        self.total_test_lbl = make_summary_card("▤", "Total Tests", "Tests completed", "#E8F1FF", "#176FE3")
        self.best_wpm_lbl = make_summary_card("↗", "Best WPM", "Highest typing speed", "#E8F8EF", "#20AF65")
        self.avg_wpm_lbl = make_summary_card("◴", "Average WPM", "Overall average speed", "#F0E9FF", "#7B3FE4")
        self.avg_accuracy_lbl = make_summary_card("◎", "Average Accuracy", "Overall typing accuracy", "#FFF0DD", "#F08A16")
        layout.addLayout(summary_layout)

        # FILTERS
        filter_card = QFrame()
        filter_card.setObjectName("filterCard")
        fl = QVBoxLayout(filter_card)
        fl.setContentsMargins(16, 13, 16, 15)
        fl.setSpacing(10)

        filter_title = QLabel("Filter Reports")
        filter_title.setObjectName("filterTitle")
        fl.addWidget(filter_title)

        filter_row = QHBoxLayout()
        filter_row.setSpacing(12)

        def filter_block(label_text, combo):
            b = QVBoxLayout()
            b.setSpacing(5)
            lbl = QLabel(label_text)
            lbl.setObjectName("filterLabel")
            b.addWidget(lbl)
            b.addWidget(combo)
            return b

        self.language_combo = QComboBox()
        self.language_combo.addItems(["All", "English", "Hindi"])
        self.language_combo.setMinimumWidth(180)

        self.exam_combo = QComboBox()
        self.exam_combo.addItem("All Exams")
        self.exam_combo.setMinimumWidth(260)

        self.period_combo = QComboBox()
        self.period_combo.addItems(["All Time", "Today", "Last 7 Days", "Last 30 Days"])
        self.period_combo.setMinimumWidth(210)

        filter_row.addLayout(filter_block("Language", self.language_combo), 1)
        filter_row.addLayout(filter_block("Exam", self.exam_combo), 2)
        filter_row.addLayout(filter_block("Period", self.period_combo), 1)
        fl.addLayout(filter_row)
        layout.addWidget(filter_card)

        # TABLE
        table_card = QFrame()
        table_card.setObjectName("tableCard")
        tl = QVBoxLayout(table_card)
        tl.setContentsMargins(1, 1, 1, 1)
        tl.setSpacing(0)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Date & Time", "Language", "Mode", "Exam",
            "Net WPM", "Accuracy", "Mistakes", "Result"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setDefaultSectionSize(46)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(True)

        tl.addWidget(self.table)
        layout.addWidget(table_card, 1)

        # ACTIONS
        actions = QHBoxLayout()
        actions.setSpacing(9)

        self.details_btn = QPushButton("◉  View Details")
        self.details_btn.setObjectName("detailsButton")
        self.delete_btn = QPushButton("▣  Delete Selected")
        self.delete_btn.setObjectName("deleteButton")
        self.export_btn = QPushButton("↓  Export CSV")
        self.export_btn.setObjectName("exportButton")
        self.refresh_btn = QPushButton("↻  Refresh")
        self.refresh_btn.setObjectName("refreshButton")
        self.clear_btn = QPushButton("◇  Clear History")
        self.clear_btn.setObjectName("clearButton")

        actions.addWidget(self.details_btn)
        actions.addWidget(self.delete_btn)
        actions.addStretch()
        actions.addWidget(self.export_btn)
        actions.addWidget(self.refresh_btn)
        actions.addWidget(self.clear_btn)
        layout.addLayout(actions)

        self.language_combo.currentIndexChanged.connect(self.apply_filters)
        self.exam_combo.currentIndexChanged.connect(self.apply_filters)
        self.period_combo.currentIndexChanged.connect(self.apply_filters)
        self.details_btn.clicked.connect(self.view_details)
        self.delete_btn.clicked.connect(self.delete_selected_report)
        self.export_btn.clicked.connect(self.export_csv)
        self.refresh_btn.clicked.connect(self.load_reports)
        self.clear_btn.clicked.connect(self.clear_history)
        self.table.cellDoubleClicked.connect(lambda row, column: self.view_details())

    # =====================================================
    # Load Reports
    # =====================================================

    def load_reports(self):

        raw_reports = (
            self.report_manager.load_reports()
        )

        # Store the original JSON index with each report.
        # This makes Delete Selected safe even when filters are active.
        self.all_reports = []

        for source_index, report in enumerate(
            raw_reports
        ):

            item = dict(
                report
            )

            item["_source_index"] = (
                source_index
            )

            self.all_reports.append(
                item
            )

        # Latest result first
        self.all_reports.reverse()

        self.load_exam_filter()

        self.apply_filters()

    # =====================================================
    # Exam Filter
    # =====================================================

    def load_exam_filter(self):

        current_exam = (
            self.exam_combo.currentText()
        )

        self.exam_combo.blockSignals(
            True
        )

        self.exam_combo.clear()

        self.exam_combo.addItem(
            "All Exams"
        )

        exams = set()

        for report in self.all_reports:

            exam = report.get(
                "exam",
                ""
            )

            if exam:
                exams.add(
                    exam
                )

        for exam in sorted(
            exams
        ):

            self.exam_combo.addItem(
                exam
            )

        index = self.exam_combo.findText(
            current_exam
        )

        if index >= 0:

            self.exam_combo.setCurrentIndex(
                index
            )

        self.exam_combo.blockSignals(
            False
        )

    # =====================================================
    # Apply Filters
    # =====================================================

    def apply_filters(self):

        language = (
            self.language_combo.currentText()
        )

        exam = (
            self.exam_combo.currentText()
        )

        period = (
            self.period_combo.currentText()
        )

        filtered = []

        now = datetime.now()

        for report in self.all_reports:

            # Language
            if (
                language != "All"
                and report.get(
                    "language"
                ) != language
            ):
                continue

            # Exam
            if (
                exam != "All Exams"
                and report.get(
                    "exam"
                ) != exam
            ):
                continue

            # Date
            report_date = None

            try:

                report_date = datetime.strptime(
                    report.get(
                        "date",
                        ""
                    ),
                    "%Y-%m-%d %H:%M:%S"
                )

            except (
                ValueError,
                TypeError
            ):

                pass

            if report_date:

                if period == "Today":

                    if (
                        report_date.date()
                        != now.date()
                    ):
                        continue

                elif period == "Last 7 Days":

                    if (
                        report_date
                        < now - timedelta(
                            days=7
                        )
                    ):
                        continue

                elif period == "Last 30 Days":

                    if (
                        report_date
                        < now - timedelta(
                            days=30
                        )
                    ):
                        continue

            filtered.append(
                report
            )

        self.filtered_reports = (
            filtered
        )

        self.fill_table(
            filtered
        )

        self.update_summary(
            filtered
        )

    # =====================================================
    # Exam Result Text
    # =====================================================

    def get_result_text(
        self,
        report
    ):

        mode = report.get(
            "mode",
            ""
        )

        exam = report.get(
            "exam",
            ""
        )

        if mode == "Custom Test":

            return report.get(
                "custom_result",
                "Completed"
            ) or "Completed"

        if (
            mode != "Exam Mode"
            or not exam
        ):

            return "Completed"

        try:

            analysis = (
                self.exam_analyzer.analyze(
                    exam_name=exam,
                    net_wpm=float(
                        report.get(
                            "net_wpm",
                            0
                        )
                    ),
                    accuracy=float(
                        report.get(
                            "accuracy",
                            0
                        )
                    )
                )
            )

            if analysis.get(
                "qualified",
                False
            ):

                return "Qualified"

            return "Not Qualified"

        except Exception:

            return "Completed"

    # =====================================================
    # Fill Table
    # =====================================================

    def fill_table(
        self,
        reports
    ):

        self.table.clearContents()
        self.table.setRowCount(
            len(reports)
        )

        for row, report in enumerate(
            reports
        ):

            date_text = report.get(
                "date",
                ""
            )

            language = report.get(
                "language",
                ""
            )

            mode = report.get(
                "mode",
                ""
            )

            exam = report.get(
                "exam",
                ""
            )

            net_wpm = report.get(
                "net_wpm",
                0
            )

            accuracy = report.get(
                "accuracy",
                0
            )

            mistakes = report.get(
                "mistakes",
                report.get(
                    "wrong_chars",
                    0
                )
            )

            display_exam = (
                exam
                if mode == "Exam Mode"
                else "-"
            )

            result_text = (
                self.get_result_text(
                    report
                )
            )

            values = [
                date_text,
                language,
                mode,
                display_exam,
                str(net_wpm),
                f"{accuracy}%",
                str(mistakes),
                result_text
            ]

            for column, value in enumerate(
                values
            ):

                item = QTableWidgetItem(
                    value
                )

                item.setTextAlignment(
                    Qt.AlignCenter
                )

                item.setData(
                    Qt.UserRole,
                    report.get(
                        "_source_index"
                    )
                )

                # Visual badge-style text colors only.
                if column == 1:
                    if language == "English":
                        item.setForeground(
                            QBrush(
                                QColor("#176FE3")
                            )
                        )
                    elif language == "Hindi":
                        item.setForeground(
                            QBrush(
                                QColor("#6F3DE5")
                            )
                        )

                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)

                elif column == 5:
                    try:
                        acc_num = float(
                            accuracy
                        )
                    except (
                        TypeError,
                        ValueError
                    ):
                        acc_num = 0

                    item.setForeground(
                        QBrush(
                            QColor(
                                "#159457"
                                if acc_num >= 80
                                else "#E23D49"
                            )
                        )
                    )

                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)

                elif column == 7:
                    result_lower = (
                        str(result_text)
                        .lower()
                    )

                    if (
                        "completed"
                        in result_lower
                        or "qualified"
                        == result_lower
                        or "passed"
                        == result_lower
                    ):
                        color = "#16894D"

                    elif (
                        "not qualified"
                        in result_lower
                        or "not passed"
                        in result_lower
                    ):
                        color = "#E17B12"

                    else:
                        color = "#31475E"

                    item.setForeground(
                        QBrush(
                            QColor(color)
                        )
                    )

                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)

                self.table.setItem(
                    row,
                    column,
                    item
                )

    # =====================================================
    # Summary
    # =====================================================

    def update_summary(
        self,
        reports
    ):

        total = len(reports)

        if total == 0:

            self.total_test_lbl.setText("0")
            self.best_wpm_lbl.setText("0")
            self.avg_wpm_lbl.setText("0")
            self.avg_accuracy_lbl.setText("0%")
            return

        wpm_values = []
        accuracy_values = []

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
                TypeError,
                ValueError
            ):
                wpm_values.append(0)

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
                TypeError,
                ValueError
            ):
                accuracy_values.append(0)

        best_wpm = max(wpm_values)

        avg_wpm = (
            sum(wpm_values)
            / total
        )

        avg_accuracy = (
            sum(accuracy_values)
            / total
        )

        self.total_test_lbl.setText(
            str(total)
        )

        self.best_wpm_lbl.setText(
            f"{best_wpm:.2f}"
        )

        self.avg_wpm_lbl.setText(
            f"{avg_wpm:.2f}"
        )

        self.avg_accuracy_lbl.setText(
            f"{avg_accuracy:.2f}%"
        )

    # =====================================================
    # View Details
    # =====================================================

    def view_details(self):

        row = self.table.currentRow()

        if row < 0:

            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a report first."
            )

            return

        if (
            row
            >= len(
                self.filtered_reports
            )
        ):

            return

        report = (
            self.filtered_reports[
                row
            ]
        )

        mode = report.get(
            "mode",
            "-"
        )

        exam = report.get(
            "exam",
            "-"
        )

        display_exam = (
            exam
            if mode == "Exam Mode"
            else "-"
        )

        result_text = (
            self.get_result_text(
                report
            )
        )

        details = (
            f"Date : {report.get('date', '-')}\n"
            f"Language : {report.get('language', '-')}\n"
            f"Mode : {mode}\n"
            f"Exam : {display_exam}\n"
            f"Duration : {report.get('duration', 0)} Min\n\n"
            f"Gross WPM : {report.get('gross_wpm', 0)}\n"
            f"Net WPM : {report.get('net_wpm', 0)}\n"
            f"Accuracy : {report.get('accuracy', 0)}%\n"
            f"Mistakes : {report.get('mistakes', report.get('wrong_chars', 0))}\n"
            f"Correct Characters : {report.get('correct_chars', 0)}\n"
            f"Wrong Characters : {report.get('wrong_chars', 0)}\n"
            f"Backspace : {report.get('backspace', 0)}\n"
            + (
                f"\nCustom Target WPM : {report.get('custom_target_wpm', 0)}\n"
                f"Custom Target Accuracy : {report.get('custom_target_accuracy', 0)}%\n"
                if mode == "Custom Test"
                else ""
            )
            + f"\nResult : {result_text}"
        )

        QMessageBox.information(
            self,
            "Typing Test Details",
            details
        )

    # =====================================================
    # Delete Selected
    # =====================================================

    def delete_selected_report(self):

        row = self.table.currentRow()

        if row < 0:

            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a report first."
            )

            return

        item = self.table.item(
            row,
            0
        )

        if item is None:

            return

        source_index = item.data(
            Qt.UserRole
        )

        if source_index is None:

            QMessageBox.critical(
                self,
                "Delete Error",
                "Unable to identify the selected report."
            )

            return

        reply = QMessageBox.question(
            self,
            "Delete Report",
            "Are you sure you want to delete the selected report?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:

            return

        if self.report_manager.delete_report(
            int(
                source_index
            )
        ):

            self.load_reports()

    # =====================================================
    # Clear History
    # =====================================================

    def clear_history(self):

        if not self.all_reports:

            QMessageBox.information(
                self,
                "No Reports",
                "There is no report history to clear."
            )

            return

        reply = QMessageBox.question(
            self,
            "Clear History",
            "Are you sure you want to delete all report history?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:

            return

        if self.report_manager.clear_reports():

            self.load_reports()

            QMessageBox.information(
                self,
                "History Cleared",
                "All report history has been deleted."
            )

    # =====================================================
    # Export CSV
    # =====================================================

    def export_csv(self):

        if self.table.rowCount() == 0:

            QMessageBox.information(
                self,
                "No Data",
                "There is no report data to export."
            )

            return

        file_path, _ = (
            QFileDialog.getSaveFileName(
                self,
                "Export Report",
                "typing_reports.csv",
                "CSV Files (*.csv)"
            )
        )

        if not file_path:

            return

        if not file_path.lower().endswith(
            ".csv"
        ):

            file_path += ".csv"

        try:

            with open(
                file_path,
                "w",
                newline="",
                encoding="utf-8-sig"
            ) as file:

                writer = csv.writer(
                    file
                )

                headers = []

                for column in range(
                    self.table.columnCount()
                ):

                    item = (
                        self.table
                        .horizontalHeaderItem(
                            column
                        )
                    )

                    headers.append(
                        item.text()
                        if item
                        else ""
                    )

                writer.writerow(
                    headers
                )

                for row in range(
                    self.table.rowCount()
                ):

                    row_data = []

                    for column in range(
                        self.table.columnCount()
                    ):

                        item = self.table.item(
                            row,
                            column
                        )

                        row_data.append(
                            item.text()
                            if item
                            else ""
                        )

                    writer.writerow(
                        row_data
                    )

            QMessageBox.information(
                self,
                "Export Complete",
                "Report exported successfully."
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Export Error",
                str(
                    error
                )
            )

    # =====================================================
    # Auto Refresh
    # =====================================================

    def showEvent(
        self,
        event
    ):

        super().showEvent(
            event
        )

        self.load_reports()
