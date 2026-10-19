class TypingEngine:

    CORRECT = 1
    WRONG = 2
    CURRENT = 3
    PENDING = 0

    def __init__(self):
        self.reset()

    def reset(self):

        self.original_text = ""

        self.typed_text = ""

        self.states = []

        self.correct_chars = 0
        self.wrong_chars = 0
        self.extra_chars = 0
        

    # ==========================
    # Main Check
    # ==========================

    def check(self, original_text, typed_text):

        self.original_text = original_text
        self.typed_text = typed_text

        self.correct_chars = 0
        self.wrong_chars = 0
        self.extra_chars = 0

        self.states = []

        original_len = len(original_text)
        typed_len = len(typed_text)

        # Character Compare
        for i in range(original_len):

            if i < typed_len:

                if typed_text[i] == original_text[i]:

                    self.states.append(self.CORRECT)
                    self.correct_chars += 1

                else:

                    self.states.append(self.WRONG)
                    self.wrong_chars += 1

            else:

                if i == typed_len:

                    self.states.append(self.CURRENT)

                else:

                    self.states.append(self.PENDING)

        # Extra Characters
        if typed_len > original_len:

            self.extra_chars = typed_len - original_len

            self.wrong_chars += self.extra_chars

    # ==========================
    # Information
    # ==========================

    def total_chars(self):

        return len(self.typed_text)

    def accuracy(self):

        total = self.correct_chars + self.wrong_chars

        if total == 0:
            return 100.0

        return round(
            (self.correct_chars / total) * 100,
            2
        )

    def mistakes(self):

        return self.wrong_chars

    def current_index(self):

        return len(self.typed_text)

    def is_finished(self):

        return len(self.typed_text) >= len(self.original_text)