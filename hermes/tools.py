"""Tool registration and execution framework for Hermes agent."""

import json
from typing import Any, Callable

# Registry of available tools
_tool_registry: dict[str, dict[str, Any]] = {}
_tool_handlers: dict[str, Callable] = {}


def tool(name: str, description: str, input_schema: dict):
    """Decorator to register a function as an agent tool.

    Usage:
        @tool("get_weather", "Get weather for a location", {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name"}
            },
            "required": ["location"]
        })
        def get_weather(location: str) -> str:
            return f"72F and sunny in {location}"
    """
    def decorator(func: Callable) -> Callable:
        _tool_registry[name] = {
            "name": name,
            "description": description,
            "input_schema": input_schema,
        }
        _tool_handlers[name] = func
        return func
    return decorator


def get_tool_definitions() -> list[dict]:
    """Return all registered tool definitions for the Claude API."""
    return list(_tool_registry.values())


def execute_tool(name: str, tool_input: dict) -> str:
    """Execute a registered tool by name with the given input."""
    handler = _tool_handlers.get(name)
    if handler is None:
        return json.dumps({"error": f"Unknown tool: {name}"})

    try:
        result = handler(**tool_input)
        if isinstance(result, str):
            return result
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})


# ---------------------------------------------------------------------------
# Example tools — replace or extend these for your Hermes agent
# ---------------------------------------------------------------------------

@tool("read_file", "Read the contents of a file at the given path", {
    "type": "object",
    "properties": {
        "path": {"type": "string", "description": "File path to read"}
    },
    "required": ["path"]
})
def read_file(path: str) -> str:
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return json.dumps({"error": f"File not found: {path}"})


@tool("write_file", "Write content to a file at the given path", {
    "type": "object",
    "properties": {
        "path": {"type": "string", "description": "File path to write"},
        "content": {"type": "string", "description": "Content to write"}
    },
    "required": ["path", "content"]
})
def write_file(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return f"Wrote {len(content)} bytes to {path}"


@tool("run_command", "Execute a shell command and return its output", {
    "type": "object",
    "properties": {
        "command": {"type": "string", "description": "Shell command to run"}
    },
    "required": ["command"]
})
def run_command(command: str) -> str:
    import subprocess
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=30
        )
        output = result.stdout
        if result.returncode != 0:
            output += f"\nSTDERR: {result.stderr}" if result.stderr else ""
            output += f"\nExit code: {result.returncode}"
        return output or "(no output)"
    except subprocess.TimeoutExpired:
        return json.dumps({"error": "Command timed out after 30 seconds"})


@tool("search_web", "Search the web for information (placeholder — wire to your search API)", {
    "type": "object",
    "properties": {
        "query": {"type": "string", "description": "Search query"}
    },
    "required": ["query"]
})
def search_web(query: str) -> str:
    return json.dumps({
        "note": "Placeholder — wire this to your preferred search API",
        "query": query,
        "results": []
    })
