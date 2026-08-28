from typing import Self, final

from pydantic import Field

from services.api.analyses.brand import company_catalog
from services.api.common.schemas import CamelCaseModel


@final
class CompanyItem(CamelCaseModel):
    """A company we can render a badge for, with all matchable labels."""

    slug: str
    name: str
    category: str | None = None
    aliases: list[str] = Field(default_factory=list)
    icon_url: str


@final
class CompaniesResponse(CamelCaseModel):
    """Catalog of company labels external services can rely on."""

    count: int
    companies: list[CompanyItem] = Field(default_factory=list)

    @classmethod
    def build(cls) -> Self:
        """Assemble the response from the brand registry catalog."""
        companies = [CompanyItem(**entry) for entry in company_catalog()]
        return cls(count=len(companies), companies=companies)
