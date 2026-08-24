from services.api.analyses.schemas.color import StatusColor, css_for_color
from services.api.common.schemas import CamelCaseModel


class Highlight(CamelCaseModel):
    """A key takeaway shown in the "Главное о кандидате" block."""

    text: str = ""
    color: StatusColor | None = None

    @property
    def status(self) -> str:
        """CSS class suffix for the highlight."""
        return css_for_color(self.color)


class Skill(CamelCaseModel):
    """A single skill chip (featured chips are rendered only when scored)."""

    name: str = ""
    group: str = ""
    color: StatusColor | None = None
    score: int = 0

    @property
    def status(self) -> str:
        """CSS class suffix for the skill chip."""
        return css_for_color(self.color)


class Risk(CamelCaseModel):
    """A risk / thing-to-check item."""

    title: str = ""
    explanation: str = ""
    color: StatusColor | None = StatusColor.ATTENTION

    @property
    def status(self) -> str:
        """CSS class suffix for the risk item."""
        return css_for_color(self.color)


class Unknown(CamelCaseModel):
    """A piece of missing information ("Нет данных: …")."""

    subject: str = ""
    reason: str = ""


class Question(CamelCaseModel):
    """A suggested interview question."""

    question: str = ""
    reason: str = ""
    color: StatusColor | None = None

    @property
    def status(self) -> str:
        """CSS class suffix for the question."""
        return css_for_color(self.color)
