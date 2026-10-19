from PySide6.QtGui import (
    QTextCursor,
    QTextCharFormat,
    QColor,
    QTextDocument
)


class HighlightEngine:

    def __init__(self):

        # ==========================
        # Character Colors
        # ==========================

        self.correct_color = QColor("#2ECC71")   # Green

        self.wrong_color = QColor("#E74C3C")     # Red

        self.current_color = QColor("#F1C40F")   # Yellow

        self.pending_color = QColor("#000000")   # Black

        # ==========================
        # Character Formats
        # ==========================

        self.correct_format = QTextCharFormat()
        self.correct_format.setForeground(
        self.correct_color
        )

        self.wrong_format = QTextCharFormat()
        self.wrong_format.setForeground(
        self.wrong_color
        )

        self.current_format = QTextCharFormat()
        self.current_format.setForeground(
        self.current_color
        )

        self.pending_format = QTextCharFormat()
        self.pending_format.setForeground(
        self.pending_color
        )

    # ==========================
    # Get Words
    # ==========================

    def get_words(

        self,

        text

    ):

        return text.split()

    # ==========================
    # Analyze Words
    # ==========================

    def analyze_words(

        self,

        original_text,

        typed_text

    ):

        original_words = self.get_words(
            original_text
        )

        typed_words = self.get_words(
            typed_text
        )

        result = []

        for index, original_word in enumerate(
            original_words
        ):

            if index >= len(typed_words):

                result.append(
                    ("pending", original_word)
                )

            elif typed_words[index] == original_word:

                result.append(
                    ("correct", original_word)
                )

            else:

                result.append(
                    ("wrong", original_word)
                )

        return result

   
    # ==========================
    # Word Highlight
    # ==========================

    def highlight_words(
        self,
        editor,
        original_text,
        typed_text,
        show_correct=True,
        show_wrong=True,
        show_current=True
    ):
        """
        Word Mode with SPACE-as-submit behavior.

        Rules:
        - current unfinished word = yellow
        - correct word + SPACE = green
        - wrong/incomplete word + SPACE = red
        - SPACE without typing anything = skipped word = red
        - every SPACE advances exactly one original word
        - extra repeated spaces therefore skip words one-by-one
        - pending words remain black

        Character Mode is untouched.
        """

        # -------------------------------------------------
        # Original word spans
        # -------------------------------------------------
        original_spans = []
        i = 0
        text_len = len(original_text)

        while i < text_len:

            while (
                i < text_len
                and original_text[i].isspace()
            ):
                i += 1

            if i >= text_len:
                break

            start_pos = i

            while (
                i < text_len
                and not original_text[i].isspace()
            ):
                i += 1

            original_spans.append(
                (
                    start_pos,
                    i,
                    original_text[start_pos:i]
                )
            )

        # -------------------------------------------------
        # Parse typed text preserving EMPTY submissions.
        #
        # Example:
        # "computer "  -> ["computer", ""]
        # " "          -> ["", ""]
        # "  "         -> ["", "", ""]
        #
        # Each separator SPACE finalizes exactly one word.
        # -------------------------------------------------
        normalized_typed = typed_text.replace(
            "\n",
            " "
        ).replace(
            "\t",
            " "
        )

        parts = normalized_typed.split(" ")

        typed_ends_with_space = (
            len(normalized_typed) > 0
            and normalized_typed.endswith(" ")
        )

        # Number of finalized/submitted words is exactly
        # the number of typed SPACE separators.
        completed_count = (
            len(parts) - 1
        )

        completed_count = min(
            completed_count,
            len(original_spans)
        )

        # Current unfinished token:
        current_typed_word = (
            ""
            if typed_ends_with_space
            else parts[-1]
        )

        selections = []

        # Clear stale Character-Mode document colors once per Word refresh.
        # This is a single full-range formatting operation, not per-character.
        # After this, Word colors are drawn with ExtraSelections and checkbox
        # states work normally.
        reset_cursor = editor.textCursor()
        reset_cursor.beginEditBlock()
        reset_cursor.select(QTextCursor.Document)
        reset_cursor.setCharFormat(
            self.pending_format
        )
        reset_cursor.endEditBlock()


        def add_selection(
            start_pos,
            end_pos,
            char_format
        ):

            if start_pos >= end_pos:
                return

            selection = editor.ExtraSelection()
            sel_cursor = editor.textCursor()

            sel_cursor.setPosition(
                start_pos
            )

            sel_cursor.setPosition(
                end_pos,
                QTextCursor.KeepAnchor
            )

            selection.cursor = sel_cursor
            selection.format = char_format

            selections.append(
                selection
            )

        # -------------------------------------------------
        # Completed/submitted words
        # -------------------------------------------------
        for word_index in range(
            completed_count
        ):

            start_pos, end_pos, original_word = (
                original_spans[
                    word_index
                ]
            )

            typed_word = (
                parts[word_index]
                if word_index < len(parts)
                else ""
            )

            # Empty word submitted by pressing SPACE directly
            # is a skipped word -> RED.
            if (
                typed_word
                and typed_word == original_word
            ):
                if show_correct:
                    add_selection(
                        start_pos,
                        end_pos,
                        self.correct_format
                    )
            else:
                if show_wrong:
                    add_selection(
                        start_pos,
                        end_pos,
                        self.wrong_format
                    )

        # -------------------------------------------------
        # Current word
        # -------------------------------------------------
        current_index = completed_count

        if current_index < len(
            original_spans
        ):

            start_pos, end_pos, original_word = (
                original_spans[
                    current_index
                ]
            )

            # Current word is yellow only when Yellow is enabled.
            if show_current:
                add_selection(
                    start_pos,
                    end_pos,
                    self.current_format
                )

        # Pending words are left untouched/black.
        editor.setExtraSelections(
            selections
        )

        editor.viewport().update()
    # ==========================
    # Highlight Method
    # ==========================


    def highlight(

        self,

        editor,

        original_text,

        typed_text,

        show_correct=True,

        show_wrong=True,

        show_current=True

    ):
        """
        Same positional highlighting rule as the working version,
        but formats consecutive runs instead of every single character.

        No resync, no word splitting, no SequenceMatcher.
        """

        cursor_position = editor.textCursor().position()
        scroll_value = editor.verticalScrollBar().value()
        cursor = editor.textCursor()

        editor.setUpdatesEnabled(False)
        cursor.beginEditBlock()

        # Same reset behavior as the working version.
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(
            self.pending_format
        )

        length = min(
            len(original_text),
            len(typed_text)
        )

        # Instead of setCharFormat once PER CHARACTER,
        # group consecutive characters with the same result.
        i = 0

        while i < length:

            is_correct = (
                original_text[i]
                == typed_text[i]
            )

            start_pos = i
            i += 1

            while (
                i < length
                and (
                    original_text[i]
                    == typed_text[i]
                ) == is_correct
            ):
                i += 1

            if (
                is_correct
                and not show_correct
            ):
                continue

            if (
                not is_correct
                and not show_wrong
            ):
                continue

            cursor.setPosition(
                start_pos
            )

            cursor.setPosition(
                i,
                QTextCursor.KeepAnchor
            )

            cursor.setCharFormat(
                self.correct_format
                if is_correct
                else self.wrong_format
            )

        # Same current-character rule as the working version.
        if (
            show_current
            and len(typed_text) < len(original_text)
        ):

            cursor.setPosition(
                len(typed_text)
            )

            cursor.movePosition(
                QTextCursor.NextCharacter,
                QTextCursor.KeepAnchor
            )

            cursor.setCharFormat(
                self.current_format
            )

        cursor.endEditBlock()

        # Restore paragraph cursor and scroll.
        cursor = editor.textCursor()

        document_length = max(
            0,
            editor.document().characterCount() - 1
        )

        safe_cursor_position = min(
            cursor_position,
            document_length
        )

        cursor.setPosition(
            safe_cursor_position
        )

        editor.setTextCursor(
            cursor
        )

        editor.verticalScrollBar().setValue(
            scroll_value
        )

        editor.setUpdatesEnabled(True)
        editor.viewport().update()
