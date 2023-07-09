"""
Models related to OpenAI's API spec.
"""
from dataclasses import dataclass
from enum import StrEnum

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
    category: QuestionTypes
    difficulty: Difficulty
    topic: str
