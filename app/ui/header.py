from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QStyle
)
from PySide6.QtCore import Signal, QSize, Qt
from PySide6.QtGui import QFont

from app.core.session_manager import SessionManager


class Header(QFrame):

    sign_in_requested = Signal()
    sign_up_requested = Signal()
    logout_requested = Signal()

    def __init__(self):
        super().__init__()

        self.setObjectName("appHeader")
        self.setFixedHeight(82)

        self.setStyleSheet("""
            QFrame#appHeader {
                background: #FFFFFF;
                border: none;
                border-bottom: 1px solid #DCE4EE;
            }

            QLabel#menuIcon {
                color: #17395F;
                font-size: 23px;
                font-weight: 700;
                padding-right: 8px;
            }

            QLabel#pageTitle {
                color: #102A49;
                font-size: 21px;
                font-weight: 700;
            }

            QLabel#pageSubtitle {
                color: #718096;
                font-size: 11px;
                font-weight: 500;
            }

            QLabel#welcomeText {
                color: #102A49;
                font-size: 12px;
                font-weight: 700;
            }

            QLabel#guestText {
                color: #155ED1;
                font-size: 12px;
                font-weight: 700;
            }

            QPushButton#signinButton,
            QPushButton#signupButton,
            QPushButton#logoutButton {
                min-height: 36px;
                border-radius: 8px;
                padding: 5px 14px;
                font-size: 11px;
                font-weight: 700;
            }

            QPushButton#signinButton {
                background: #FFFFFF;
                color: #175FC5;
                border: 1px solid #77A9EB;
            }

            QPushButton#signinButton:hover {
                background: #F2F7FF;
                border-color: #4789DC;
            }

            QPushButton#signupButton {
                background: #1767D9;
                color: #FFFFFF;
                border: 1px solid #1767D9;
            }

            QPushButton#signupButton:hover {
                background: #125CC7;
            }

            QPushButton#logoutButton {
                background: #FFF7F5;
                color: #B5473C;
                border: 1px solid #E5B7B1;
            }

            QPushButton#logoutButton:hover {
                background: #FFF0ED;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(26, 0, 28, 0)
        layout.setSpacing(10)

        menu = QLabel("☰")
        menu.setObjectName("menuIcon")
        menu.setFixedWidth(34)
        menu.setAlignment(Qt.AlignCenter)

        title_box = QVBoxLayout()
        title_box.setSpacing(0)

        self.title_lbl = QLabel("TypingPro Dashboard")
        self.title_lbl.setObjectName("pageTitle")

        self.subtitle_lbl = QLabel(
            "Your daily companion for better typing"
        )
        self.subtitle_lbl.setObjectName("pageSubtitle")

        title_box.addWidget(self.title_lbl)
        title_box.addWidget(self.subtitle_lbl)

        layout.addWidget(menu)
        layout.addLayout(title_box)
        layout.addStretch()

        welcome_box = QHBoxLayout()
        welcome_box.setSpacing(4)

        welcome = QLabel("Welcome,")
        welcome.setObjectName("welcomeText")

        self.user_lbl = QLabel()
        self.user_lbl.setObjectName("guestText")

        welcome_box.addWidget(welcome)
        welcome_box.addWidget(self.user_lbl)

        layout.addLayout(welcome_box)
        layout.addSpacing(12)

        self.sign_in_btn = QPushButton("Sign In")
        self.sign_in_btn.setObjectName("signinButton")
        self.sign_in_btn.setIcon(
            self.style().standardIcon(
                QStyle.SP_DialogApplyButton
            )
        )

        self.sign_up_btn = QPushButton("Sign Up")
        self.sign_up_btn.setObjectName("signupButton")
        self.sign_up_btn.setIcon(
            self.style().standardIcon(
                QStyle.SP_FileDialogNewFolder
            )
        )

        self.logout_btn = QPushButton("Logout")
        self.logout_btn.setObjectName("logoutButton")
        self.logout_btn.setIcon(
            self.style().standardIcon(
                QStyle.SP_DialogCancelButton
            )
        )

        for button in (
            self.sign_in_btn,
            self.sign_up_btn,
            self.logout_btn
        ):
            button.setIconSize(QSize(16, 16))
            button.setCursor(Qt.PointingHandCursor)

        layout.addWidget(self.sign_in_btn)
        layout.addWidget(self.sign_up_btn)
        layout.addWidget(self.logout_btn)

        self.sign_in_btn.clicked.connect(
            self.sign_in_requested.emit
        )
        self.sign_up_btn.clicked.connect(
            self.sign_up_requested.emit
        )
        self.logout_btn.clicked.connect(
            self.logout_requested.emit
        )

        SessionManager.signals.profile_changed.connect(
            self.refresh_profile
        )

        self.refresh_profile()

    def set_page(self, title, subtitle=""):
        self.title_lbl.setText(title)
        self.subtitle_lbl.setText(subtitle)

    def refresh_profile(self):
        self.user_lbl.setText(
            SessionManager.display_name()
        )

        guest = SessionManager.is_guest()

        self.sign_in_btn.setVisible(guest)
        self.sign_up_btn.setVisible(guest)
        self.logout_btn.setVisible(not guest)
