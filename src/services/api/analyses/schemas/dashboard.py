from typing import final

from pydantic import Field

from services.api.analyses.schemas.candidate import CandidateBlock
from services.api.analyses.schemas.glance import GlanceBlock
from services.api.analyses.schemas.insights import (
    Highlight,
    Question,
    Risk,
    Skill,
    Unknown,
)
from services.api.analyses.schemas.lifeline import LifelineBlock
from services.api.common.schemas import CamelCaseModel


@final
class Dashboard(CamelCaseModel):
    """Full resume-report payload rendered by the dashboard template."""

    candidate: CandidateBlock
    glance: GlanceBlock
    lifeline: LifelineBlock = Field(default_factory=LifelineBlock)
    highlights: list[Highlight] = Field(default_factory=list)
    featured_skills: list[Skill] = Field(default_factory=list)
    other_skills: list[Skill] = Field(default_factory=list)
    risks: list[Risk] = Field(default_factory=list)
    unknowns: list[Unknown] = Field(default_factory=list)
    questions: list[Question] = Field(default_factory=list)
