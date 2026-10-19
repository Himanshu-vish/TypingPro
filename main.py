import sys
import ctypes
from pathlib import Path

from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import QApplication

# IMPORTANT:
# Splash lightweight hai, isliye ise start me import kar sakte hain.
from app.ui.splash_screen import SplashScreen


# =========================================================
# BASIC APP INFORMATION
# =========================================================

APP_NAME = "TypingPro"
APP_VERSION = "1.0.0"

LAUNCHER_MODE = "--launcher-mode" in sys.argv
READY_FILE = None
for _arg in sys.argv[1:]:
    if _arg.startswith("--ready-file="):
        READY_FILE = _arg.split("=", 1)[1].strip().strip('"')
        break

QT_ARGV = [_arg for _arg in sys.argv if _arg != "--launcher-mode" and not _arg.startswith("--ready-file=")]

def signal_launcher_ready():
    if not READY_FILE:
        return
    try:
        ready_path = Path(READY_FILE)
        ready_path.parent.mkdir(parents=True, exist_ok=True)
        ready_path.write_text("READY", encoding="utf-8")
    except Exception:
        pass


# =========================================================
# FAST RESOURCE PATH
# =========================================================
# Dashboard/app_paths ko import kiye bina icon mil jayega.
# Isse splash jaldi show ho sakta hai.

def fast_resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent

    return str(base_path / relative_path)


# =========================================================
# PROFESSIONAL GLOBAL STYLE
# =========================================================

PROFESSIONAL_QSS = """
QWidget {
    font-family: "Segoe UI";
    font-size: 10.5pt;
    color: #172033;
}

QMainWindow,
QStackedWidget {
    background: #F4F7FB;
}

QWidget:disabled {
    color: #9AA5B5;
}

QLabel {
    background: transparent;
    color: #172033;
}

QLabel:disabled {
    color: #9AA5B5;
}

QPushButton {
    background: #FFFFFF;
    color: #263449;
    border: 1px solid #D8E0EB;
    border-radius: 7px;
    padding: 7px 14px;
    min-height: 22px;
    font-weight: 600;
}

QPushButton:hover {
    background: #F3F7FF;
    border: 1px solid #AFC5EA;
    color: #1557A0;
}

QPushButton:pressed {
    background: #E8F0FC;
    border: 1px solid #7FA5D8;
}

QPushButton:focus {
    border: 1px solid #4F8DD8;
}

QPushButton:disabled {
    background: #F0F2F5;
    color: #A1A9B5;
    border: 1px solid #E0E4EA;
}

QComboBox {
    background: #FFFFFF;
    color: #172033;
    border: 1px solid #CBD5E1;
    border-radius: 7px;
    padding: 6px 30px 6px 10px;
    min-height: 24px;
}

QComboBox:hover {
    border: 1px solid #8EB1DE;
}

QComboBox:focus {
    border: 1px solid #3979C6;
}

QComboBox:disabled {
    background: #F0F2F5;
    color: #9AA5B5;
}

QComboBox::drop-down {
    width: 28px;
    border: none;
}

QComboBox QAbstractItemView {
    background: #FFFFFF;
    color: #172033;
    border: 1px solid #D8E0EB;
    border-radius: 6px;
    selection-background-color: #E6F0FD;
    selection-color: #145DA0;
    padding: 4px;
    outline: none;
}

QTextEdit,
QPlainTextEdit,
QLineEdit {
    background: #FFFFFF;
    color: #172033;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    padding: 7px;
    selection-background-color: #BFD8F7;
    selection-color: #172033;
}

QTextEdit:hover,
QPlainTextEdit:hover,
QLineEdit:hover {
    border: 1px solid #A8BFDA;
}

QTextEdit:focus,
QPlainTextEdit:focus,
QLineEdit:focus {
    border: 2px solid #3B82D0;
    padding: 6px;
}

QTextEdit[readOnly="true"] {
    background: #FBFCFE;
}

QCheckBox,
QRadioButton {
    spacing: 7px;
    color: #263449;
    padding: 2px;
}

QCheckBox:hover,
QRadioButton:hover {
    color: #1557A0;
}

QProgressBar {
    background: #E8EDF4;
    color: #304155;
    border: none;
    border-radius: 6px;
    min-height: 12px;
    text-align: center;
    font-size: 9pt;
}

QProgressBar::chunk {
    background: #2E7DCE;
    border-radius: 6px;
}

QTableWidget {
    background: #FFFFFF;
    alternate-background-color: #F8FAFD;
    color: #263449;
    border: 1px solid #DCE3EC;
    border-radius: 8px;
    gridline-color: #E5EAF0;
    selection-background-color: #DCEBFA;
    selection-color: #153B66;
}

QTableWidget::item {
    padding: 7px;
}

QHeaderView::section {
    background: #EDF3FA;
    color: #263449;
    border: none;
    border-right: 1px solid #D8E0E9;
    border-bottom: 1px solid #D8E0E9;
    padding: 8px;
    font-weight: 700;
}

QScrollBar:vertical {
    background: #F1F4F8;
    width: 11px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #B8C3D1;
    min-height: 32px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background: #8FA2B8;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background: #F1F4F8;
    height: 11px;
    margin: 0;
}

QScrollBar::handle:horizontal {
    background: #B8C3D1;
    min-width: 32px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal:hover {
    background: #8FA2B8;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0;
}

QMenu {
    background: #FFFFFF;
    color: #172033;
    border: 1px solid #D8E0EB;
    border-radius: 7px;
    padding: 5px;
}

QMenu::item {
    padding: 7px 25px 7px 12px;
    border-radius: 5px;
}

QMenu::item:selected {
    background: #E8F1FC;
    color: #145DA0;
}

QToolTip {
    background: #172033;
    color: #FFFFFF;
    border: none;
    padding: 6px;
}

QDialog {
    background: #F7F9FC;
}

QDialog QLabel {
    color: #172033;
}

QGroupBox {
    background: #FFFFFF;
    border: 1px solid #DCE3EC;
    border-radius: 9px;
    margin-top: 12px;
    padding-top: 12px;
    font-weight: 700;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 5px;
    color: #263449;
}

QFrame {
    border-color: #DCE3EC;
}

QStatusBar {
    background: #FFFFFF;
    color: #64748B;
    border-top: 1px solid #E2E8F0;
    min-height: 24px;
}

QStatusBar::item {
    border: none;
}
"""


# =========================================================
# WINDOWS TASKBAR APP ID
# =========================================================

if sys.platform == "win32":
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "TypingPro.DesktopApp.1.0"
        )
    except Exception:
        pass


# =========================================================
# CREATE QT APPLICATION IMMEDIATELY
# =========================================================

app = QApplication(QT_ARGV)

app.setApplicationName(APP_NAME)
app.setApplicationVersion(APP_VERSION)
app.setOrganizationName(APP_NAME)

app.setStyle("Fusion")
app.setFont(QFont("Segoe UI", 10))


# =========================================================
# ICON - WITHOUT LOADING MAIN APPLICATION
# =========================================================

icon_path = fast_resource_path(
    "assets/icons/typingpro.ico"
)

typingpro_icon = QIcon(icon_path)

app.setWindowIcon(typingpro_icon)


# =========================================================
# SHOW SPLASH IMMEDIATELY
# =========================================================

splash = None
if not LAUNCHER_MODE:
    splash = SplashScreen(icon_path=icon_path, version=APP_VERSION)
    splash.show()
    app.processEvents()

def update_splash(text, progress):
    if splash is not None:
        splash.set_status(text, progress)
        app.processEvents()


# =========================================================
# GLOBAL MAIN WINDOW
# =========================================================

window = None


# =========================================================
# LOAD HEAVY APPLICATION AFTER SPLASH
# =========================================================

def load_typingpro():

    global window

    try:

        # -------------------------------------------------
        # 10%
        # -------------------------------------------------

        update_splash("Starting TypingPro...", 10)

        # =================================================
        # HEAVY IMPORTS AB START HONGE
        # =================================================
        # IMPORTANT:
        # DashboardWindow ko top par import NAHI kiya gaya.
        # Ab splash already screen par visible hai.

        update_splash("Loading application modules...", 25)

        from app.core.app_paths import migrate_legacy_reports, migrate_legacy_database

        # -------------------------------------------------
        # DATA
        # -------------------------------------------------

        update_splash("Preparing your data...", 40)

        migrate_legacy_database()
        migrate_legacy_reports()

        # -------------------------------------------------
        # HEAVY DASHBOARD IMPORT
        # -------------------------------------------------

        update_splash("Loading typing workspace...", 55)

        from app.ui.dashboard import DashboardWindow

        # -------------------------------------------------
        # CREATE COMPLETE APPLICATION
        # -------------------------------------------------

        update_splash("Loading English, Hindi and Learning modules...", 70)

        # Apply the global style BEFORE constructing the full widget tree.
        # This avoids creating every page once and then repolishing the
        # complete application afterwards.
        app.setStyleSheet(PROFESSIONAL_QSS)

        window = DashboardWindow()

        window.setWindowIcon(
            typingpro_icon
        )

        update_splash("Finishing your workspace...", 90)

        # -------------------------------------------------
        # COMPLETE
        # -------------------------------------------------

        update_splash("TypingPro is ready!", 100)

        window.show()
        app.processEvents()
        signal_launcher_ready()

        if splash is not None:
            splash.close()

    except Exception:

        if splash is not None:
            splash.close()
        raise


# =========================================================
# START LOADING AFTER SPLASH HAS BEEN PAINTED
# =========================================================

QTimer.singleShot(
    0,
    load_typingpro
)


# =========================================================
# RUN
# =========================================================

sys.exit(
    app.exec()
)