# app/schemas/rule.py
# ──────────────────────────────────────────────
# Pydantic Schemas for Dynamic Scoring Rules
# ──────────────────────────────────────────────

from enum import Enum
from typing import Any, Optional, Union
from pydantic import BaseModel, Field, ConfigDict, field_validator


class RuleOperator(str, Enum):
    EACH = "each"                  # Multiplier / per-unit (e.g. kills * 2, solved * 10)
    EQUALS = "equals"              # Equal to (e.g. placement == 1, result == "WIN")
    EQ = "=="
    GREATER_THAN_OR_EQUAL = ">="
    LESS_THAN_OR_EQUAL = "<="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    NOT_EQUAL = "!="


class EventRuleBase(BaseModel):
    """Base shared fields for scoring rules."""
    metric: str = Field(
        ...,
        min_length=1,
        max_length=100,
        examples=["kills", "placement", "result", "problems_solved"],
        description="The metric name found in player results to evaluate.",
    )
    condition: Optional[str] = Field(
        default=None,
        max_length=255,
        examples=["Each kill awards +2 points", "1st place awards +10 points"],
        description="Human-readable explanation of this scoring rule.",
    )
    operator: str = Field(
        ...,
        examples=["each", "equals", ">=", "<=", "==", "!="],
        description="Comparison or aggregation operator: 'each', 'equals', '==', '>=', '<=', '>', '<', '!='",
    )
    value: Optional[str] = Field(
        default=None,
        max_length=100,
        examples=["1", "WIN", "10", None],
        description="Threshold or categorical value to match against (optional for 'each').",
    )
    points: float = Field(
        ...,
        examples=[2.0, 10.0, -2.0],
        description="Points to award or deduct (can be positive bonus or negative penalty).",
    )
    priority: int = Field(
        default=0,
        examples=[0, 1, 2],
        description="Priority order for rule evaluation.",
    )

    @field_validator("value", mode="before")
    @classmethod
    def convert_value_to_str(cls, v: Any) -> Optional[str]:
        if v is None:
            return None
        return str(v).strip()

    @field_validator("metric", "operator", mode="before")
    @classmethod
    def clean_strings(cls, v: Any) -> str:
        if isinstance(v, str):
            return v.strip().lower()
        return str(v)


class EventRuleCreate(EventRuleBase):
    """Payload for creating a new scoring rule on an event."""
    pass


class EventRuleUpdate(BaseModel):
    """Payload for updating an existing scoring rule."""
    metric: Optional[str] = Field(default=None, min_length=1, max_length=100)
    condition: Optional[str] = Field(default=None, max_length=255)
    operator: Optional[str] = None
    value: Optional[str] = None
    points: Optional[float] = None
    priority: Optional[int] = None

    @field_validator("value", mode="before")
    @classmethod
    def convert_value_to_str(cls, v: Any) -> Optional[str]:
        if v is None:
            return None
        return str(v).strip()

    @field_validator("metric", "operator", mode="before")
    @classmethod
    def clean_strings(cls, v: Any) -> Optional[str]:
        if isinstance(v, str):
            return v.strip().lower()
        return v


class EventRuleResponse(BaseModel):
    """Response representation of an event scoring rule."""
    id: int
    event_id: int
    metric: str
    condition: Optional[str] = None
    operator: str
    value: Optional[str] = None
    points: float
    priority: int

    model_config = ConfigDict(from_attributes=True)
