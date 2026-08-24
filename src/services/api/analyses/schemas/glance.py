from services.api.analyses.schemas.color import StatusColor, css_for_color
from services.api.common.schemas import CamelCaseModel


class GlanceBlock(CamelCaseModel):
    """Compact "glance" tiles; each colour code is chosen by the caller."""

    profile: str
    level: str
    level_color: StatusColor
    experience: str
    experience_color: StatusColor
    fintech: str
    fintech_color: StatusColor
    gaps: str
    gaps_color: StatusColor

    @property
    def level_status(self) -> str:
        """CSS class suffix for the level tile."""
        return css_for_color(self.level_color)

    @property
    def experience_status(self) -> str:
        """CSS class suffix for the experience tile."""
        return css_for_color(self.experience_color)

    @property
    def fintech_status(self) -> str:
        """CSS class suffix for the bank/fintech-experience tile."""
        return css_for_color(self.fintech_color)

    @property
    def gaps_status(self) -> str:
        """CSS class suffix for the career-breaks tile."""
        return css_for_color(self.gaps_color)
