"""Integration tests for MCP server."""

from simple_mcp_server.server import create_server


def test_create_server():
    """Test server creation."""
    server = create_server()
    assert server is not None
    assert server.name == "simple-mcp-server"
