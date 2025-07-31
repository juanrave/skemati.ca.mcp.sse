# skemati.ca.mcp.sse

Servidor MCP (Model Context Protocol) con FastAPI y soporte para Server-Sent Events (SSE) para consulta de procesos judiciales en Colombia.

## ¿Qué hace este proyecto?

- Expone un servidor MCP usando FastAPI y Starlette.
- Permite la consulta de procesos judiciales por número de radicación o por nombre/razón social, integrando la API pública de la Rama Judicial de Colombia.
- Soporta streaming de eventos en tiempo real mediante SSE.
- Incluye herramientas MCP para integración con clientes LLM y flujos de IA.

## Instalación

1. **Clona el repositorio:**
   ```sh
   git clone https://github.com/juanrave/skemati.ca.mcp.sse.git
   cd skemati.ca.mcp.sse
   ```

2. **Crea y activa un entorno virtual:**
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instala las dependencias:**
   ```sh
   pip install -r requirements.txt
   ```
   O, si usas `uv`:
   ```sh
   uv pip install fastapi uvicorn httpx
   ```

   > **Nota:** Si necesitas el paquete `mcp`, consulta la documentación interna o a tu equipo para instalarlo.

## Ejecución del servidor

1. **Ejecuta el servidor:**
   ```sh
   uvicorn server:starlette_app --host 0.0.0.0 --port 8080
   ```
   O, si tienes un bloque `if __name__ == "__main__":` en `server.py`:
   ```sh
   python server.py
   ```

2. **Endpoints disponibles:**
   - `/sse` — Endpoint SSE para comunicación en tiempo real.
   - `/messages/` — Endpoint para mensajes MCP.
   - Herramientas MCP: consulta de procesos judiciales por número o nombre.

## Ejemplo de uso

Consulta de radicación por número:
```python
await get_radicacion_por_numero("11001310302520230012300")
```

Consulta de radicación por nombre:
```python
await get_radicacion_por_nombre("BANCOLOMBIA")
```

## Notas

- Asegúrate de tener Python 3.10+ instalado.
- Si usas el cliente MCP remoto:
  ```sh
  npx -p mcp-remote@latest mcp-remote-client http://localhost:8080/sse
  ```

---

¿Quieres que lo actualice directamente en tu archivo `README.md`?