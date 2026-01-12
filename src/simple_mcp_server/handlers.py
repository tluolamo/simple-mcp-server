"""MCP tool handlers that connect tools to the protocol."""

from typing import Any

from mcp.server import Server
from mcp.types import TextContent, Tool

from . import tools

GET_CURRENT_TIME_TOOL = {
    "name": "get_current_time",
    "description": "Get current time in various formats (iso, unix, or human-readable)",
    "inputSchema": {
        "type": "object",
        "properties": {
            "format": {
                "type": "string",
                "enum": ["iso", "unix", "human"],
                "description": "Output format",
                "default": "iso",
            },
            "timezone": {
                "type": "string",
                "description": "Timezone name (e.g., 'America/New_York')",
            },
        },
        "required": [],
    },
}

CALCULATE_TOOL = {
    "name": "calculate",
    "description": "Perform basic arithmetic operations",
    "inputSchema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["add", "subtract", "multiply", "divide", "power", "modulo"],
                "description": "The operation to perform",
            },
            "a": {
                "type": "number",
                "description": "First operand",
            },
            "b": {
                "type": "number",
                "description": "Second operand",
            },
        },
        "required": ["operation", "a", "b"],
    },
}

STRING_TRANSFORM_TOOL = {
    "name": "string_transform",
    "description": "Transform strings in various ways",
    "inputSchema": {
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "Input string to transform",
            },
            "operation": {
                "type": "string",
                "enum": ["uppercase", "lowercase", "reverse", "length", "word_count"],
                "description": "The transformation to apply",
            },
        },
        "required": ["text", "operation"],
    },
}

GENERATE_UUID_TOOL = {
    "name": "generate_uuid",
    "description": "Generate a UUID (version 1, 4, or 5)",
    "inputSchema": {
        "type": "object",
        "properties": {
            "version": {
                "type": "integer",
                "enum": [1, 4, 5],
                "description": "UUID version",
                "default": 4,
            },
            "namespace": {
                "type": "string",
                "enum": ["dns", "url", "oid", "x500"],
                "description": "UUID namespace for version 5",
            },
            "name": {
                "type": "string",
                "description": "Name to hash for version 5",
            },
        },
        "required": [],
    },
}

LIST_OPERATIONS_TOOL = {
    "name": "list_operations",
    "description": "List all available operations/tools with their descriptions",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}

TOOL_DEFINITIONS = [
    GET_CURRENT_TIME_TOOL,
    CALCULATE_TOOL,
    STRING_TRANSFORM_TOOL,
    GENERATE_UUID_TOOL,
    LIST_OPERATIONS_TOOL,
]


def _handle_get_current_time(arguments: dict[str, Any]) -> str:  # pragma: no cover
    """Handle get_current_time tool."""
    return tools.get_current_time(
        format_type=arguments.get("format", "iso"),
        tz=arguments.get("timezone"),
    )


def _handle_calculate(arguments: dict[str, Any]) -> str:  # pragma: no cover
    """Handle calculate tool."""
    result = tools.calculate(
        operation=arguments["operation"],
        a=float(arguments["a"]),
        b=float(arguments["b"]),
    )
    return str(result)


def _handle_string_transform(arguments: dict[str, Any]) -> str:  # pragma: no cover
    """Handle string_transform tool."""
    result = tools.string_transform(
        text=arguments["text"],
        operation=arguments["operation"],
    )
    return str(result)


def _handle_generate_uuid(arguments: dict[str, Any]) -> str:  # pragma: no cover
    """Handle generate_uuid tool."""
    return tools.generate_uuid(
        version=arguments.get("version", 4),
        namespace=arguments.get("namespace"),
        name=arguments.get("name"),
    )


def _handle_list_operations(_arguments: dict[str, Any]) -> str:  # pragma: no cover
    """Handle list_operations tool."""
    result = tools.list_operations()
    return "\n".join(
        f"- {tool}: {info['description']}\n  Parameters: {info['parameters']}"
        for tool, info in result.items()
    )


def register_tools(server: Server) -> None:
    """Register all tool handlers with the MCP server.

    Args:
        server: MCP server instance to register tools with
    """

    @server.list_tools()
    async def list_tools() -> list[Tool]:  # pragma: no cover - MCP protocol handler
        """List all available tools."""
        return [Tool(**definition) for definition in TOOL_DEFINITIONS]

    @server.call_tool()
    async def call_tool(
        name: str, arguments: dict[str, Any]
    ) -> list[TextContent]:  # pragma: no cover - MCP protocol handler
        """Handle tool calls by routing to appropriate handlers.

        Args:
            name: Name of the tool to call
            arguments: Tool-specific arguments

        Returns:
            List of text content with the tool result

        Raises:
            ValueError: If tool name is unknown or arguments are invalid
        """
        tool_handlers = {
            "get_current_time": _handle_get_current_time,
            "calculate": _handle_calculate,
            "string_transform": _handle_string_transform,
            "generate_uuid": _handle_generate_uuid,
            "list_operations": _handle_list_operations,
        }

        try:  # pragma: no cover
            handler = tool_handlers.get(name)
            if not handler:
                raise ValueError(f"Unknown tool: {name}")

            result = handler(arguments)
            return [TextContent(type="text", text=result)]

        except (ValueError, ZeroDivisionError, KeyError) as e:
            return [TextContent(type="text", text=f"Error: {e!s}")]
