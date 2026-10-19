from PySide6.QtCore import QObject, QTimer, Signal


class TypingTimer(QObject):

    # Signals
    time_changed = Signal(int)
    finished = Signal()

    def __init__(self):
        super().__init__()

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)

        self.remaining_seconds = 0
        self.is_running = False

    # ==========================
    # Start Timer
    # ==========================

    def start(self, minutes):

        # अगर पहले से चल रहा है
        if self.is_running:
            return

        self.remaining_seconds = minutes * 60

        self.is_running = True

        self.time_changed.emit(self.remaining_seconds)

        self.timer.start(1000)

    # ==========================
    # Every Second
    # ==========================

    def tick(self):

        self.remaining_seconds -= 1

        self.time_changed.emit(self.remaining_seconds)

        if self.remaining_seconds <= 0:

            self.stop()

            self.finished.emit()

    # ==========================
    # Stop Timer
    # ==========================

    def stop(self):

        self.timer.stop()

        self.is_running = False

    # ==========================
    # Reset Timer
    # ==========================

    def reset(self, minutes):

        self.stop()

        self.remaining_seconds = minutes * 60

        self.time_changed.emit(self.remaining_seconds)