import time


class TypingStatistics:

    def __init__(self):
        self.reset()

    # ==========================
    # Reset
    # ==========================

    def reset(self):

        self.start_time = None
        self.end_time = None

        self.correct_chars = 0
        self.wrong_chars = 0

    # ==========================
    # Start Test
    # ==========================

    def start(self):

        if self.start_time is None:
            self.start_time = time.time()

    # ==========================
    # Stop Test
    # ==========================

    def stop(self):

        if self.end_time is None:
            self.end_time = time.time()

    # ==========================
    # Update Statistics
    # ==========================

    def update(self, correct_chars, wrong_chars):

        self.correct_chars = correct_chars
        self.wrong_chars = wrong_chars

    # ==========================
    # Elapsed Time
    # ==========================

    def elapsed_seconds(self):

        if self.start_time is None:
            return 0

        if self.end_time is None:
            return max(1, int(time.time() - self.start_time))

        return max(1, int(self.end_time - self.start_time))

    # ==========================
    # Accuracy
    # ==========================

    def accuracy(self):

        total = self.correct_chars + self.wrong_chars

        if total == 0:
            return 100.0

        return round(
            (self.correct_chars / total) * 100,
            2
        )

    # ==========================
    # Gross WPM
    # ==========================

    def gross_wpm(self):

        minutes = self.elapsed_seconds() / 60

        if minutes <= 0:
            return 0

        total_typed = self.correct_chars + self.wrong_chars

        return round((total_typed / 5) / minutes)

    # ==========================
    # Net WPM
    # ==========================

    def net_wpm(self):

        minutes = self.elapsed_seconds() / 60

        if minutes <= 0:
            return 0

        net_chars = max(
            0,
            self.correct_chars - self.wrong_chars
        )

        return round((net_chars / 5) / minutes)

    # ==========================
    # Current WPM
    # ==========================

    def wpm(self):

        return self.net_wpm()

    # ==========================
    # CPM
    # ==========================

    def cpm(self):

        minutes = self.elapsed_seconds() / 60

        if minutes <= 0:
            return 0

        return round(self.correct_chars / minutes)

    # ==========================
    # Mistakes
    # ==========================

    def mistakes(self):

        return self.wrong_chars