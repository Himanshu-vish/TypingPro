from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QFont


class SectionTitle(QLabel):

    def __init__(self, text):
        super().__init__(text)

        self.setFont(QFont("Segoe UI", 16, QFont.Bold))

        self.setStyleSheet("""
            color:#222;
            margin-top:10px;
            margin-bottom:5px;
        """)