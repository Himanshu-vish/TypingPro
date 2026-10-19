from app.core.version import APP_DISPLAY_VERSION

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QStackedWidget,
    QStatusBar
)

from app.ui.sidebar import Sidebar
from app.ui.header import Header
from app.ui.dialogs.auth_dialogs import SignInDialog, SignUpDialog
from app.core.session_manager import SessionManager

# Pages
from app.ui.pages.dashboard_page import DashboardPage
from app.ui.pages.english_page import EnglishPage
from app.ui.pages.hindi_page import HindiPage
from app.ui.pages.learning_page import LearningPage
from app.ui.pages.reports_page import ReportsPage
from app.ui.pages.settings_page import SettingsPage
from app.ui.pages.about_page import AboutPage


class DashboardWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"TypingPro {APP_DISPLAY_VERSION}")
        self.resize(1480, 880)

        self.build_ui()

    def build_ui(self):

        # =====================================
        # Central Widget
        # =====================================

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # =====================================
        # Sidebar
        # =====================================

        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)

        # =====================================
        # Right Area
        # =====================================

        right_widget = QWidget()

        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # =====================================
        # Header
        # =====================================

        self.header = Header()
        right_layout.addWidget(self.header)

        # Guest / User account actions
        self.header.sign_in_requested.connect(self.open_sign_in)
        self.header.sign_up_requested.connect(self.open_sign_up)
        self.header.logout_requested.connect(self.logout_user)
        SessionManager.signals.profile_changed.connect(self.refresh_profile_data)

        # =====================================
        # Stacked Pages
        # =====================================

        self.stack = QStackedWidget()

        # Dashboard Page
        self.dashboard_page = DashboardPage()

        # English Page
        self.english_page = EnglishPage()

        # Hindi Page
        self.hindi_page = HindiPage()

        # Learning Page
        self.learning_page = LearningPage()

        # Reports Page
        self.reports_page = ReportsPage()

        # Settings Page
        self.settings_page = SettingsPage()

        # About Page
        self.about_page = AboutPage()
                # =====================================
        # Add Pages
        # =====================================

        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.english_page)
        self.stack.addWidget(self.hindi_page)
        self.stack.addWidget(self.learning_page)
        self.stack.addWidget(self.reports_page)
        self.stack.addWidget(self.settings_page)
        self.stack.addWidget(self.about_page)

        right_layout.addWidget(self.stack)

        main_layout.addWidget(right_widget)

        # =====================================
        # Sidebar Navigation
        # =====================================

        self.sidebar.page_changed.connect(self.open_page)

        # =====================================
        # Dashboard Quick Start Navigation
        # =====================================

        self.dashboard_page.english_btn.clicked.connect(
            lambda: self.open_page(1)
        )

        self.dashboard_page.hindi_btn.clicked.connect(
            lambda: self.open_page(2)
        )

        self.dashboard_page.upp_btn.clicked.connect(
            self.open_upp_practice
        )

        self.dashboard_page.ssc_btn.clicked.connect(
            self.open_ssc_typing
        )

        self.dashboard_page.ccc_btn.clicked.connect(
            self.open_ccc_practice
        )

        self.dashboard_page.learn_btn.clicked.connect(
            lambda: self.open_page(3)
        )

        # =====================================
        # Back To Dashboard
        # =====================================

        self.english_page.back_btn.clicked.connect(
            lambda: self.open_page(0)
        )

        self.hindi_page.back_btn.clicked.connect(
            lambda: self.open_page(0)
        )

        self.learning_page.back_btn.clicked.connect(
            lambda: self.open_page(0)
        )

        # =====================================
        # Status Bar
        # =====================================

        status = QStatusBar()
        status.showMessage("TypingPro • Ready")
        self.setStatusBar(status)

        self.open_page(0)

    # =====================================
    # Open Normal Page
    # =====================================

    # =====================================
    # Guest / User Profile
    # =====================================

    def open_sign_in(self):
        dialog = SignInDialog(self)
        dialog.exec()

    def open_sign_up(self):
        dialog = SignUpDialog(self)
        dialog.exec()

    def logout_user(self):
        SessionManager.logout()

    def refresh_profile_data(self):
        self.header.refresh_profile()

        if hasattr(self.dashboard_page, "load_dashboard_data"):
            self.dashboard_page.load_dashboard_data()

        if hasattr(self.reports_page, "load_reports"):
            self.reports_page.load_reports()

        if hasattr(self.settings_page, "load_settings"):
            self.settings_page.load_settings()

        if hasattr(self.learning_page, "refresh_profile"):
            self.learning_page.refresh_profile()

        # English/Hindi pages already read SettingsManager.
        # Re-apply settings only through their existing safe integration method.
        for page in (self.english_page, self.hindi_page):
            if hasattr(page, "refresh_settings"):
                page.refresh_settings()

    def open_page(self, index):

        self.stack.setCurrentIndex(index)

        # Every page shares this QStackedWidget. Keep the active page exactly
        # inside the stack viewport so a geometry change from one page cannot
        # remain visible when navigating to another page.
        current_page = self.stack.currentWidget()
        if current_page is not None:
            current_page.setGeometry(self.stack.contentsRect())
            current_page.updateGeometry()

        self.stack.updateGeometry()

        page_headers = {
            0: (
                "TypingPro Dashboard",
                "Your daily companion for better typing"
            ),
            1: (
                "English Typing",
                "Practice speed, accuracy and exam-ready English typing"
            ),
            2: (
                "Hindi Typing",
                "Practice Hindi typing with InScript keyboard support"
            ),
            3: (
                "Learn Typing",
                "Guided lessons and keyboard training"
            ),
            4: (
                "Reports",
                "Track progress, performance and previous tests"
            ),
            5: (
                "Settings",
                "Manage TypingPro preferences and behaviour"
            ),
            6: (
                "About TypingPro",
                "Know more about TypingPro and its features"
            ),
        }

        title, subtitle = page_headers.get(
            index,
            ("TypingPro", "")
        )

        if hasattr(self.header, "set_page"):
            self.header.set_page(
                title,
                subtitle
            )


    # =====================================
    # UPP Practice
    # =====================================

    def open_upp_practice(self):

        self.open_page(1)

        self.english_page.test_mode_combo.setCurrentText(
            "Exam Mode"
        )

        self.english_page.exam_combo.setCurrentText(
            "UPP Computer Operator"
        )


    # =====================================
    # SSC Typing
    # =====================================

    def open_ssc_typing(self):

        self.open_page(1)

        self.english_page.test_mode_combo.setCurrentText(
            "Exam Mode"
        )

        self.english_page.exam_combo.setCurrentText(
            "SSC CHSL LDC/JSA"
        )

    # =====================================
    # CCC Practice
    # =====================================

    def open_ccc_practice(self):

        self.open_page(1)

        self.english_page.test_mode_combo.setCurrentText(
            "Exam Mode"
        )

        self.english_page.exam_combo.setCurrentText(
            "CCC"
        )