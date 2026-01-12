"""Main MCP server setup and entry point."""

import asyncio

from mcp.server import Server
from mcp.server.stdio import stdio_server

from .handlers import register_tools


def create_server() -> Server:
    """Create and configure the MCP server.

    Returns:
        Configured MCP server instance
    """
    server = Server("simple-mcp-server")
    register_tools(server)
    return server


async def run_server() -> None:  # pragma: no cover
    """Run the MCP server with stdio transport."""
    server = create_server()

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def main() -> None:  # pragma: no cover
    """Start the MCP server."""
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
