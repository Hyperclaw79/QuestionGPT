"""
Models related to OpenAI's API spec.
"""
from dataclasses import dataclass
from enum import StrEnum
from typing import Optional

from models.question_formats import Difficulty, QuestionTypes


class Roles(StrEnum):
    """
    An enumeration of message roles.
    """
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class Message:
    """
    Data class representing a message sent to ChatGPT.
    """
    role: Roles
    content: str


@dataclass
class UserInput:
    """Data class representing user input."""
    question_type: QuestionTypes = None
    difficulty: Difficulty = None
    topic: str = ""
    instructions: Optional[str] = ""

    def __post_init__(self):
        """Validate the user input."""
        validation_map = {
            "question_type": self._validate_qtype,
            "difficulty": self._validate_difficulty,
            "topic": self._validate_topic,
        }
        if invalid_fields := [
            field
            for field, validator in validation_map.items()
            if not validator()
        ]:
            raise ValueError(
                f"Invalid values for fields: {invalid_fields}"
            )

    def _validate_qtype(self):
        """Validate the question type."""
        try:
            QuestionTypes(self.question_type)
            return True
        except ValueError:
            return False

    def _validate_difficulty(self):
        """Validate the difficulty."""
        try:
            Difficulty(self.difficulty)
            return True
        except ValueError:
            return False

    def _validate_topic(self):
        """Validate the topic."""
        return bool(self.topic)
