from enum import IntEnum
from typing import final

from services.api.common.schemas import CamelCaseModel


@final
class StatusColor(IntEnum):
    """Colour code sent by the caller (maps to a ``status-*`` class)."""

    POSITIVE = 1
    ATTENTION = 2
    NEGATIVE = 3
    NEUTRAL = 4
    UNKNOWN = 5


# code -> CSS ``status-*`` suffix used in the template.
CSS: dict[StatusColor, str] = {
    StatusColor.POSITIVE: "positive",
    StatusColor.ATTENTION: "attention",
    StatusColor.NEGATIVE: "negative",
    StatusColor.NEUTRAL: "neutral",
    StatusColor.UNKNOWN: "unknown",
}


def css_for_color(color: StatusColor | None) -> str:
    """Map a colour code to its CSS suffix (``neutral`` if unset)."""
    if color is None:
        return CSS[StatusColor.NEUTRAL]
    return CSS[StatusColor(color)]


@final
class ColorsResponse(CamelCaseModel):
    """Colour codes callers put next to values in the payload."""

    positive: int = StatusColor.POSITIVE
    attention: int = StatusColor.ATTENTION
    negative: int = StatusColor.NEGATIVE
    neutral: int = StatusColor.NEUTRAL
    unknown: int = StatusColor.UNKNOWN
