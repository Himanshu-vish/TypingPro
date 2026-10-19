from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QSpinBox,
    QComboBox,
    QPushButton,
    QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class CustomTestDialog(QDialog):

    Accepted = QDialog.Accepted
    Rejected = QDialog.Rejected

    def __init__(
        self,
        parent=None,
        duration=5,
        target_wpm=30,
        target_accuracy=95,
        difficulty="Easy"
    ):
        super().__init__(parent)

        self.setWindowTitle("Custom Test Setup")
        self.setFixedWidth(430)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(14)

        title = QLabel("Create Custom Typing Test")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        layout.addWidget(title)

        info = QLabel(
            "Set your own duration, speed target, accuracy target "
            "and paragraph difficulty."
        )
        info.setWordWrap(True)
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)

        form = QFormLayout()

        self.duration = QSpinBox()
        self.duration.setRange(1, 30)
        self.duration.setSuffix(" Min")
        self.duration.setValue(int(duration))

        self.target_wpm = QSpinBox()
        self.target_wpm.setRange(1, 150)
        self.target_wpm.setSuffix(" WPM")
        self.target_wpm.setValue(int(target_wpm))

        self.target_accuracy = QSpinBox()
        self.target_accuracy.setRange(1, 100)
        self.target_accuracy.setSuffix("%")
        self.target_accuracy.setValue(int(target_accuracy))

        self.difficulty = QComboBox()
        self.difficulty.addItems(["Easy", "Medium", "Hard"])
        self.difficulty.setCurrentText(difficulty)

        form.addRow("Duration:", self.duration)
        form.addRow("Target WPM:", self.target_wpm)
        form.addRow("Target Accuracy:", self.target_accuracy)
        form.addRow("Difficulty:", self.difficulty)

        layout.addLayout(form)

        buttons = QHBoxLayout()

        self.start_btn = QPushButton("Start Custom Test")
        self.cancel_btn = QPushButton("Cancel")

        self.start_btn.setMinimumHeight(40)
        self.cancel_btn.setMinimumHeight(40)

        buttons.addWidget(self.start_btn)
        buttons.addWidget(self.cancel_btn)

        layout.addLayout(buttons)

        self.start_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

    def values(self):
        return {
            "duration": self.duration.value(),
            "target_wpm": self.target_wpm.value(),
            "target_accuracy": self.target_accuracy.value(),
            "difficulty": self.difficulty.currentText()
        }


class CustomResultDialog(QDialog):

    def __init__(
        self,
        result,
        target_wpm,
        target_accuracy,
        parent=None
    ):
        super().__init__(parent)

        self.setWindowTitle("Custom Test Result")
        self.setFixedWidth(500)

        net_wpm = float(result.get("net_wpm", 0))
        accuracy = float(result.get("accuracy", 0))

        passed = (
            net_wpm >= float(target_wpm)
            and accuracy >= float(target_accuracy)
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(12)

        title = QLabel(
            "CUSTOM TEST PASSED ✅"
            if passed
            else "CUSTOM TEST NOT PASSED ❌"
        )
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        layout.addWidget(title)

        details = QLabel(
            f"Target WPM : {target_wpm}\n"
            f"Your Net WPM : {net_wpm:.2f}\n\n"
            f"Target Accuracy : {target_accuracy}%\n"
            f"Your Accuracy : {accuracy:.2f}%\n\n"
            f"Gross WPM : {float(result.get('gross_wpm', 0)):.2f}\n"
            f"Wrong Characters : {result.get('wrong_chars', 0)}\n"
            f"Backspace : {result.get('backspace', 0)}"
        )
        details.setFont(QFont("Segoe UI", 11))
        details.setAlignment(Qt.AlignLeft)
        layout.addWidget(details)

        if passed:
            message = QLabel(
                "You achieved both your custom speed and accuracy targets."
            )
        else:
            need_wpm = max(0, float(target_wpm) - net_wpm)
            need_accuracy = max(0, float(target_accuracy) - accuracy)
            message = QLabel(
                f"Need WPM improvement: {need_wpm:.2f}\n"
                f"Need Accuracy improvement: {need_accuracy:.2f}%"
            )

        message.setWordWrap(True)
        layout.addWidget(message)

        close_btn = QPushButton("Close")
        close_btn.setMinimumHeight(40)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

    @staticmethod
    def status(result, target_wpm, target_accuracy):
        return (
            "Passed"
            if (
                float(result.get("net_wpm", 0)) >= float(target_wpm)
                and float(result.get("accuracy", 0)) >= float(target_accuracy)
            )
            else "Not Passed"
        )
