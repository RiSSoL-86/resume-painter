from datetime import datetime
from typing import TypedDict

from pydantic import Field

from services.api.analyses.brand import company_icon
from services.api.analyses.schemas.color import StatusColor, css_for_color
from services.api.analyses.schemas.lifeline.constants import (
    MIN_BREAK_MONTHS,
    MIN_COURSE_PX,
    MIN_STUDY_PX,
    MIN_WORK_MONTHS,
    PER_BULLET_PX,
    PX_PER_MONTH,
    WORK_GAP_PX,
)
from services.api.analyses.schemas.lifeline.utils import (
    duration_label,
    months_between,
    now_like,
    span_months,
)
from services.api.common.schemas import CamelCaseModel


class WorkCheck(CamelCaseModel):
    """A named, colour-coded tag scored by the caller for a work place."""

    name: str
    name_color: StatusColor | None = None

    @property
    def status(self) -> str:
        """CSS class suffix for the check chip."""
        return css_for_color(self.name_color)


class WorkItem(CamelCaseModel):
    """A work-experience entry; duration and colour are derived here."""

    company: str
    company_color: StatusColor | None = None
    label: str
    position: str
    start_date: datetime
    end_date: datetime | None = None
    bullets: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)
    checks: list[WorkCheck] = Field(default_factory=list)

    @property
    def resolved_end(self) -> datetime:
        """End date, or now for the current (still-ongoing) job."""
        return self.end_date or now_like(self.start_date)

    def _months(self) -> int:
        return months_between(self.start_date, self.resolved_end)

    @property
    def duration_label(self) -> str:
        """Human-readable tenure computed from the dates."""
        return duration_label(self._months())

    @property
    def visible_bullets(self) -> list[str]:
        """Bullets by tenure: 0 under 1y, 2 from 1y, +1 per extra 6mo."""
        months = self._months()
        if months < 12:
            return []
        count = 2 + (months - 12) // 6
        return self.bullets[:count]

    @property
    def logo_url(self) -> str | None:
        """Company icon from the brand registry, by label then name."""
        return company_icon(self.label) or company_icon(self.company)

    @property
    def status(self) -> str:
        """Card colour — sent by the caller in ``companyColor``."""
        return css_for_color(self.company_color)


class EducationItem(CamelCaseModel):
    """An education entry; only the end date is known (start is unknown)."""

    end_date: datetime
    institution: str
    specialty: str

    @property
    def kind(self) -> str:
        """Timeline category discriminator for the template."""
        return "study"


class CourseItem(CamelCaseModel):
    """A course entry; only the end date is known (start is unknown)."""

    end_date: datetime
    name: str
    specialty: str

    @property
    def kind(self) -> str:
        """Timeline category discriminator for the template."""
        return "course"


class BreakItem(CamelCaseModel):
    """A career break; only the bounds are sent, duration is derived."""

    start_date: datetime
    end_date: datetime

    @property
    def kind(self) -> str:
        """Timeline category discriminator for the template."""
        return "gap"

    @property
    def duration_label(self) -> str:
        """Human-readable break length computed from the dates."""
        return duration_label(months_between(self.start_date, self.end_date))


type BackgroundItem = EducationItem | CourseItem | BreakItem


class BackgroundBlock(CamelCaseModel):
    """Education, courses and career breaks (the non-work timeline)."""

    education: list[EducationItem] = Field(default_factory=list)
    courses: list[CourseItem] = Field(default_factory=list)
    breaks: list[BreakItem] = Field(default_factory=list)

    @property
    def timeline(self) -> list[BackgroundItem]:
        """All entries merged and sorted newest-first (like work)."""
        items: list[BackgroundItem] = [
            *self.education,
            *self.courses,
            *self.breaks,
        ]
        return sorted(items, key=lambda item: item.end_date, reverse=True)


class WorkPlacement(TypedDict):
    """A work card with its position on the shared time axis."""

    work: WorkItem
    top: int
    height: int


class BackgroundPlacement(TypedDict):
    """A study/course/break card placed on the shared time axis."""

    item: BackgroundItem
    top: int
    height: int


class LifelineLayout(TypedDict):
    """Both columns laid out on one time→pixel scale (newest on top)."""

    stage_height: int
    work: list[WorkPlacement]
    background: list[BackgroundPlacement]


class LifelineBlock(CamelCaseModel):
    """Career timeline: work places plus study/courses/breaks."""

    work: list[WorkItem] = Field(default_factory=list)
    background: BackgroundBlock = Field(default_factory=BackgroundBlock)

    @property
    def layout(self) -> LifelineLayout:
        """Stack work cards; gaps are the real months between jobs × scale."""
        background = self.background.timeline
        order = sorted(self.work, key=lambda w: w.resolved_end, reverse=True)
        ends = [w.resolved_end for w in self.work]
        ends += [item.end_date for item in background]
        if not ends:
            return {"stage_height": 0, "work": [], "background": []}
        newest = max(ends)
        scale = PX_PER_MONTH
        work_floor = round(MIN_WORK_MONTHS * scale)
        break_floor = round(MIN_BREAK_MONTHS * scale)

        work: list[WorkPlacement] = []
        top = 0
        for i, w in enumerate(order):
            span = span_months(w.start_date, w.resolved_end)
            floor = work_floor + round(len(w.visible_bullets) * PER_BULLET_PX)
            height = max(round(span * scale), floor)
            work.append({"work": w, "top": top, "height": height})
            top += height
            if i + 1 < len(order):
                nxt = order[i + 1]
                gap = span_months(nxt.resolved_end, w.start_date)
                top += max(round(gap * scale), WORK_GAP_PX)

        # date→pixel map anchored on the work cards (end→top, start→bottom)
        anchors: list[tuple[float, int]] = []
        for p in work:
            anchors.append(
                (span_months(p["work"].resolved_end, newest), p["top"])
            )
            anchors.append(
                (
                    span_months(p["work"].start_date, newest),
                    p["top"] + p["height"],
                )
            )
        anchors.sort()

        def px_at(moment: datetime) -> int:
            """Pixel for a date, interpolated between the work anchors."""
            age = span_months(moment, newest)
            if not anchors:
                return round(age * scale)
            if age <= anchors[0][0]:
                a0, p0 = anchors[0]
                return round(p0 - (a0 - age) * scale)
            if age >= anchors[-1][0]:
                a1, p1 = anchors[-1]
                return round(p1 + (age - a1) * scale)
            for (a0, p0), (a1, p1) in zip(anchors, anchors[1:], strict=False):
                if a0 <= age <= a1:
                    if a1 == a0:
                        return p0
                    return round(p0 + (age - a0) / (a1 - a0) * (p1 - p0))
            return round(age * scale)

        def break_center(brk: BreakItem) -> float | None:
            """Seam midpoint between the jobs the break sits between."""
            below_idx = next(
                (
                    i
                    for i, p in enumerate(work)
                    if p["work"].resolved_end <= brk.start_date
                ),
                None,
            )
            if below_idx is None:
                return None
            below = work[below_idx]
            if below_idx == 0:
                return float(below["top"])
            above = work[below_idx - 1]
            return (above["top"] + above["height"] + below["top"]) / 2

        cards: list[BackgroundPlacement] = []
        bg_cursor = 0
        for item in background:
            top = px_at(item.end_date)
            if isinstance(item, BreakItem):
                span = span_months(item.start_date, item.end_date)
                height = max(round(span * scale), break_floor)
                center = break_center(item)
                if center is not None:
                    top = round(center - height / 2)
            elif isinstance(item, EducationItem):
                height = MIN_STUDY_PX
            else:
                height = MIN_COURSE_PX
            top = max(top, bg_cursor)
            cards.append({"item": item, "top": top, "height": height})
            bg_cursor = top + height + WORK_GAP_PX

        stage = max(
            [p["top"] + p["height"] for p in work]
            + [c["top"] + c["height"] for c in cards],
            default=0,
        )
        return {"stage_height": stage, "work": work, "background": cards}
