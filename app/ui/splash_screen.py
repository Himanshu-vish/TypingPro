from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QFrame,
    QGraphicsDropShadowEffect,
    QSizePolicy,
)


class SplashScreen(QWidget):

    def __init__(self, icon_path, version="1.0.0"):
        super().__init__()

        self.setWindowFlags(
            Qt.SplashScreen
            | Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
        )

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(900, 540)

        self._build_ui(icon_path, version)
        self.center_on_screen()

    def showEvent(self, event):
        super().showEvent(event)

        # Pehle Qt splash ko properly paint hone do,
        # uske baad PyInstaller native splash close hoga.
        QTimer.singleShot(
            100,
            self.close_native_splash
        )

    def close_native_splash(self):
        try:
            import pyi_splash

            if pyi_splash.is_alive():
                pyi_splash.close()

        except Exception:
            # python main.py se run karne par pyi_splash nahi hota.
            pass

    # =========================================================
    # BUILD UI
    # =========================================================

    def _build_ui(self, icon_path, version):

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)

        card = QFrame()
        card.setObjectName("SplashMainCard")

        card.setStyleSheet("""
            QFrame#SplashMainCard {
                background: qlineargradient(
                    x1:0,
                    y1:0,
                    x2:1,
                    y2:1,
                    stop:0 #FFFFFF,
                    stop:0.52 #FBFDFF,
                    stop:1 #EAF5FF
                );
                border: 1px solid #C9DDF2;
                border-radius: 26px;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(42)
        shadow.setOffset(0, 8)

        card.setGraphicsEffect(shadow)
        root.addWidget(card)

        main = QVBoxLayout(card)

        main.setContentsMargins(
            55,
            24,
            55,
            26
        )

        main.setSpacing(0)

        # =====================================================
        # VERSION
        # =====================================================

        version_row = QHBoxLayout()
        version_row.addStretch()

        version_label = QLabel(
            f"Version {version}"
        )

        version_label.setStyleSheet("""
            QLabel {
                color: #58718D;
                font-family: "Segoe UI";
                font-size: 14px;
                background: transparent;
            }
        """)

        version_row.addWidget(version_label)
        main.addLayout(version_row)

        # =====================================================
        # ICON
        # =====================================================

        main.addSpacing(5)

        icon_row = QHBoxLayout()
        icon_row.addStretch()

        icon_label = QLabel()

        app_icon = QIcon(icon_path)

        icon_label.setPixmap(
            app_icon.pixmap(
                105,
                105
            )
        )

        icon_label.setFixedSize(
            115,
            115
        )

        icon_label.setAlignment(
            Qt.AlignCenter
        )

        icon_label.setStyleSheet(
            "background: transparent;"
        )

        icon_row.addWidget(icon_label)
        icon_row.addStretch()

        main.addLayout(icon_row)

        # =====================================================
        # TYPINGPRO
        # =====================================================

        title_row = QHBoxLayout()

        title_row.setContentsMargins(
            0, 0, 0, 0
        )

        title_row.setSpacing(0)

        title_row.addStretch()

        typing_label = QLabel("Typing")

        typing_label.setFixedHeight(72)

        typing_label.setAlignment(
            Qt.AlignCenter
        )

        typing_label.setStyleSheet("""
            QLabel {
                color: #061A48;
                font-family: "Segoe UI";
                font-size: 54px;
                font-weight: 800;
                background: transparent;
                padding: 0px;
                margin: 0px;
            }
        """)

        pro_label = QLabel("Pro")

        pro_label.setFixedHeight(72)

        pro_label.setAlignment(
            Qt.AlignCenter
        )

        pro_label.setStyleSheet("""
            QLabel {
                color: #1684F8;
                font-family: "Segoe UI";
                font-size: 54px;
                font-weight: 800;
                background: transparent;
                padding: 0px;
                margin: 0px;
            }
        """)

        title_row.addWidget(typing_label)
        title_row.addWidget(pro_label)

        title_row.addStretch()

        main.addLayout(title_row)

        # =====================================================
        # SUBTITLE
        # =====================================================

        subtitle = QLabel(
            "P R A C T I C E   •   T Y P E   •   I M P R O V E"
        )

        subtitle.setAlignment(
            Qt.AlignCenter
        )

        subtitle.setFixedHeight(25)

        subtitle.setStyleSheet("""
            QLabel {
                color: #587392;
                font-family: "Segoe UI";
                font-size: 13px;
                font-weight: 600;
                background: transparent;
            }
        """)

        main.addWidget(subtitle)

        # =====================================================
        # PROGRESS
        # =====================================================

        main.addSpacing(25)

        progress_holder = QWidget()

        progress_holder.setStyleSheet(
            "background: transparent;"
        )

        progress_layout = QHBoxLayout(
            progress_holder
        )

        progress_layout.setContentsMargins(
            130,
            0,
            130,
            0
        )

        self.progress = QProgressBar()

        self.progress.setRange(
            0,
            100
        )

        self.progress.setValue(15)

        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(12)

        self.progress.setStyleSheet("""
            QProgressBar {
                background: #E3EDF6;
                border: none;
                border-radius: 6px;
            }

            QProgressBar::chunk {
                background: qlineargradient(
                    x1:0,
                    y1:0,
                    x2:1,
                    y2:0,
                    stop:0 #08A8F4,
                    stop:1 #1687F8
                );
                border-radius: 6px;
            }
        """)

        progress_layout.addWidget(
            self.progress
        )

        main.addWidget(
            progress_holder
        )

        # =====================================================
        # STATUS
        # =====================================================

        main.addSpacing(7)

        self.status_label = QLabel(
            "Preparing your typing workspace..."
        )

        self.status_label.setAlignment(
            Qt.AlignCenter
        )

        self.status_label.setFixedHeight(25)

        self.status_label.setStyleSheet("""
            QLabel {
                color: #294C73;
                font-family: "Segoe UI";
                font-size: 14px;
                background: transparent;
            }
        """)

        main.addWidget(
            self.status_label
        )

        # =====================================================
        # FEATURES
        # =====================================================

        main.addSpacing(20)

        feature_row = QHBoxLayout()

        feature_row.setContentsMargins(
            65,
            0,
            65,
            0
        )

        feature_row.setSpacing(22)

        feature_row.addWidget(
            self.feature_card(
                "⚡",
                "Improve",
                "Typing Speed",
                "#DDF1FF",
                "#F5B400"
            )
        )

        feature_row.addWidget(
            self.feature_card(
                "◎",
                "Build",
                "Accuracy",
                "#DDFBF2",
                "#1687F8"
            )
        )

        feature_row.addWidget(
            self.feature_card(
                "▥",
                "Track",
                "Progress",
                "#EFE8FF",
                "#7957E8"
            )
        )

        feature_row.addWidget(
            self.feature_card(
                "▤",
                "Learn",
                "Step by Step",
                "#FFF0DE",
                "#FF8B20"
            )
        )

        main.addLayout(
            feature_row
        )

        # =====================================================
        # QUOTE
        # =====================================================

        main.addSpacing(19)

        quote = QLabel(
            "“ Small Steps Create Big Results ”"
        )

        quote.setAlignment(
            Qt.AlignCenter
        )

        quote.setStyleSheet("""
            QLabel {
                color: #173A68;
                font-family: "Segoe UI";
                font-size: 18px;
                font-style: italic;
                background: transparent;
            }
        """)

        main.addWidget(quote)

        # =====================================================
        # DIVIDER
        # =====================================================

        main.addSpacing(11)

        divider_row = QHBoxLayout()

        divider_row.addStretch()

        divider = QFrame()

        divider.setFixedSize(
            50,
            3
        )

        divider.setStyleSheet("""
            QFrame {
                background: #1687F8;
                border: none;
                border-radius: 1px;
            }
        """)

        divider_row.addWidget(divider)
        divider_row.addStretch()

        main.addLayout(divider_row)

        # =====================================================
        # FOOTER
        # =====================================================

        main.addSpacing(12)

        footer = QLabel(
            "T Y P E   T O D A Y   F O R   A   B E T T E R   T O M O R R O W"
        )

        footer.setAlignment(
            Qt.AlignCenter
        )

        footer.setStyleSheet("""
            QLabel {
                color: #267CCD;
                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 600;
                background: transparent;
            }
        """)

        main.addWidget(footer)

    # =========================================================
    # FEATURE CARD
    # =========================================================

    def feature_card(
        self,
        symbol,
        first_line,
        second_line,
        circle_background,
        symbol_color
    ):

        container = QWidget()

        container.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred
        )

        container.setStyleSheet(
            "background: transparent;"
        )

        layout = QVBoxLayout(container)

        layout.setContentsMargins(
            3, 0, 3, 0
        )

        layout.setSpacing(2)

        icon = QLabel(symbol)

        icon.setFixedSize(
            55,
            55
        )

        icon.setAlignment(
            Qt.AlignCenter
        )

        icon.setStyleSheet(f"""
            QLabel {{
                background: {circle_background};
                color: {symbol_color};
                border-radius: 27px;
                font-family: "Segoe UI Symbol";
                font-size: 25px;
                font-weight: 700;
            }}
        """)

        icon_holder = QHBoxLayout()

        icon_holder.addStretch()
        icon_holder.addWidget(icon)
        icon_holder.addStretch()

        layout.addLayout(icon_holder)

        first = QLabel(first_line)

        first.setAlignment(
            Qt.AlignCenter
        )

        first.setStyleSheet("""
            QLabel {
                color: #0B2148;
                font-family: "Segoe UI";
                font-size: 13px;
                font-weight: 700;
                background: transparent;
            }
        """)

        second = QLabel(second_line)

        second.setAlignment(
            Qt.AlignCenter
        )

        second.setStyleSheet("""
            QLabel {
                color: #0B2148;
                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 600;
                background: transparent;
            }
        """)

        layout.addWidget(first)
        layout.addWidget(second)

        return container

    # =========================================================
    # STATUS
    # =========================================================

    def set_status(
        self,
        text,
        progress=None
    ):

        self.status_label.setText(text)

        if progress is not None:
            self.progress.setValue(
                progress
            )

    # =========================================================
    # CENTER
    # =========================================================

    def center_on_screen(self):

        screen = self.screen()

        if screen is None:
            return

        geometry = screen.availableGeometry()

        x = (
            geometry.x()
            + (
                geometry.width()
                - self.width()
            ) // 2
        )

        y = (
            geometry.y()
            + (
                geometry.height()
                - self.height()
            ) // 2
        )

        self.move(x, y)