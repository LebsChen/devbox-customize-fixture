#!/usr/bin/env python3
"""Minimal stdio MCP server (newline-delimited JSON-RPC) for DevBox fixtures."""
import json
import sys

TOOLS = [{
    "name": "fixture_echo",
    "description": "Echo text prefixed with the fixture MCP token.",
    "inputSchema": {"type": "object", "properties": {"text": {"type": "string"}},
                    "required": ["text"]},
}]


def reply(msg_id, result):
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": result}) + "\n")
    sys.stdout.flush()


for line in sys.stdin:
    if not line.strip():
        continue
    req = json.loads(line)
    method, msg_id = req.get("method"), req.get("id")
    if msg_id is None:
        continue
    if method == "initialize":
        reply(msg_id, {"protocolVersion": req.get("params", {}).get("protocolVersion", "2024-11-05"),
                       "capabilities": {"tools": {}},
                       "serverInfo": {"name": "devbox-fixture", "version": "1.0.0"}})
    elif method == "tools/list":
        reply(msg_id, {"tools": TOOLS})
    elif method == "tools/call":
        text = req.get("params", {}).get("arguments", {}).get("text", "")
        reply(msg_id, {"content": [{"type": "text", "text": f"MCP-OK-2208:{text}"}]})
    else:
        sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": msg_id,
                                     "error": {"code": -32601, "message": "method not found"}}) + "\n")
        sys.stdout.flush()
