from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

import fastapi
from fastapi.openapi import docs

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable


here = Path(__file__).parent


def get_swagger_ui_html(
    request: fastapi.Request,
    swagger_ui_parameters: dict[str, Any] | None = None,
) -> fastapi.responses.HTMLResponse:
    return docs.get_swagger_ui_html(
        openapi_url=str(request.app.url_path_for("openapi")),
        title=request.app.title + " - Swagger UI",
        swagger_css_url=request.app.url_path_for("dark_theme"),
        swagger_ui_parameters=swagger_ui_parameters,
    )


def generate_swagger_ui_html(
    swagger_ui_parameters: dict[str, Any] | None,
) -> Callable[[fastapi.request], Awaitable[fastapi.responses.HTMLResponse]]:
    async def swagger_ui_html(request: fastapi.Request) -> fastapi.responses.HTMLResponse:
        return get_swagger_ui_html(request, swagger_ui_parameters)

    return swagger_ui_html


async def dark_swagger_theme() -> fastapi.responses.FileResponse:
    return fastapi.responses.FileResponse(here / "swagger_ui_dark.min.css")


def install(
    router: fastapi.APIRouter,
    path: str = "/docs",
    swagger_ui_parameters: dict[str, Any] | None = None,
) -> None:
    router.get(path, include_in_schema=False)(generate_swagger_ui_html(swagger_ui_parameters))
    router.get("/dark_theme.css", include_in_schema=False, name="dark_theme")(dark_swagger_theme)
