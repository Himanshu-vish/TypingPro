from app.core.version import APP_DISPLAY_VERSION

from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QButtonGroup
)
from PySide6.QtCore import Signal, Qt


class Sidebar(QFrame):

    page_changed = Signal(int)

    def __init__(self):
        super().__init__()

        # QFrame is used instead of plain QWidget so the sidebar
        # background is always painted correctly.
        self.setObjectName("sidebar")
        self.setFixedWidth(270)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.setStyleSheet("""
            QFrame#sidebar {
                background-color: #102A46;
                border: none;
            }

            QLabel#logo {
                background-color: #1976E8;
                color: #FFFFFF;
                border: none;
                border-radius: 12px;
                font-family: "Segoe UI";
                font-size: 26px;
                font-weight: 800;
            }

            QLabel#brandName {
                background: transparent;
                color: #FFFFFF;
                border: none;
                font-family: "Segoe UI";
                font-size: 21px;
                font-weight: 750;
            }

            QLabel#version {
                background: transparent;
                color: #AFC2D5;
                border: none;
                font-family: "Segoe UI";
                font-size: 11px;
                font-weight: 600;
            }

            QLabel#suiteText {
                background: transparent;
                color: #91A9C0;
                border: none;
                font-family: "Segoe UI";
                font-size: 9.5px;
                font-weight: 500;
            }

            QPushButton#navButton {
                background-color: transparent;
                color: #E8F0F7;
                border: none;
                border-radius: 9px;
                text-align: left;
                padding-left: 17px;
                padding-right: 10px;
                min-height: 52px;
                font-family: "Segoe UI";
                font-size: 14px;
                font-weight: 650;
            }

            QPushButton#navButton:hover {
                background-color: #1B4266;
                color: #FFFFFF;
            }

            QPushButton#navButton:checked {
                background-color: #1976E8;
                color: #FFFFFF;
                font-weight: 750;
            }

            QFrame#statusCard {
                background-color: #153A5C;
                border: 1px solid #2B587C;
                border-radius: 11px;
            }

            QLabel#readyDot {
                background-color: #26C86B;
                border: none;
                border-radius: 7px;
            }

            QLabel#readyTitle {
                background: transparent;
                color: #FFFFFF;
                border: none;
                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 700;
            }

            QLabel#readySub {
                background: transparent;
                color: #9AB0C5;
                border: none;
                font-family: "Segoe UI";
                font-size: 9.5px;
                font-weight: 500;
            }
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 18, 12, 14)
        root.setSpacing(7)

        # =================================================
        # BRAND
        # =================================================

        brand = QFrame()
        brand.setStyleSheet(
            "QFrame { background: transparent; border: none; }"
        )

        brand_layout = QHBoxLayout(brand)
        brand_layout.setContentsMargins(4, 0, 4, 13)
        brand_layout.setSpacing(12)

        logo = QLabel("TP")
        logo.setObjectName("logo")
        logo.setFixedSize(62, 62)
        logo.setAlignment(Qt.AlignCenter)

        brand_copy = QVBoxLayout()
        brand_copy.setSpacing(1)

        brand_name = QLabel("TypingPro")
        brand_name.setObjectName("brandName")

        version = QLabel(APP_DISPLAY_VERSION)
        version.setObjectName("version")

        suite = QLabel("Smart Typing Practice Suite")
        suite.setObjectName("suiteText")

        brand_copy.addWidget(brand_name)
        brand_copy.addWidget(version)
        brand_copy.addWidget(suite)

        brand_layout.addWidget(logo)
        brand_layout.addLayout(brand_copy, 1)

        root.addWidget(brand)

        # =================================================
        # SIDEBAR SERIAL ORDER
        #
        # Visible order:
        # Dashboard
        # Learn Typing
        # English Typing
        # Hindi Typing
        # Settings
        # Reports
        # About
        #
        # Existing dashboard stack:
        # 0 Dashboard
        # 1 English
        # 2 Hindi
        # 3 Learn
        # 4 Reports
        # 5 Settings
        # 6 About
        # =================================================

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        self.buttons = []

        menu_items = [
            ("⌂", "Dashboard", 0),
            ("🎓", "Learn Typing", 3),
            ("⌨", "English Typing", 1),
            ("अ", "Hindi Typing", 2),
            ("⚙", "Settings", 5),
            ("▥", "Reports", 4),
            ("●", "About", 6),
        ]

        for visual_index, (icon, title, page_index) in enumerate(menu_items):

            button = QPushButton(f"{icon}     {title}")
            button.setObjectName("navButton")
            button.setCheckable(True)
            button.setCursor(Qt.PointingHandCursor)

            button.clicked.connect(
                lambda checked=False,
                page=page_index,
                visual=visual_index:
                self.change_page(page, visual)
            )

            self.button_group.addButton(button, visual_index)
            self.buttons.append(button)
            root.addWidget(button)

        self.buttons[0].setChecked(True)

        root.addStretch()

        # =================================================
        # READY STATUS
        # =================================================

        status = QFrame()
        status.setObjectName("statusCard")
        status.setAttribute(Qt.WA_StyledBackground, True)

        status_layout = QHBoxLayout(status)
        status_layout.setContentsMargins(14, 11, 14, 11)
        status_layout.setSpacing(9)

        dot = QLabel()
        dot.setObjectName("readyDot")
        dot.setFixedSize(14, 14)

        status_copy = QVBoxLayout()
        status_copy.setSpacing(1)

        ready_title = QLabel("TypingPro Ready")
        ready_title.setObjectName("readyTitle")

        ready_sub = QLabel("All systems operational")
        ready_sub.setObjectName("readySub")

        status_copy.addWidget(ready_title)
        status_copy.addWidget(ready_sub)

        status_layout.addWidget(dot, 0, Qt.AlignTop)
        status_layout.addLayout(status_copy, 1)

        root.addWidget(status)

    def change_page(self, page_index, visual_index):
        self.setCurrentRow(visual_index)
        self.page_changed.emit(page_index)

    # Compatibility with existing dashboard.py
    def setCurrentRow(self, visual_index):
        if 0 <= visual_index < len(self.buttons):
            self.buttons[visual_index].setChecked(True)

    def currentRow(self):
        for index, button in enumerate(self.buttons):
            if button.isChecked():
                return index
        return 0
