"""Unit tests for pure tool functions."""

import pytest

from simple_mcp_server.tools import (
    calculate,
    generate_uuid,
    get_current_time,
    list_operations,
    string_transform,
)


def test_get_current_time_iso():
    """Test getting current time in ISO format."""
    result = get_current_time("iso")
    assert isinstance(result, str)
    assert "T" in result or "-" in result


def test_get_current_time_unix():
    """Test getting current time in Unix format."""
    result = get_current_time("unix")
    assert isinstance(result, str)
    assert result.isdigit()


def test_get_current_time_human():
    """Test getting current time in human format."""
    result = get_current_time("human")
    assert isinstance(result, str)
    assert len(result) > 0


def test_get_current_time_invalid_format():
    """Test invalid format raises error."""
    with pytest.raises(ValueError, match="Invalid format"):
        get_current_time("invalid")


def test_get_current_time_with_timezone():
    """Test getting time with specific timezone."""
    result = get_current_time("iso", "America/New_York")
    assert isinstance(result, str)
    assert len(result) > 0


def test_get_current_time_invalid_timezone():
    """Test invalid timezone raises error."""
    with pytest.raises(ValueError, match="Invalid timezone"):
        get_current_time("iso", "Invalid/Timezone")


def test_calculate_add():
    """Test addition."""
    assert calculate("add", 2, 3) == 5


def test_calculate_subtract():
    """Test subtraction."""
    assert calculate("subtract", 5, 3) == 2


def test_calculate_multiply():
    """Test multiplication."""
    assert calculate("multiply", 4, 3) == 12


def test_calculate_divide():
    """Test division."""
    assert calculate("divide", 10, 2) == 5


def test_calculate_divide_by_zero():
    """Test division by zero raises error."""
    with pytest.raises(ZeroDivisionError):
        calculate("divide", 10, 0)


def test_calculate_power():
    """Test power operation."""
    assert calculate("power", 2, 3) == 8


def test_calculate_modulo():
    """Test modulo operation."""
    assert calculate("modulo", 10, 3) == 1


def test_calculate_modulo_by_zero():
    """Test modulo by zero raises error."""
    with pytest.raises(ZeroDivisionError):
        calculate("modulo", 10, 0)


def test_calculate_invalid_operation():
    """Test invalid operation raises error."""
    with pytest.raises(ValueError, match="Invalid operation"):
        calculate("invalid", 1, 2)


def test_string_transform_uppercase():
    """Test uppercase transformation."""
    assert string_transform("hello", "uppercase") == "HELLO"


def test_string_transform_lowercase():
    """Test lowercase transformation."""
    assert string_transform("HELLO", "lowercase") == "hello"


def test_string_transform_reverse():
    """Test reverse transformation."""
    assert string_transform("hello", "reverse") == "olleh"


def test_string_transform_length():
    """Test length transformation."""
    assert string_transform("hello", "length") == 5


def test_string_transform_word_count():
    """Test word count transformation."""
    assert string_transform("hello world test", "word_count") == 3


def test_string_transform_invalid_operation():
    """Test invalid operation raises error."""
    with pytest.raises(ValueError, match="Invalid operation"):
        string_transform("test", "invalid")


def test_generate_uuid_v1():
    """Test UUID v1 generation."""
    result = generate_uuid(1)
    assert isinstance(result, str)
    assert len(result) == 36
    assert result.count("-") == 4


def test_generate_uuid_v4():
    """Test UUID v4 generation."""
    result = generate_uuid(4)
    assert isinstance(result, str)
    assert len(result) == 36


def test_generate_uuid_v4_default():
    """Test UUID v4 is default."""
    result = generate_uuid()
    assert isinstance(result, str)
    assert len(result) == 36


def test_generate_uuid_v5():
    """Test UUID v5 generation."""
    result = generate_uuid(5, namespace="dns", name="example.com")
    assert isinstance(result, str)
    assert len(result) == 36


def test_generate_uuid_v5_missing_params():
    """Test UUID v5 without required params raises error."""
    with pytest.raises(ValueError, match="requires both"):
        generate_uuid(5)


def test_generate_uuid_invalid_version():
    """Test invalid UUID version raises error."""
    with pytest.raises(ValueError, match="Invalid version"):
        generate_uuid(3)


def test_generate_uuid_v5_invalid_namespace():
    """Test UUID v5 with invalid namespace raises error."""
    with pytest.raises(ValueError, match="Invalid namespace"):
        generate_uuid(5, namespace="invalid", name="test")


def test_list_operations():
    """Test listing operations."""
    result = list_operations()
    assert isinstance(result, dict)
    assert "get_current_time" in result
    assert "calculate" in result
    assert "string_transform" in result
    assert "generate_uuid" in result
    assert "list_operations" in result
    assert len(result) == 5
