class ExamAnalyzer:

    def __init__(self):

        self.exams = {

            # ==========================
            # Uttar Pradesh
            # ==========================

            "UPP Computer Operator": {
                "min_wpm": 30,
                "min_accuracy": 95
            },

            # ==========================
            # SSC
            # ==========================

            "SSC CHSL LDC/JSA": {
                "min_wpm": 35,
                "min_accuracy": 95
            },

            # ==========================
            # Delhi High Court
            # ==========================

            "Delhi High Court Restorer": {
                "min_wpm": 35,
                "min_accuracy": 0
            },

            # ==========================
            # Allahabad High Court
            # ==========================

            "Allahabad High Court JA": {
                "min_wpm": 30,
                "min_accuracy": 0
            },

            # ==========================
            # DSSSB
            # ==========================

            "DSSSB Typing": {
                "min_wpm": 30,
                "min_accuracy": 0
            },

            # ==========================
            # CCC
            # ==========================

            "CCC": {
                "min_wpm": 30,
                "min_accuracy": 90
            },

            # ==========================
            # CPCT
            # ==========================

            "CPCT": {
                "min_wpm": 30,
                "min_accuracy": 95
            },

            # ==========================
            # Custom
            # ==========================

            "Custom": {
                "min_wpm": 0,
                "min_accuracy": 0
            }

        }

    # =====================================
    # Get Exam List
    # =====================================

    def exam_names(self):

        return list(self.exams.keys())

    # =====================================
    # Analyze Result
    # =====================================

    def analyze(

        self,

        exam_name,

        net_wpm,

        accuracy

    ):

        if exam_name not in self.exams:

            return {

                "status": False,

                "message": "Unknown Exam"

            }

        exam = self.exams[exam_name]

        required_wpm = exam["min_wpm"]

        required_accuracy = exam["min_accuracy"]

        # ==========================
        # Speed Check
        # ==========================

        speed_ok = (
            net_wpm >= required_wpm
        )

        # ==========================
        # Accuracy Check
        # ==========================

        if required_accuracy == 0:

            accuracy_ok = True

        else:

            accuracy_ok = (
                accuracy >= required_accuracy
            )

        # ==========================
        # Final Qualification
        # ==========================

        qualified = (
            speed_ok and accuracy_ok
        )

        # ==========================
        # Remaining Requirement
        # ==========================

        need_wpm = max(

            0,

            round(
                required_wpm - net_wpm,
                2
            )

        )

        if required_accuracy == 0:

            need_accuracy = 0

        else:

            need_accuracy = max(

                0,

                round(
                    required_accuracy - accuracy,
                    2
                )

            )

        # ==========================
        # Recommendation
        # ==========================

        if qualified:

            recommendation = (

                "Excellent! You are ready "
                "for this typing requirement. "
                "Keep practicing to improve "
                "your speed even further."

            )

        elif not speed_ok and not accuracy_ok:

            recommendation = (

                "Not qualified yet. "
                "Focus on improving both "
                "typing speed and accuracy. "
                "Keep practicing every day!"

            )

        elif not speed_ok:

            recommendation = (

                "Your accuracy is good, "
                "but you need more typing speed. "
                "Keep practicing—you are getting closer!"

            )

        else:

            recommendation = (

                "Your typing speed is good. "
                "Improve your accuracy and "
                "you can reach the target!"

            )

        return {

            "status": True,

            "exam": exam_name,

            "qualified": qualified,

            "required_wpm": required_wpm,

            "required_accuracy": required_accuracy,

            "your_wpm": round(
                net_wpm,
                2
            ),

            "your_accuracy": round(
                accuracy,
                2
            ),

            "need_wpm": need_wpm,

            "need_accuracy": need_accuracy,

            "recommendation":
                recommendation

        }

    # =====================================
    # Grade
    # =====================================

    def grade(

        self,

        accuracy

    ):

        if accuracy >= 98:

            return "S+"

        if accuracy >= 95:

            return "A+"

        if accuracy >= 90:

            return "A"

        if accuracy >= 80:

            return "B"

        if accuracy >= 70:

            return "C"

        return "D"

    # =====================================
    # Readiness %
    # =====================================

    def readiness(

        self,

        exam_name,

        net_wpm,

        accuracy

    ):

        if exam_name not in self.exams:

            return 0

        exam = self.exams[exam_name]

        # ==========================
        # Speed Score
        # ==========================

        if exam["min_wpm"]:

            speed_score = min(

                100,

                (
                    net_wpm
                    /
                    exam["min_wpm"]
                ) * 100

            )

        else:

            speed_score = 100

        # ==========================
        # Accuracy Score
        # ==========================

        if exam["min_accuracy"]:

            accuracy_score = min(

                100,

                (
                    accuracy
                    /
                    exam["min_accuracy"]
                ) * 100

            )

        else:

            accuracy_score = 100

        return round(

            (
                speed_score
                +
                accuracy_score
            ) / 2,

            2

        )