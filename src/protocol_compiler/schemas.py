from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

# Enums

class Domain(str, Enum):
    STUDY = "study"
    FITNESS = "fitness"
    CODING = "coding"
    GENERAL = "general"


class TaskType(str, Enum):
    CONCEPTUAL = "conceptual_pass"
    PRACTICE = "practice"
    REVIEW = "review"
    TEST = "test"
    EXECUTE = "execute"


# Core schemas

class IntentFrame(BaseModel):
    """
    Canonical, validated representation of our user intent
    """

    objective: str = Field(
        ...,
        description="What the user is trying to achieve"
    )

    domain: Domain = Field(
        ...,
        description="High-level domain of the intent"
    )
    
    time_horizon_days: int = Field(
        ...,
        gt=0,
        description="Total number of days available"
    )

    starting_state: Optional[str] = Field(
        None,
        description="User's current capability or context"
    )

    constraints: List[str] = Field(
        default_factory=list,
        description="Hard constraints (time, energy, environment)"
    )

    success_definition: str = Field(
        ...,
        description="What success concretely looks like"
    )


class Task(BaseModel):
    """
    A single executable unit inside a protocol
    """

    type: TaskType = Field(
        ...,
        description="Type of task"
    )

    description: Optional[str] = Field(
        None,
        description="Human-readable description (optional)"
    )

    duration_min: Optional[int] = Field(
        None,
        gt=0,
        description="Time allocated (if applicable)"
    )

    count: Optional[int] = Field(
        None,
        gt=0,
        description="Repetition count (if applicable)"
    )

class ProtocolDay(BaseModel):
    """
    One day in the protocol timeline.
    """

    day: int = Field(
        ...,
        gt=0,
        description="Day index (1-based)"
    )

    focus: Optional[str] = Field(
        None,
        description="Primary focus of the day"
    )

    tasks: List[Task] = Field(
        ...,
        min_length=1
    )


class ProtocolPlan(BaseModel):
    """
    Fully structured execution protocol.
    """

    intent: IntentFrame = Field(
        ...,
        description="The intent this protocol was compiled from"
    )

    days: List[ProtocolDay] = Field(
        ...,
        min_length=1,
        description="Ordered list of protocol days"
    )