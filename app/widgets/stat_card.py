from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from app.core.theme import (
    CARD_BACKGROUND,
    BORDER_COLOR,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    RADIUS,
    FONT_FAMILY,
)


class StatCard(QFrame):

    def __init__(self, title, value):
        super().__init__()

        self.setMinimumSize(220, 120)

        self.setStyleSheet(f"""
        QFrame {{
            background: {CARD_BACKGROUND};
            border: 1px solid {BORDER_COLOR};
            border-radius: {RADIUS}px;
        }}

        QLabel {{
            border: none;
            background: transparent;
        }}
        """)

        layout = QVBoxLayout(self)

        layout.setContentsMargins(20, 15, 20, 15)

        title_label = QLabel(title)
        title_label.setFont(QFont(FONT_FAMILY, 10))
        title_label.setStyleSheet(f"color:{TEXT_SECONDARY};")

        self.value_label = QLabel(value)
        self.value_label.setFont(
            QFont(
                FONT_FAMILY,
                22,
                QFont.Bold
            )
        )
        self.value_label.setAlignment(
            Qt.AlignLeft
        )
        self.value_label.setStyleSheet(
            f"color:{TEXT_PRIMARY};"
        )

        layout.addWidget(title_label)
        layout.addSpacing(8)
        layout.addWidget(
        self.value_label
        )
        layout.addStretch()

    def set_value(self, value):

        self.value_label.setText(
            str(value)
        )