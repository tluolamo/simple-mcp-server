# Simple MCP Server Demo

A simple Model Context Protocol (MCP) server demo with 5 basic tools, demonstrating how to build an MCP service with functional programming principles.

## Features

- **5 Simple Tools**: Time, calculations, string operations, UUID generation, and tool listing
- **Functional Style**: Pure functions with dictionary-based dispatch
- **100% Test Coverage**: Comprehensive unit tests
- **Type Safe**: Full type hints throughout
- **Local Operations**: No network calls, all operations are local

## Installation

```bash
# Install dependencies
task install
```

## Testing the Server

### Using MCP Inspector (Recommended)

Test the MCP server interactively using the official MCP Inspector:

```bash
# Using task command
task inspect

# Or run directly
npx @modelcontextprotocol/inspector uv run simple-mcp-server
```

This will:
1. Start the MCP server
2. Open a web interface at http://localhost:5173
3. Allow you to test all tools interactively

### Using Unit Tests

```bash
# Run all tests
task test

# Run with coverage report
task coverage
```

## Usage with Claude Desktop

Add this server to your Claude Desktop configuration:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "simple-mcp-server": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/simple-mcp-server",
        "run",
        "simple-mcp-server"
      ]
    }
  }
}
```

Replace `/absolute/path/to/simple-mcp-server` with the actual path to this project.

## Available Tools

### 1. get_current_time

Get the current time in various formats.

**Parameters:**
- `format` (optional): "iso", "unix", or "human" (default: "iso")
- `timezone` (optional): Timezone name like "America/New_York"

**Examples:**
```
ISO format (default): "2024-01-15T14:30:00+00:00"
Unix timestamp: "1705329000"
Human readable: "2024-01-15 14:30:00 UTC"
With timezone: "2024-01-15 09:30:00 EST"
```

### 2. calculate

Perform basic arithmetic operations.

**Parameters:**
- `operation`: "add", "subtract", "multiply", "divide", "power", or "modulo"
- `a`: First number
- `b`: Second number

**Examples:**
```
add(5, 3) = 8.0
subtract(10, 4) = 6.0
multiply(7, 6) = 42.0
divide(15, 3) = 5.0
power(2, 8) = 256.0
modulo(17, 5) = 2.0
```

### 3. string_transform

Transform strings in various ways.

**Parameters:**
- `text`: Input string
- `operation`: "uppercase", "lowercase", "reverse", "length", or "word_count"

**Examples:**
```
uppercase("hello") = "HELLO"
lowercase("WORLD") = "world"
reverse("hello") = "olleh"
length("hello world") = 11
word_count("hello world test") = 3
```

### 4. generate_uuid

Generate a UUID.

**Parameters:**
- `version` (optional): 1, 4, or 5 (default: 4)
- `namespace` (for v5): "dns", "url", "oid", or "x500"
- `name` (for v5): String to hash

**Examples:**
```
v1: "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
v4: "550e8400-e29b-41d4-a716-446655440000" (random)
v5: "886313e1-3b8a-5372-9b90-0c9aee199e5d" (deterministic)
```

### 5. list_operations

List all available tools with their descriptions.

**Parameters:** None

**Returns:** Formatted list of all tools and their parameters.

## Development

### Available Tasks

- `task install` - Install dependencies with uv
- `task format` - Format code with ruff
- `task lint` - Lint code with ruff
- `task lint-fix` - Lint and auto-fix issues
- `task test` - Run tests
- `task coverage` - Run tests with coverage report
- `task dev` - Run server in development mode
- `task inspect` - Test server with MCP Inspector (interactive)
- `task check` - Run all checks (format, lint, coverage)
- `task clean` - Clean build artifacts and cache

### Development Workflow

1. Make code changes
2. Run `task format` to format code
3. Run `task lint` to check for issues
4. Run `task test` to run unit tests
5. Run `task check` to run all checks before committing

### Project Structure

```
simple-mcp-server/
├── src/simple_mcp_server/
│   ├── server.py      # Main MCP server
│   ├── tools.py       # Pure tool functions
│   └── handlers.py    # MCP tool handlers
└── tests/
    ├── test_tools.py  # Unit tests
    └── test_server.py # Integration tests
```

### Code Style

This project follows functional programming principles:
- Pure functions with no side effects
- 80% test coverage requirement

## Requirements

- Python 3.14+
- uv (package manager)
- go-task (task runner)

## License

MIT
