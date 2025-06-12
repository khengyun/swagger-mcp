from __future__ import annotations

import threading

import httpx
import streamlit as st
import uvicorn
from fastapi import FastAPI
from fastmcp.server.openapi import FastMCPOpenAPI
from fastmcp.server.server import FastMCP

# FastMCP manager that aggregates all running servers
manager = FastMCP(name="swagger-mcp-ui")

# FastAPI app exposing the manager's HTTP interface
api_app = FastAPI()
api_app.mount("/", manager.http_app(path="/"))

# Track mounted servers by prefix
SERVERS: dict[str, FastMCPOpenAPI] = {}


def _run_http_server() -> None:
    """Run the FastMCP HTTP interface on port 8000 in a background thread."""
    uvicorn.run(api_app, host="0.0.0.0", port=8000, log_level="info")


def _ensure_http_server_running() -> None:
    if "_http_thread" not in st.session_state:
        thread = threading.Thread(target=_run_http_server, daemon=True)
        thread.start()
        st.session_state["_http_thread"] = thread


def streamlit_app() -> None:
    """Render the Streamlit UI for managing Swagger MCP servers."""
    _ensure_http_server_running()

    st.title("Swagger MCP UI")

    st.subheader("Running Servers")
    for name in list(SERVERS.keys()):
        col1, col2 = st.columns([4, 1])
        col1.write(name)
        if col2.button("Stop", key=f"stop_{name}"):
            server = SERVERS.pop(name)
            manager.unmount(prefix=name)
            st.experimental_rerun()

    st.subheader("Add Server")
    with st.form("add_server"):
        name = st.text_input("Name")
        spec = st.text_input("OpenAPI Spec URL or Path")
        server_url = st.text_input("Server URL (optional)")
        submitted = st.form_submit_button("Start")
        if submitted:
            client = (
                httpx.AsyncClient(base_url=server_url)
                if server_url
                else httpx.AsyncClient()
            )
            server = FastMCPOpenAPI(openapi_spec=spec, client=client, name=name)
            manager.mount(prefix=name, server=server)
            SERVERS[name] = server
            st.experimental_rerun()

    st.markdown(
        "The MCP HTTP API is available at [http://localhost:8000](http://localhost:8000)."
    )


def main() -> None:  # pragma: no cover - used as a console script
    import streamlit.web.cli as stcli
    import sys

    sys.argv = ["streamlit", "run", __file__]
    sys.exit(stcli.main())


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
