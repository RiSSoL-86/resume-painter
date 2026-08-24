from datetime import datetime

from services.api.analyses.schemas.color import StatusColor, css_for_color
from services.api.common.schemas import CamelCaseModel


class CandidateBlock(CamelCaseModel):
    """Top block (cockpit): overall verdict and candidate identity."""

    full_name: str
    headline: str
    overall_score: int
    overall_color: StatusColor
    age: str = "—"
    salary: str = "—"
    updated: datetime
    updated_color: StatusColor

    @property
    def overall_status(self) -> str:
        """CSS class suffix for the gauge."""
        return css_for_color(self.overall_color)

    @property
    def updated_status(self) -> str:
        """CSS class suffix for the "last updated" tag."""
        return css_for_color(self.updated_color)
