import json
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import asyncio

# Initialize FastMCP server
mcp = FastMCP("skemati.ca", 
    json_response=True)

# Constants
API_BASE = "https://consultaprocesos.ramajudicial.gov.co:448/api/v2/Procesos/Consulta/NumeroRadicacion"
USER_AGENT = "skemati.ca.sse-app/1.0"

async def make_request(url: str) -> dict[str, Any] | None:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

@mcp.tool()
async def get_radicacion(numero: str) -> str:
    """Get 
    Args:
        numero: 
    Returns:

    """
    url = f"{API_BASE}?numero={numero}&SoloActivos=false&pagina=1"
    data = await make_request(url)

    if not data:
        return "Unable to fetch data found."

    return json.dumps(data)

app = FastAPI()

async def event_generator():
    for i in range(10):
        yield f"data: Message {i}\n\n"
        await asyncio.sleep(1)

@app.get("/stream")
async def stream():
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("?{numero}")
async def stream_alerts(numero: str):
    async def event_generator():
        # You can call your get_alerts tool here and yield results as they come in
        alerts = await get_radicacion(numero)
        for alert in alerts.split("\n---\n"):
            yield f"data: {alert}\n\n"
            await asyncio.sleep(1)  # Simulate streaming
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/tools")
async def list_tools():
    """List all available MCP tools with their names and docstrings."""
    tools = []
    tool_dict = getattr(mcp, "_tools", {})
    for name, func in tool_dict.items():
        tools.append({
            "name": name,
            "doc": func.__doc__
        })
    return tools

@app.get("/skemati.ca.mcp/sse")
async def mcp_sse(request: Request):
    async def event_generator():
        data = await get_radicacion("NY")
        for alert in data.split("\n---\n"):
            if await request.is_disconnected():
                break
            yield f"data: {alert}\n\n"
            await asyncio.sleep(1)
    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    mcp.run(transport="streamable-http")