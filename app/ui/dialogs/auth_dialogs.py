from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from app.core.auth_manager import AuthManager
from app.core.session_manager import SessionManager


class ForgotPasswordDialog(QDialog):

    def __init__(
        self,
        parent=None,
        username=""
    ):
        super().__init__(parent)

        self.auth = AuthManager()

        self.setWindowTitle(
            "Forgot Password - TypingPro"
        )
        self.setFixedWidth(420)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            35, 30, 35, 30
        )
        layout.setSpacing(12)

        title = QLabel(
            "Reset Password"
        )
        title.setAlignment(
            Qt.AlignCenter
        )
        title.setFont(
            QFont(
                "Segoe UI",
                20,
                QFont.Bold
            )
        )

        info = QLabel(
            "Enter your username and offline Recovery PIN."
        )
        info.setWordWrap(True)
        info.setAlignment(
            Qt.AlignCenter
        )

        self.username = QLineEdit()
        self.username.setPlaceholderText(
            "Username"
        )
        self.username.setText(
            username
        )

        self.recovery_pin = QLineEdit()
        self.recovery_pin.setPlaceholderText(
            "Recovery PIN (4-6 digits)"
        )
        self.recovery_pin.setEchoMode(
            QLineEdit.Password
        )
        self.recovery_pin.setMaxLength(
            6
        )

        self.new_password = QLineEdit()
        self.new_password.setPlaceholderText(
            "New Password"
        )
        self.new_password.setEchoMode(
            QLineEdit.Password
        )

        self.confirm_password = QLineEdit()
        self.confirm_password.setPlaceholderText(
            "Confirm New Password"
        )
        self.confirm_password.setEchoMode(
            QLineEdit.Password
        )

        reset_btn = QPushButton(
            "Reset Password"
        )
        reset_btn.setMinimumHeight(
            42
        )

        cancel_btn = QPushButton(
            "Cancel"
        )
        cancel_btn.setMinimumHeight(
            38
        )

        layout.addWidget(title)
        layout.addWidget(info)
        layout.addSpacing(8)
        layout.addWidget(self.username)
        layout.addWidget(self.recovery_pin)
        layout.addWidget(self.new_password)
        layout.addWidget(self.confirm_password)
        layout.addWidget(reset_btn)
        layout.addWidget(cancel_btn)

        reset_btn.clicked.connect(
            self.reset_password
        )
        cancel_btn.clicked.connect(
            self.reject
        )
        self.confirm_password.returnPressed.connect(
            self.reset_password
        )

    def reset_password(self):

        if (
            self.new_password.text()
            != self.confirm_password.text()
        ):

            QMessageBox.warning(
                self,
                "Reset Failed",
                "New passwords do not match."
            )
            return

        ok, message = self.auth.reset_password(
            self.username.text(),
            self.recovery_pin.text(),
            self.new_password.text()
        )

        if not ok:

            QMessageBox.warning(
                self,
                "Reset Failed",
                message
            )
            return

        QMessageBox.information(
            self,
            "TypingPro",
            "Password reset successfully. "
            "You can now sign in with the new password."
        )

        self.accept()


class SignInDialog(QDialog):

    def __init__(
        self,
        parent=None
    ):
        super().__init__(parent)

        self.auth = AuthManager()

        self.setWindowTitle(
            "Sign In - TypingPro"
        )
        self.setFixedWidth(
            400
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            35, 30, 35, 30
        )
        layout.setSpacing(
            12
        )

        title = QLabel(
            "Sign In"
        )
        title.setAlignment(
            Qt.AlignCenter
        )
        title.setFont(
            QFont(
                "Segoe UI",
                20,
                QFont.Bold
            )
        )

        self.username = QLineEdit()
        self.username.setPlaceholderText(
            "Username"
        )

        self.password = QLineEdit()
        self.password.setPlaceholderText(
            "Password"
        )
        self.password.setEchoMode(
            QLineEdit.Password
        )

        button = QPushButton(
            "Sign In"
        )
        button.setMinimumHeight(
            42
        )

        forgot_btn = QPushButton(
            "Forgot Password?"
        )
        forgot_btn.setFlat(
            True
        )
        forgot_btn.setCursor(
            Qt.PointingHandCursor
        )

        layout.addWidget(title)
        layout.addSpacing(8)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(button)
        layout.addWidget(forgot_btn)

        button.clicked.connect(
            self.sign_in
        )
        forgot_btn.clicked.connect(
            self.open_forgot_password
        )
        self.password.returnPressed.connect(
            self.sign_in
        )

    def open_forgot_password(self):

        dialog = ForgotPasswordDialog(
            self,
            self.username.text()
        )

        dialog.exec()

    def sign_in(self):

        ok, user, message = self.auth.login(
            self.username.text(),
            self.password.text()
        )

        if not ok:

            QMessageBox.warning(
                self,
                "Sign In Failed",
                message
            )
            return

        SessionManager.login(
            user
        )

        self.accept()


class SignUpDialog(QDialog):

    def __init__(
        self,
        parent=None
    ):
        super().__init__(parent)

        self.auth = AuthManager()

        self.setWindowTitle(
            "Create Account - TypingPro"
        )
        self.setFixedWidth(
            420
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            35, 30, 35, 30
        )
        layout.setSpacing(
            12
        )

        title = QLabel(
            "Create Account"
        )
        title.setAlignment(
            Qt.AlignCenter
        )
        title.setFont(
            QFont(
                "Segoe UI",
                20,
                QFont.Bold
            )
        )

        recovery_info = QLabel(
            "Recovery PIN is used only for offline password reset. "
            "Remember it."
        )
        recovery_info.setWordWrap(
            True
        )

        self.name = QLineEdit()
        self.name.setPlaceholderText(
            "Full Name"
        )

        self.username = QLineEdit()
        self.username.setPlaceholderText(
            "Username"
        )

        self.password = QLineEdit()
        self.password.setPlaceholderText(
            "Password"
        )
        self.password.setEchoMode(
            QLineEdit.Password
        )

        self.confirm = QLineEdit()
        self.confirm.setPlaceholderText(
            "Confirm Password"
        )
        self.confirm.setEchoMode(
            QLineEdit.Password
        )

        self.recovery_pin = QLineEdit()
        self.recovery_pin.setPlaceholderText(
            "Recovery PIN (4-6 digits)"
        )
        self.recovery_pin.setEchoMode(
            QLineEdit.Password
        )
        self.recovery_pin.setMaxLength(
            6
        )

        self.confirm_pin = QLineEdit()
        self.confirm_pin.setPlaceholderText(
            "Confirm Recovery PIN"
        )
        self.confirm_pin.setEchoMode(
            QLineEdit.Password
        )
        self.confirm_pin.setMaxLength(
            6
        )

        button = QPushButton(
            "Sign Up"
        )
        button.setMinimumHeight(
            42
        )

        layout.addWidget(title)
        layout.addSpacing(8)
        layout.addWidget(self.name)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.confirm)
        layout.addWidget(recovery_info)
        layout.addWidget(self.recovery_pin)
        layout.addWidget(self.confirm_pin)
        layout.addWidget(button)

        button.clicked.connect(
            self.sign_up
        )

    def sign_up(self):

        if (
            self.password.text()
            != self.confirm.text()
        ):

            QMessageBox.warning(
                self,
                "Sign Up Failed",
                "Passwords do not match."
            )
            return

        pin = self.recovery_pin.text()

        if (
            pin
            != self.confirm_pin.text()
        ):

            QMessageBox.warning(
                self,
                "Sign Up Failed",
                "Recovery PINs do not match."
            )
            return

        if (
            not pin.isdigit()
            or not 4 <= len(pin) <= 6
        ):

            QMessageBox.warning(
                self,
                "Sign Up Failed",
                "Recovery PIN must be 4 to 6 digits."
            )
            return

        ok, result = self.auth.signup(
            self.name.text(),
            self.username.text(),
            self.password.text(),
            pin
        )

        if not ok:

            QMessageBox.warning(
                self,
                "Sign Up Failed",
                result
            )
            return

        # Account creation still signs the user in immediately.
        login_ok, user, message = self.auth.login(
            self.username.text(),
            self.password.text()
        )

        if not login_ok:

            QMessageBox.warning(
                self,
                "TypingPro",
                message
            )
            return

        SessionManager.login(
            user
        )

        QMessageBox.information(
            self,
            "TypingPro",
            "Account created successfully."
        )

        self.accept()
