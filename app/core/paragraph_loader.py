import random
from pathlib import Path

from app.core.app_paths import resource_path

class ParagraphLoader:

    # ==========================
    # Base Folder
    # ==========================
    BASE_FOLDER = resource_path("assets", "paragraphs")
    # ==========================
    # Last Selected Paragraph
    # ==========================

    _last_index = -1
    current_index = 0
    total_paragraphs = 0
    @classmethod
    def get_file(
        cls,
        language="english",
        category="easy"
    ):

        return (
            cls.BASE_FOLDER
            / language
            / f"{category}.txt"
        )
    @classmethod
    def get_paragraph(cls, language="english", level="easy"):

        file_path = cls.get_file(
        language,
        level
        )
        print("Looking for:", file_path)
        print("Exists:", file_path.exists())
        print("Current Working Dir:", Path.cwd())

        if not file_path.exists():
            return "Paragraph file not found."

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

        paragraphs = [

            p.strip()

            for p in content.split("===")

            if p.strip()

        ]

        if not paragraphs:
            return "No paragraph available."

        if len(paragraphs) == 1:
            return paragraphs[0]

        available_indexes = [

            i

            for i in range(len(paragraphs))

            if i != cls._last_index

        ]

        selected = random.choice(available_indexes)

        cls._last_index = selected

        cls.current_index = selected + 1

        cls.total_paragraphs = len(paragraphs)

        return paragraphs[selected]

    @classmethod
    def paragraph_info(cls):

        return (

            cls.current_index,

            cls.total_paragraphs

        )