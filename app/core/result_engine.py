class ResultEngine:

    def __init__(self):

        self.reset()

    # ==========================
    # Reset
    # ==========================

    def reset(self):

        self.gross_wpm = 0
        self.net_wpm = 0

        self.accuracy = 100

        self.correct_chars = 0
        self.wrong_chars = 0

        self.total_keystrokes = 0

        self.backspace = 0

        self.test_time = 0

    # ==========================
    # Generate Result
    # ==========================

    def generate(

        self,

        correct_chars,

        wrong_chars,

        elapsed_seconds,

        backspace_count

    ):

        self.correct_chars = correct_chars

        self.wrong_chars = wrong_chars

        self.backspace = backspace_count

        self.total_keystrokes = (

            correct_chars +

            wrong_chars +

            backspace_count

        )

        self.test_time = elapsed_seconds

        total_words = correct_chars / 5

        minutes = elapsed_seconds / 60

        if minutes <= 0:

            minutes = 1 / 60

        self.gross_wpm = round(

            total_words / minutes,

            2

        )

        penalty = wrong_chars / 5

        self.net_wpm = max(

            0,

            round(

                self.gross_wpm - penalty,

                2

            )

        )

        total = correct_chars + wrong_chars

        if total == 0:

            self.accuracy = 100

        else:

            self.accuracy = round(

                (correct_chars / total) * 100,

                2

            )

    # ==========================
    # Exam Qualification
    # ==========================

    def check_exam(self, exam_name):

        exams = {

            "UPP": {
                "wpm": 30,
                "accuracy": 95
            },

            "SSC": {
                "wpm": 35,
                "accuracy": 95
            },

            "CCC": {
                "wpm": 30,
                "accuracy": 90
            },

            "CPCT": {
                "wpm": 30,
                "accuracy": 95
            }

        }

        # ==========================
        # Custom Test
        # ==========================

        if exam_name not in exams:

            return {

                "status": "CUSTOM",

                "qualified": None,

                "message":
                    "Keep practicing and create your own target! 💪"

            }

        required = exams[exam_name]

        speed_ok = (
            self.net_wpm >= required["wpm"]
        )

        accuracy_ok = (
            self.accuracy >= required["accuracy"]
        )

        qualified = (
            speed_ok and accuracy_ok
        )

        # ==========================
        # Motivational Message
        # ==========================

        if qualified:

            message = (
                "🎉 Congratulations! "
                "You are Qualified! "
                "Your hard work is paying off. "
                "Keep practicing and aim even higher! 💪🏆"
            )

        else:

            if not speed_ok and not accuracy_ok:

                message = (
                    "💪 Not Qualified Yet. "
                    "Don't give up! Improve your typing speed "
                    "and accuracy step by step. "
                    "Every practice makes you better! 🔥"
                )

            elif not speed_ok:

                message = (
                    "💪 Not Qualified Yet. "
                    "Your accuracy is good, but you need to "
                    "increase your typing speed. "
                    "Keep practicing—you are getting closer! 🚀"
                )

            else:

                message = (
                    "💪 Not Qualified Yet. "
                    "Your speed is good, but improve your accuracy. "
                    "Accuracy first, speed will follow! 🎯"
                )

        return {

            "exam": exam_name,

            "required_wpm":
                required["wpm"],

            "required_accuracy":
                required["accuracy"],

            "your_wpm":
                self.net_wpm,

            "your_accuracy":
                self.accuracy,

            "qualified":
                qualified,

            "need_wpm":
                max(
                    0,
                    required["wpm"] - self.net_wpm
                ),

            "need_accuracy":
                round(
                    max(
                        0,
                        required["accuracy"] - self.accuracy
                    ),
                    2
                ),

            "message":
                message
        }