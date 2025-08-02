# skemati.ca.mcp.sse

Servidor MCP (Model Context Protocol) con soporte para Server-Sent Events (SSE) y consulta de procesos judiciales en Colombia.

## Descripción

Este proyecto implementa un servidor MCP usando Starlette y FastAPI, permitiendo la consulta de procesos judiciales por número de radicación o por nombre/razón social, integrando la API pública de la Rama Judicial de Colombia. Además, soporta streaming de eventos en tiempo real mediante SSE y expone herramientas MCP para integración con clientes LLM y flujos de IA.

## Características

- Exposición de endpoints SSE para comunicación en tiempo real.
- Herramientas MCP para consulta de procesos judiciales:
  - Por número de radicación.
  - Por nombre de persona natural.
  - Por nombre de persona jurídica.
- Integración con la API oficial de la Rama Judicial de Colombia.
- Ejecución de comandos CLI para consulta judicial.
- Código compatible con Python 3.10+.

## Instalación

1. **Clona el repositorio:**
   ```sh
   git clone https://github.com/juanrave/skemati.ca.mcp.sse.git
   cd skemati.ca.mcp.sse
   ```

2. **Crea y activa un entorno virtual:**
   ```sh
   python3.10 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instala las dependencias:**
   ```sh
   pip install -r requirements.txt
   ```
   O, si usas [uv](https://github.com/astral-sh/uv):
   ```sh
   pip install uv
   uv pip install fastapi uvicorn httpx "mcp[cli]"
   ```

   > **Nota:** El paquete `mcp` puede ser privado. Consulta a tu equipo si no está disponible en PyPI.

## Ejecución

1. **Inicia el servidor:**
   ```sh
   python server.py
   ```
   El servidor se ejecutará por defecto en el puerto 2055.

2. **Endpoints disponibles:**
   - `GET /sse` — Endpoint SSE para comunicación en tiempo real.
   - `POST /messages/` — Endpoint para mensajes MCP.

## Uso de las herramientas MCP

- **Consulta por número de radicación:**
  ```python
  await get_radicacion_por_numero("11001310302520230012300")
  ```

- **Consulta por nombre de persona natural:**
  ```python
  await get_radicacion_por_nombre_persona_natural("JUAN PEREZ")
  ```

- **Consulta por nombre de persona jurídica:**
  ```python
  await get_radicacion_por_nombre_persona_juridica("BANCOLOMBIA")
  ```

## Requisitos

- Python 3.10 o superior.
- Acceso a la API de la Rama Judicial de Colombia.
- Dependencias listadas en `pyproject.toml` o `requirements.txt`.

## Notas adicionales

- Si usas el cliente MCP remoto:
  ```sh
  npx -p mcp-remote@latest mcp-remote-client http://localhost:2055/sse
  ```
- Puedes cambiar el puerto modificando la variable `port` en `server.py`.

---