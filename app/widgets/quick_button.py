from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QFont


class QuickButton(QPushButton):

    def __init__(self, text):
        super().__init__(text)

        self.setMinimumHeight(55)

        self.setFont(QFont("Segoe UI", 11, QFont.Bold))

        self.setStyleSheet("""
            QPushButton{

                background:#1976D2;

                color:white;

                border:none;

                border-radius:10px;

            }

            QPushButton:hover{

                background:#1565C0;

            }

            QPushButton:pressed{

                background:#0D47A1;

            }
        """)