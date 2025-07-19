SSE (Server-Sent Events) is a technology used in Model Context Protocol (MCP) to enable real-time, server-pushed updates to clients over a single HTTP connection. In MCP, SSE facilitates communication between AI models and tools, allowing the server to stream responses back to the client in real-time. This is particularly useful for remote MCP servers where the client and server are not on the same machine. 

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
    
npx -p mcp-remote@latest mcp-remote-client http://localhost:8000/mcp/sse



uv init skemati.ca.mcp.sse
cd skemati.ca.mcp.sse
uv venv
source .venv/bin/activate   
uv add "mcp[cli]" httpx  
uv python pin 3.10      

sudo apt update              
sudo apt install python3.10 python3.10-dev
pip3 install fastapi uvicorn
/Library/Developer/CommandLineTools/usr/bin/python3 -m pip install --upgrade pip
uv add fastapi uvicorn 


python3 -m ensurepip --upgrade
python3 -m pip install fastapi uvicorn

uv add fastapi uvicorn 

uv run base.py 

tail -n 20 -f ~/Library/Logs/Claude/mcp*.log   