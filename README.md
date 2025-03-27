# MCP Server OS Tools

This is a python bundle to use with the mcp python container:
https://github.com/ground-creative/mcp-container-python

## Installation

1. Follow instructions to install the MCP Python container from here:
   https://github.com/ground-creative/mcp-container-python

2. Clone the repository in folder mcp_server

```
cd mcp_servers
rm -rf tools
git clone https://github.com/ground-creative/mcp-os-tool-python.git tools
```

3. Run the server

```
# Run via fastapi wrapper
python3 run.py -s fastapi

# Run the mcp server directly
python3 run.py -s fastmcp
```
