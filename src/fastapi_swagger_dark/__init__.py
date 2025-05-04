from pathlib import Path

import fastapi
from fastapi.openapi import docs


here = Path(__file__).parent


def get_swagger_ui_html(request):
    return docs.get_swagger_ui_html(
        openapi_url=str(request.url_for("openapi")),
        title=request.app.title + " - Swagger UI",
        swagger_css_url=request.url_for("dark_theme"),
    )


async def swagger_ui_html(request: fastapi.Request) -> fastapi.responses.HTMLResponse:
    return get_swagger_ui_html(request)


async def dark_swagger_theme(request: fastapi.Request) -> fastapi.responses.FileResponse:
    f = here / "swagger_ui_dark.min.css"
    return fastapi.responses.FileResponse(str(f))


def install(router: fastapi.APIRouter, path: str = "/docs") -> None:
    router.get(path, include_in_schema=False)(swagger_ui_html)
    router.get("/dark_theme.css", include_in_schema=False, name="dark_theme")(dark_swagger_theme)
