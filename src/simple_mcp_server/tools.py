"""Pure functions implementing tool logic."""

import uuid
from datetime import UTC, datetime
from typing import Literal
from zoneinfo import ZoneInfo


def get_current_time(
    format_type: Literal["iso", "unix", "human"] = "iso",
    tz: str | None = None,
) -> str:
    """Get current time in various formats.

    Args:
        format_type: Output format - "iso", "unix", or "human"
        tz: Timezone name (e.g., "America/New_York"). None uses system timezone.

    Returns:
        Current time as a string in the requested format

    Raises:
        ValueError: If format_type is invalid or timezone is unknown
    """
    formatters = {
        "iso": lambda dt: dt.isoformat(),
        "unix": lambda dt: str(int(dt.timestamp())),
        "human": lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S %Z"),
    }

    formatter = formatters.get(format_type)
    if not formatter:
        raise ValueError(f"Invalid format: {format_type}. Must be 'iso', 'unix', or 'human'")

    try:
        dt = datetime.now(ZoneInfo(tz)) if tz else datetime.now(UTC)
    except Exception as e:
        raise ValueError(f"Invalid timezone: {tz}") from e

    return formatter(dt)


def _divide(a: float, b: float) -> float:
    """Divide a by b with zero check."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


def _modulo(a: float, b: float) -> float:
    """Calculate a modulo b with zero check."""
    if b == 0:
        raise ZeroDivisionError("Cannot take modulo by zero")
    return a % b


def calculate(
    operation: Literal["add", "subtract", "multiply", "divide", "power", "modulo"],
    a: float,
    b: float,
) -> float:
    """Perform basic arithmetic operations.

    Args:
        operation: The operation to perform
        a: First operand
        b: Second operand

    Returns:
        Result of the calculation

    Raises:
        ValueError: If operation is invalid
        ZeroDivisionError: If dividing or taking modulo by zero
    """
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": _divide,
        "power": lambda x, y: x**y,
        "modulo": _modulo,
    }

    operation_fn = operations.get(operation)
    if not operation_fn:
        raise ValueError(
            f"Invalid operation: {operation}. "
            f"Must be 'add', 'subtract', 'multiply', 'divide', 'power', or 'modulo'"
        )

    return operation_fn(a, b)


def string_transform(
    text: str,
    operation: Literal["uppercase", "lowercase", "reverse", "length", "word_count"],
) -> str | int:
    """Transform strings in various ways.

    Args:
        text: Input string to transform
        operation: The transformation to apply

    Returns:
        Transformed string or count (int for length/word_count)

    Raises:
        ValueError: If operation is invalid
    """
    operations = {
        "uppercase": str.upper,
        "lowercase": str.lower,
        "reverse": lambda s: s[::-1],
        "length": len,
        "word_count": lambda s: len(s.split()),
    }

    operation_fn = operations.get(operation)
    if not operation_fn:
        raise ValueError(
            f"Invalid operation: {operation}. "
            f"Must be 'uppercase', 'lowercase', 'reverse', 'length', or 'word_count'"
        )

    return operation_fn(text)


def _generate_uuid_v5(namespace: str | None, name: str | None) -> str:
    """Generate UUID version 5."""
    if not namespace or not name:
        raise ValueError("Version 5 requires both 'namespace' and 'name' parameters")

    namespace_map = {
        "dns": uuid.NAMESPACE_DNS,
        "url": uuid.NAMESPACE_URL,
        "oid": uuid.NAMESPACE_OID,
        "x500": uuid.NAMESPACE_X500,
    }

    ns_uuid = namespace_map.get(namespace.lower())
    if not ns_uuid:
        raise ValueError(f"Invalid namespace: {namespace}. Must be 'dns', 'url', 'oid', or 'x500'")

    return str(uuid.uuid5(ns_uuid, name))


def generate_uuid(
    version: Literal[1, 4, 5] = 4,
    namespace: str | None = None,
    name: str | None = None,
) -> str:
    """Generate a UUID.

    Args:
        version: UUID version (1, 4, or 5)
        namespace: UUID namespace for version 5 (e.g., 'dns', 'url', 'oid', 'x500')
        name: Name to hash for version 5

    Returns:
        Generated UUID as a string

    Raises:
        ValueError: If version is invalid or required params are missing for v5
    """
    generators = {
        1: lambda: str(uuid.uuid1()),
        4: lambda: str(uuid.uuid4()),
        5: lambda: _generate_uuid_v5(namespace, name),
    }

    generator = generators.get(version)
    if not generator:
        raise ValueError(f"Invalid version: {version}. Must be 1, 4, or 5")

    return generator()


def list_operations() -> dict[str, dict[str, str]]:
    """List all available operations/tools.

    Returns:
        Dictionary mapping tool names to their descriptions and parameters
    """
    return {
        "get_current_time": {
            "description": "Get current time in various formats",
            "parameters": "format (iso|unix|human), timezone (optional)",
        },
        "calculate": {
            "description": "Perform basic arithmetic operations",
            "parameters": "operation (add|subtract|multiply|divide|power|modulo), a, b",
        },
        "string_transform": {
            "description": "Transform strings in various ways",
            "parameters": "text, operation (uppercase|lowercase|reverse|length|word_count)",
        },
        "generate_uuid": {
            "description": "Generate a UUID",
            "parameters": "version (1|4|5), namespace (optional for v5), name (optional for v5)",
        },
        "list_operations": {
            "description": "List all available operations/tools",
            "parameters": "none",
        },
    }
