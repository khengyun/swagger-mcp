from __future__ import annotations

import httpx
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastmcp.server.server import FastMCP
from fastmcp.server.openapi import FastMCPOpenAPI
from pathlib import Path

app = FastAPI()
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

manager = FastMCP(name="swagger-mcp-ui")

# Mount FastMCP HTTP interface under /mcp
app.mount("/mcp", manager.http_app(path="/"))

# Keep track of mounted servers by prefix
SERVERS: dict[str, FastMCPOpenAPI] = {}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "servers": list(SERVERS.keys())}
    )


@app.post("/add", response_class=HTMLResponse)
async def add_server(
    request: Request,
    name: str = Form(...),
    spec: str = Form(...),
    server_url: str | None = Form(None),
):
    client = httpx.AsyncClient(base_url=server_url) if server_url else httpx.AsyncClient()
    server = FastMCPOpenAPI(openapi_spec=spec, client=client, name=name)
    manager.mount(prefix=name, server=server)
    SERVERS[name] = server
    return RedirectResponse("/", status_code=303)


@app.post("/remove", response_class=HTMLResponse)
async def remove_server(name: str = Form(...)):
    server = SERVERS.pop(name, None)
    if server:
        manager.unmount(prefix=name)
    return RedirectResponse("/", status_code=303)


def main() -> None:
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
