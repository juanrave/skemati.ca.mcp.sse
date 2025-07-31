from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from mcp.server import Server
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Mount, Route
import uvicorn
import json
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import asyncio
import subprocess

# Create the MCP server
mcp = FastMCP("SSE Example Server")

API_BASE = "https://consultaprocesos.ramajudicial.gov.co:448/api/v2/"
API_RADICACION = "Procesos/Consulta/NumeroRadicacion"
API_NOMBRE_RAZON_SOCIAL = "Procesos/Consulta/NombreRazonSocial"

USER_AGENT = "skemati.ca.sse-app/1.0"

def ejecutar_comando_para_llm(comando, timeout=25):
    try:
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True
        )

        salida = resultado.stdout.strip()
        print(f"[DEBUG] Salida del comando: {salida}")  # <-- LOG


        # 🔎 Detectar errores conocidos en la salida (aunque el comando haya "funcionado")
        errores_conocidos = [
            "radicado no encontrado",
            "error de conexión",
            "parámetro inválido",
            "no se pudo procesar",  # puedes agregar más
        ]

        for error in errores_conocidos:
            if error.lower() in salida.lower():
                return f"[ERROR DETECTADO] {error.capitalize()}"

        return salida  # ✅ Si todo está bien

    except subprocess.CalledProcessError as e:
        salida_error = (e.stderr or e.stdout or "").strip()
        return f"[ERROR DE EJECUCIÓN] {salida_error}"

    except subprocess.TimeoutExpired:
        return "[ERROR] El comando excedió el tiempo de espera"

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
async def get_radicacion_por_numero(numero: str) -> str:
    """Get 
    Args:
        numero: corresponde al numero de radicacion.
    Returns:
        Los resultados de la consulta de la radicacion por numero.
    """
    """url = f"{API_BASE}{API_RADICACION}?numero={numero}&SoloActivos=false&pagina=1"
    data = await make_request(url)

    if not data:
        return "Unable to fetch data found."

    return json.dumps(data)
    """
    data = ejecutar_comando_para_llm(["judicial", "consulta", "radicado", numero])
    return json.dumps(data)

@mcp.tool()
async def get_radicacion_por_nombre(nombre: str) -> str:
    """Get 
    Args:
        nombre: corresponde al nombre de la razon social.
    Returns:
        Los resultados de la consulta de la radicacion por nombre de la razon social.
    """
    """url = f"{API_BASE}{API_NOMBRE_RAZON_SOCIAL}?nombre={nombre}&tipoPersona=nat&SoloActivos=false&pagina=1"
    data = await make_request(url)

    if not data:
        return "Unable to fetch data found."

    return json.dumps(data)
    """
    comando = ["judicial", "consulta", "nombre", nombre, "--tipo", "jur"]
    print(f"[DEBUG] Comando construido en get_radicacion_por_nombre: {comando}")  # <-- LOG
    data = ejecutar_comando_para_llm(comando)

    return json.dumps(data)

def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    """Create a Starlette application that can serve the MCP server with SSE."""
    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(
                request.scope,
                request.receive,
                request._send,
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )

    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )

if __name__ == "__main__":
    # Get the underlying MCP server
    mcp_server = mcp._mcp_server
    
    # Create Starlette app with SSE support
    starlette_app = create_starlette_app(mcp_server, debug=True)
    
    port = 8080
    print(f"Starting MCP server with SSE transport on port {port}...")
    print(f"SSE endpoint available at: http://localhost:{port}/sse")
    
    # Run the server using uvicorn
    uvicorn.run(starlette_app, host="0.0.0.0", port=port)