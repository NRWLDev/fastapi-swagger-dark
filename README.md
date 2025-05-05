[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![image](https://img.shields.io/pypi/v/fastapi_swagger_dark.svg)](https://pypi.org/project/fastapi-swagger-dark/)
[![image](https://img.shields.io/pypi/l/fastapi_swagger_dark.svg)](https://pypi.org/project/fastapi-swagger-dark/)
[![image](https://img.shields.io/pypi/pyversions/fastapi_swagger_dark.svg)](https://pypi.org/project/fastapi-swagger-dark/)
![style](https://github.com/NRWLDev/fastapi-swagger-dark/actions/workflows/style.yml/badge.svg)
![tests](https://github.com/NRWLDev/fastapi-swagger-dark/actions/workflows/tests.yml/badge.svg)
[![codecov](https://codecov.io/gh/NRWLDev/fastapi-swagger-dark/branch/main/graph/badge.svg)](https://codecov.io/gh/NRWLDev/fastapi-swagger-dark)

Simple plugin to support enabling a dark theme for swagger docs in a FastAPI application.

![screenshot](https://raw.githubusercontent.com/NRWLDev/fastapi-swagger-dark/main/screenshot.png)

# Usage

The simplest usage with default `/docs` endpoint can be achieved with something like:

```python
import fastapi
import fastapi_swagger_dark as fsd

app = fastapi.FastAPI(docs_url=None)
router = fastapi.APIRouter()

fsd.install(router)
app.include_router(router)
```

To install using a custom path:

```python
import fastapi
import fastapi_swagger_dark as fsd

app = fastapi.FastAPI(docs_url=None)
router = fastapi.APIRouter()

fsd.install(router, path="/swagger-docs")
app.include_router(router)
```

To install using a custom prefix:

```python
import fastapi
import fastapi_swagger_dark as fsd

app = fastapi.FastAPI(docs_url=None)
router = fastapi.APIRouter(prefix="/api/v1")

fsd.install(router, path="/docs")
app.include_router(router)
```

If you are customising the documentation endpoints, for example with
authorization, you can replace fastapi's default get_swagger_ui_html with the
custom one using the dark theme. Ensure the dark_theme route is also included.

```python
import typing

import fastapi
import fastapi_swagger_dark as fsd

app = fastapi.FastAPI(docs_url=None)


def auth_validation(...) -> None:
    ...


async def swagger_ui_html(
    request: fastapi.Request,
    _docs_auth: typing.Annotated[None, fastapi.Depends(auth_validation)],
) -> fastapi.responses.HTMLResponse:
    return fsd.get_swagger_ui_html(request)


app.get("/docs")(swwagger_ui_html)
app.get("/dark_theme.css", include_in_schema=False, name="dark_theme")(fsd.dark_swagger_theme)
```

# Credit

Thanks go to [@georgekhananaev](https://github.com/georgekhananaev) and their repository
[darktheme-auth-fastapi-server](https://github.com/georgekhananaev/darktheme-auth-fastapi-server)
for the basis of the stylesheet used here.
