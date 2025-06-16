from pathlib import Path

import fastapi
from fastapi.openapi import docs

here = Path(__file__).parent


def get_swagger_ui_html(request: fastapi.Request) -> fastapi.responses.HTMLResponse:
    return docs.get_swagger_ui_html(
        openapi_url=str(request.app.url_path_for("openapi")),
        title=request.app.title + " - Swagger UI",
        swagger_css_url=request.app.url_path_for("dark_theme"),
    )


async def swagger_ui_html(request: fastapi.Request) -> fastapi.responses.HTMLResponse:
    return get_swagger_ui_html(request)


async def dark_swagger_theme() -> fastapi.responses.FileResponse:
    return fastapi.responses.FileResponse(here / "swagger_ui_dark.min.css")


def install(router: fastapi.APIRouter, path: str = "/docs") -> None:
    router.get(path, include_in_schema=False)(swagger_ui_html)
    router.get("/dark_theme.css", include_in_schema=False, name="dark_theme")(dark_swagger_theme)
