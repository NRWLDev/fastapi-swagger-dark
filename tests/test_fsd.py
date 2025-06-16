import http
from pathlib import Path
from unittest import mock

import fastapi
import httpx
import pytest

import fastapi_swagger_dark as fsd


@pytest.fixture
def app():
    app_ = fastapi.FastAPI()
    router = fastapi.APIRouter()
    fsd.install(router)
    app_.include_router(router)

    return app_


def test_install():
    router = mock.Mock()

    fsd.install(router)

    assert router.get.call_args_list == [
        mock.call("/docs", include_in_schema=False),
        mock.call("/dark_theme.css", include_in_schema=False, name="dark_theme"),
    ]
    assert router.get.return_value.call_args_list == [
        mock.call(fsd.swagger_ui_html),
        mock.call(fsd.dark_swagger_theme),
    ]


def test_install_with_custom_path():
    router = mock.Mock()

    fsd.install(router, "/path/to/docs")

    assert router.get.call_args_list == [
        mock.call("/path/to/docs", include_in_schema=False),
        mock.call("/dark_theme.css", include_in_schema=False, name="dark_theme"),
    ]
    assert router.get.return_value.call_args_list == [
        mock.call(fsd.swagger_ui_html),
        mock.call(fsd.dark_swagger_theme),
    ]


def test_generate_swagger_ui_html(app):
    r = fastapi.Request({"type": "http", "app": app, "headers": {}, "root_path": "http://host"})

    response = fsd.get_swagger_ui_html(r)

    assert b'<link type="text/css" rel="stylesheet" href="/dark_theme.css">' in response.body


async def test_swagger_ui_html(app):
    r = fastapi.Request({"type": "http", "app": app, "headers": {}, "root_path": "http://host"})

    response = await fsd.swagger_ui_html(r)

    assert b'<link type="text/css" rel="stylesheet" href="/dark_theme.css">' in response.body


async def test_dark_swagger_theme():
    response = await fsd.dark_swagger_theme()

    assert response.path == Path(fsd.here / "swagger_ui_dark.min.css")


@pytest.mark.parametrize(
    ("prefix", "path"),
    [
        (None, None),
        (None, "/docs"),
        (None, "/custom-docs"),
        ("/prefix", "/docs"),
        ("/prefix", "/custom-docs"),
    ],
)
async def test_custom_configuration_swagger_html(prefix, path):
    app = fastapi.FastAPI()

    router = fastapi.APIRouter(prefix=prefix or "")
    kwargs = {"path": path} if path else {}
    fsd.install(router, **kwargs)
    app.include_router(router)

    transport = httpx.ASGITransport(app=app, raise_app_exceptions=False, client=("1.2.3.4", 123))
    client = httpx.AsyncClient(transport=transport, base_url="https://test")

    url = f"{prefix}{path or '/docs'}" if prefix else path or "/docs"
    r = await client.get(url)

    assert r.status_code == http.HTTPStatus.OK
    assert r.headers["content-type"] == "text/html; charset=utf-8"


@pytest.mark.parametrize("prefix", [None, "/prefix"])
async def test_custom_configuration_swagger_css(prefix):
    app = fastapi.FastAPI()

    router = fastapi.APIRouter(prefix=prefix or "")
    fsd.install(router)
    app.include_router(router)

    transport = httpx.ASGITransport(app=app, raise_app_exceptions=False, client=("1.2.3.4", 123))
    client = httpx.AsyncClient(transport=transport, base_url="https://test")

    url = f"{prefix}/dark_theme.css" if prefix else "/dark_theme.css"
    r = await client.get(url)

    assert r.status_code == http.HTTPStatus.OK
    assert r.headers["content-type"] == "text/css; charset=utf-8"
