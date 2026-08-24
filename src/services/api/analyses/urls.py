from dmr.routing import Router, path

from services.api.analyses.controllers import (
    AnalysisDashboardController,
    ColorController,
    CompaniesController,
)

router = Router(
    prefix="analyses/",
    urls=[
        path(
            "dashboard/",
            AnalysisDashboardController.as_view(),
            name="dashboard",
        ),
        path(
            "colors/",
            ColorController.as_view(),
            name="colors",
        ),
        path(
            "companies/",
            CompaniesController.as_view(),
            name="companies",
        ),
    ],
)
