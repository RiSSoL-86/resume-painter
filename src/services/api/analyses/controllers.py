from http import HTTPStatus
from typing import final

from django.http import HttpResponse
from dmr import Body, Controller, ResponseSpec, modify, validate
from dmr.plugins.pydantic import PydanticSerializer
from dmr.renderers import FileRenderer

from services.api.analyses.schemas import (
    ColorsResponse,
    CompaniesResponse,
    Dashboard,
)
from services.api.analyses.utils import render_html


@final
class AnalysisDashboardController(Controller[PydanticSerializer]):
    """Render a resume dashboard payload as an HTML report page."""

    auth = None

    @validate(
        ResponseSpec(
            str,
            status_code=HTTPStatus.OK,
            limit_to_content_types={"text/html"},
            description="Resume report rendered as HTML",
        ),
        tags=["Analyses"],
        renderers=[FileRenderer("text/html")],
        validate_responses=False,
    )
    async def post(self, parsed_body: Body[Dashboard]) -> HttpResponse:
        """Render the provided dashboard payload as an HTML report."""
        download_name = parsed_body.candidate.full_name or "report"
        return await render_html(
            status=HTTPStatus.OK,
            context={"d": parsed_body, "pending": False},
            template_name="analyses/dashboard.html",
            download_name=download_name,
        )


@final
class ColorController(Controller[PydanticSerializer]):
    """Publish the colour codes used across dashboard payloads."""

    auth = None

    @modify(status_code=HTTPStatus.OK, tags=["Analyses"])
    async def get(self) -> ColorsResponse:
        """Return the colour-code enum (name -> number)."""
        return ColorsResponse()


@final
class CompaniesController(Controller[PydanticSerializer]):
    """Publish the company labels we can render a badge for."""

    auth = None

    @modify(status_code=HTTPStatus.OK, tags=["Analyses"])
    async def get(self) -> CompaniesResponse:
        """Return the catalog of renderable company labels and icons."""
        return CompaniesResponse.build()
