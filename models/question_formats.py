"""This module contains the data classes for the different question formats."""

# pylint: disable=too-few-public-methods

from dataclasses import dataclass, field
from enum import StrEnum
import random
from typing import Optional


class QuestionTypes(StrEnum):
    """Enumeration of question types."""
    MCQ = 'mcq'
    FILL = 'fill'
    MULTI_SELECT = 'multi_select'


class Difficulty(StrEnum):
    """Enumeration of question difficulties."""
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'


@dataclass
class ScoringRules:
    """Data class representing the scoring rules."""
    #: The points awarded for answering the question correctly
    points: Optional[int] = 0
    #: The points deducted for answering the question incorrectly
    negative_points: Optional[int] = 0
    #: The time limit for answering the question
    allowed_duration_secs: Optional[int] = 60
    #: Whether the question can be skipped
    skippable: Optional[bool] = False
    #: End the quiz if the question is answered incorrectly
    instant_fail: Optional[bool] = False
    #: Allow approximately correct answers
    allow_approximate: Optional[bool] = False


@dataclass
class Analytics:
    """Data class representing the analytics for a question."""
    #: The number of times the question was answered correctly
    num_correct: Optional[int] = 0
    #: The number of times the question was answered incorrectly
    num_incorrect: Optional[int] = 0
    #: The number of times the question was skipped
    num_skipped: Optional[int] = 0


@dataclass
class Question:
    """Data class representing a question."""
    #: The category of the question
    category: QuestionTypes
    #: The difficulty of the question
    difficulty: Difficulty
    #: The topic of the question
    topic: str
    #: The question statement
    statement: str
    #: The scoring scheme for the question
    scoring_rules: ScoringRules
    #: The analytics for the question
    analytics: Analytics


@dataclass
class ChoiceMixin:
    """Mixin for questions with choices."""
    solution: list[str] = field(default_factory=list)
    choices: list[str] = field(default_factory=list)
    num_selectable: Optional[int] = 1

    def post_init(self):
        """Shuffle the choices."""
        random.shuffle(self.choices)


@dataclass
class FillInTheBlanks(Question):
    """Fill in the blanks question."""
    solution: str
    category = QuestionTypes.FILL



@dataclass
class MultiSelect(ChoiceMixin, Question):
    """Multiple Selections question."""
    category = QuestionTypes.MULTI_SELECT


@dataclass
class MCQ(ChoiceMixin, Question):
    """Multiple choice question with single selectable answer."""
    category = QuestionTypes.MCQ
    def __post_init__(self):
        # Number of selectable choices is always 1.
        self.num_selectable = 1


QT_MAPPING = {
    QuestionTypes.MCQ: MCQ,
    QuestionTypes.FILL: FillInTheBlanks,
    QuestionTypes.MULTI_SELECT: MultiSelect,
}
