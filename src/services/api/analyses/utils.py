from http import HTTPStatus
from typing import Any
from urllib.parse import quote

from asgiref.sync import sync_to_async
from django.http import HttpResponse
from django.template.loader import render_to_string


async def render_html(
    status: HTTPStatus,
    context: dict[str, Any],
    template_name: str,
    download_name: str = "",
) -> HttpResponse:
    """Render a template to HTML.

    When ``download_name`` is given the response is served as an attachment
    named ``<download_name>.html``; otherwise it is returned inline.
    """

    html = await sync_to_async(
        func=render_to_string,
        thread_sensitive=False,
    )(template_name, context=context)
    response = HttpResponse(
        html,
        status=status,
        content_type="text/html; charset=utf-8",
    )
    if download_name:
        encoded = quote(f"{download_name}.html")
        ascii_name = (
            download_name.encode("ascii", "ignore").decode("ascii").strip()
        )
        fallback = f"{ascii_name}.html" if ascii_name else "report.html"
        response["Content-Disposition"] = (
            f"attachment; filename=\"{fallback}\"; filename*=UTF-8''{encoded}"
        )
    return response
