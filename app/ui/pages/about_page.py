from app.core.version import APP_DISPLAY_VERSION

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QFrame,
    QScrollArea,
    QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import (
    QPainter,
    QPen,
    QBrush,
    QColor,
    QFont
)


class DesktopIllustration(QWidget):
    """Code-drawn monitor + keyboard + plant to match the approved About UI."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(390, 180)
        self.setMaximumHeight(210)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        # subtle decorative dots
        p.setPen(Qt.NoPen)
        for x, y, r in [
            (w*0.76, h*0.13, 3), (w*0.83, h*0.21, 2),
            (w*0.91, h*0.14, 2), (w*0.95, h*0.42, 3),
            (w*0.69, h*0.32, 2), (w*0.87, h*0.51, 2)
        ]:
            p.setBrush(QColor("#BFD8F8"))
            p.drawEllipse(int(x), int(y), r, r)

        # monitor stand
        p.setBrush(QColor("#233B57"))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(QRectF(w*0.49, h*0.58, w*0.10, h*0.10), 4, 4)
        p.drawRoundedRect(QRectF(w*0.44, h*0.67, w*0.20, h*0.045), 4, 4)

        # monitor shell
        p.setBrush(QColor("#1D3552"))
        p.setPen(QPen(QColor("#17304C"), 2))
        p.drawRoundedRect(QRectF(w*0.34, h*0.07, w*0.40, h*0.51), 8, 8)

        # monitor screen
        p.setBrush(QColor("#2F7DEA"))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(QRectF(w*0.355, h*0.085, w*0.37, h*0.46), 5, 5)

        p.setPen(QColor("#FFFFFF"))
        p.setFont(QFont("Segoe UI", 32, QFont.Bold))
        p.drawText(
            QRectF(w*0.355, h*0.085, w*0.37, h*0.46),
            Qt.AlignCenter,
            "TP"
        )

        # keyboard
        p.setPen(QPen(QColor("#24415F"), 1))
        p.setBrush(QColor("#EDF3FA"))
        kb = QRectF(w*0.27, h*0.70, w*0.47, h*0.16)
        p.drawRoundedRect(kb, 7, 7)

        for row in range(3):
            for col in range(11):
                x = kb.x() + 9 + col * (kb.width()-18)/11
                y = kb.y() + 7 + row * (kb.height()-14)/3
                rw = (kb.width()-24)/12
                rh = (kb.height()-18)/4
                p.setBrush(QColor("#FFFFFF"))
                p.drawRoundedRect(QRectF(x, y, rw, rh), 2, 2)

        # mouse
        p.setBrush(QColor("#2B4968"))
        p.setPen(Qt.NoPen)
        p.drawEllipse(QRectF(w*0.77, h*0.74, w*0.065, h*0.09))

        # plant
        p.setBrush(QColor("#4B84D8"))
        p.drawRoundedRect(QRectF(w*0.86, h*0.54, w*0.06, h*0.18), 4, 4)

        p.setPen(QPen(QColor("#3B7A63"), 3))
        p.drawLine(int(w*0.89), int(h*0.54), int(w*0.86), int(h*0.37))
        p.drawLine(int(w*0.89), int(h*0.54), int(w*0.92), int(h*0.31))
        p.drawLine(int(w*0.89), int(h*0.54), int(w*0.89), int(h*0.27))

        p.setPen(Qt.NoPen)
        p.setBrush(QColor("#69A2E4"))
        p.drawEllipse(QRectF(w*0.835, h*0.31, w*0.045, h*0.12))
        p.setBrush(QColor("#4D8CD7"))
        p.drawEllipse(QRectF(w*0.905, h*0.25, w*0.045, h*0.12))
        p.setBrush(QColor("#82B5EC"))
        p.drawEllipse(QRectF(w*0.87, h*0.20, w*0.04, h*0.13))


class AboutPage(QWidget):

    def __init__(self):
        super().__init__()
        self.build_ui()

    def build_ui(self):

        self.setObjectName("aboutPage")
        self.setStyleSheet("""
            QWidget#aboutPage {
                background:#F4F7FB;
                font-family:"Segoe UI";
            }
            QFrame#heroCard,
            QFrame#featureCard,
            QFrame#infoCard,
            QFrame#examCard {
                background:#FFFFFF;
                border:1px solid #D9E3EE;
                border-radius:15px;
            }
            QFrame#heroCard {
                background:#F8FBFF;
                border:1px solid #C9DDF5;
            }
            QLabel#logo {
                background:#1769D5;
                color:#FFFFFF;
                border-radius:30px;
                font-size:30px;
                font-weight:900;
            }
            QLabel#badge {
                background:#E8F1FF;
                color:#1769D5;
                border:1px solid #C8DDF7;
                border-radius:7px;
                padding:6px 10px;
                font-size:12px;
                font-weight:800;
            }
            QLabel#heroTitle {
                color:#102A49;
                font-size:36px;
                font-weight:850;
            }
            QLabel#heroSub {
                color:#1769D5;
                font-size:19px;
                font-weight:800;
            }
            QLabel#heroBody {
                color:#455B72;
                font-size:14px;
                font-weight:650;
            }
            QLabel#sectionTitle {
                color:#17324F;
                font-size:20px;
                font-weight:850;
            }
            QLabel#featureIcon {
                border-radius:24px;
                min-width:48px;min-height:48px;
                max-width:48px;max-height:48px;
                font-size:20px;font-weight:800;
            }
            QLabel#featureTitle {
                color:#20364D;
                font-size:16px;
                font-weight:800;
            }
            QLabel#featureText {
                color:#52677D;
                font-size:13px;
                font-weight:650;
            }
            QLabel#infoCaption {
                color:#4B74A1;
                font-size:11px;
                font-weight:800;
            }
            QLabel#infoValue {
                color:#17324F;
                font-size:16px;
                font-weight:850;
            }
            QLabel#infoSub {
                color:#5A6F84;
                font-size:12px;
                font-weight:650;
            }
            QLabel#examTitle {
                color:#176345;
                font-size:17px;
                font-weight:850;
            }
            QLabel#examText {
                color:#4E6A5D;
                font-size:13px;
                font-weight:650;
            }
            QLabel#tag {
                background:#F8FBFF;
                color:#34566F;
                border:1px solid #CBD9E6;
                border-radius:7px;
                padding:6px 9px;
                font-size:11px;
                font-weight:700;
            }
            QLabel#footerText {
                color:#617387;
                font-size:11.5px;
                font-weight:650;
            }
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 16, 24, 14)
        root.setSpacing(12)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea{background:transparent;border:none;}")

        content = QWidget()
        content.setStyleSheet("background:transparent;")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 6)
        layout.setSpacing(12)

        # HERO
        hero = QFrame()
        hero.setObjectName("heroCard")
        hero.setMinimumHeight(235)
        hl = QHBoxLayout(hero)
        hl.setContentsMargins(25, 20, 22, 20)
        hl.setSpacing(18)

        logo = QLabel("TP")
        logo.setObjectName("logo")
        logo.setFixedSize(92, 92)
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet(
            "background-color:#1769D5;"
            "color:#FFFFFF;"
            "border:none;"
            "border-radius:30px;"
            "font-size:30px;"
            "font-weight:900;"
        )

        copy = QVBoxLayout()
        copy.setSpacing(4)

        badge = QLabel(f"OFFLINE • WINDOWS DESKTOP • {APP_DISPLAY_VERSION}")
        badge.setObjectName("badge")
        badge.setMaximumWidth(260)

        title = QLabel("TypingPro")
        title.setObjectName("heroTitle")

        sub = QLabel("Smart Typing Practice Suite")
        sub.setObjectName("heroSub")

        body = QLabel(
            "Professional English & Hindi typing practice software built for speed, accuracy, "
            "learning and competitive exam preparation. Your profiles, reports and preferences "
            "remain stored locally on your computer."
        )
        body.setObjectName("heroBody")
        body.setWordWrap(True)
        body.setMaximumWidth(590)

        copy.addWidget(badge)
        copy.addWidget(title)
        copy.addWidget(sub)
        copy.addWidget(body)
        copy.addStretch()

        art = DesktopIllustration()
        hl.addWidget(logo, 0, Qt.AlignVCenter)
        hl.addLayout(copy, 2)
        hl.addWidget(art, 1)
        layout.addWidget(hero)

        # PRODUCT INFO CARDS
        info_row = QHBoxLayout()
        info_row.setSpacing(10)

        for cap, value, sub_text, icon_text, bg, fg in [
            ("PRODUCT", "TypingPro", "Smart Typing Practice Suite", "◈", "#E8F1FF", "#1769D5"),
            ("VERSION", APP_DISPLAY_VERSION, "Stable desktop release", APP_DISPLAY_VERSION.lstrip("v"), "#E8F8EF", "#169457"),
            ("DEVELOPER", "Himanshu Vishwakarma", "Software Developer & Creator", "●", "#F0E9FF", "#673CC8"),
            ("PLATFORM", "Windows Desktop", "Offline 64-bit application", "▣", "#FFF0DD", "#D9780B"),
        ]:
            card = QFrame()
            card.setObjectName("infoCard")
            card.setMinimumHeight(92)
            cl = QHBoxLayout(card)
            cl.setContentsMargins(14, 12, 14, 12)
            cl.setSpacing(10)

            ic = QLabel(icon_text)
            ic.setFixedSize(46, 46)
            ic.setAlignment(Qt.AlignCenter)
            ic.setStyleSheet(
                f"background:{bg};color:{fg};border-radius:23px;"
                "font-size:16px;font-weight:800;"
            )

            box = QVBoxLayout()
            box.setSpacing(1)
            c = QLabel(cap); c.setObjectName("infoCaption")
            v = QLabel(value); v.setObjectName("infoValue")
            st = QLabel(sub_text); st.setObjectName("infoSub")
            st.setWordWrap(True)
            box.addWidget(c); box.addWidget(v); box.addWidget(st)
            cl.addWidget(ic); cl.addLayout(box, 1)
            info_row.addWidget(card, 1)

        layout.addLayout(info_row)

        sec = QLabel("Core Capabilities")
        sec.setObjectName("sectionTitle")
        layout.addWidget(sec)

        features = [
            ("⌨", "English & Hindi Typing", "Practice English and Hindi with built-in InScript keyboard support.", "#E8F1FF", "#1769D5"),
            ("✓", "Live Typing Feedback", "Character/word highlighting with correct, wrong and current feedback.", "#E8F8EF", "#169457"),
            ("◎", "Exam Mode", "Practice in an exam-style environment with qualification analysis.", "#F0E9FF", "#673CC8"),
            ("↗", "Detailed Reports", "Review WPM, accuracy, mistakes, result history and export reports.", "#FFF0DD", "#D9780B"),
            ("★", "Learning Module", "Guided English/Hindi lessons, keyboard guide, progress and stars.", "#FFEAF2", "#D83E78"),
            ("▣", "Offline & Private", "Works without internet and keeps user data stored locally.", "#E6F8F7", "#158F89"),
        ]

        grid = QGridLayout()
        grid.setHorizontalSpacing(11)
        grid.setVerticalSpacing(11)

        for i, (icon_text, heading, desc, bg, fg) in enumerate(features):
            card = QFrame()
            card.setObjectName("featureCard")
            card.setMinimumHeight(105)

            cl = QHBoxLayout(card)
            cl.setContentsMargins(15, 14, 15, 14)
            cl.setSpacing(12)

            ic = QLabel(icon_text)
            ic.setObjectName("featureIcon")
            ic.setAlignment(Qt.AlignCenter)
            ic.setStyleSheet(
                f"background:{bg};color:{fg};border-radius:24px;"
                "font-size:20px;font-weight:800;"
            )

            box = QVBoxLayout()
            box.setSpacing(3)
            h = QLabel(heading); h.setObjectName("featureTitle")
            d = QLabel(desc); d.setObjectName("featureText"); d.setWordWrap(True)
            box.addWidget(h); box.addWidget(d)
            cl.addWidget(ic); cl.addLayout(box, 1)
            grid.addWidget(card, i // 3, i % 3)

        layout.addLayout(grid)

        # EXAM STRIP
        exam = QFrame()
        exam.setObjectName("examCard")
        el = QVBoxLayout(exam)
        el.setContentsMargins(16, 13, 16, 14)
        el.setSpacing(8)

        eh = QLabel("Competitive Exam Ready")
        eh.setObjectName("examTitle")
        eb = QLabel(
            "Built for typing practice required in government and competitive examinations, "
            "with Practice Mode, Exam Mode and Custom Test."
        )
        eb.setObjectName("examText")
        eb.setWordWrap(True)
        el.addWidget(eh)
        el.addWidget(eb)

        tags = QHBoxLayout()
        tags.setSpacing(7)
        for text in ["UPP Computer Operator", "SSC CHSL", "LDC / JSA", "CCC", "DSSSB", "High Court", "CPCT", "Custom Test"]:
            tag = QLabel(text)
            tag.setObjectName("tag")
            tags.addWidget(tag)
        tags.addStretch()
        el.addLayout(tags)
        layout.addWidget(exam)

        footer = QHBoxLayout()
        f1 = QLabel("100% Offline  •  Fast & Lightweight  •  Secure & Private")
        f1.setObjectName("footerText")
        f2 = QLabel("© 2026 Himanshu Vishwakarma  •  TypingPro")
        f2.setObjectName("footerText")
        f2.setAlignment(Qt.AlignRight)
        footer.addWidget(f1, 1)
        footer.addWidget(f2, 1)
        layout.addLayout(footer)
        layout.addStretch()

        scroll.setWidget(content)
        root.addWidget(scroll)

