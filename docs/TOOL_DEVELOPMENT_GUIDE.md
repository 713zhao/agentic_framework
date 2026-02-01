# Creating Custom Tools Guide

This guide shows you how to extend the agent framework with custom tools.

## Quick Start

1. **Create a new file** in `agent_framework/tools/` (e.g., `my_tools.py`)
2. **Import the decorator**: `from ..tools import register_tool`
3. **Decorate your functions**: `@register_tool(tags=["category"])`
4. **Done!** Tools are automatically discovered and available

## Example: Creating a Math Tools Module

Create `agent_framework/tools/math_tools.py`:

```python
from ..tools import register_tool

@register_tool(tags=["math"])
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@register_tool(tags=["math"])
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b
```

That's it! These tools are now available to your agents.

## Tool Registration Options

### Basic Registration
```python
@register_tool(tags=["category"])
def my_tool(param: str) -> str:
    """Tool description for the LLM."""
    return f"Result: {param}"
```

### Advanced Registration
```python
@register_tool(
    tool_name="custom_name",           # Override function name
    description="Custom description",   # Override docstring
    tags=["tag1", "tag2"],             # Multiple tags
    terminal=False,                     # Set to True to end agent loop
    parameters_override={               # Custom JSON schema
        "type": "object",
        "properties": {
            "param": {"type": "string", "maxLength": 100}
        },
        "required": ["param"]
    }
)
def my_advanced_tool(param: str) -> str:
    return f"Result: {param}"
```

## Type Hints (Automatic Schema Generation)

The framework automatically converts Python type hints to JSON schema:

| Python Type | JSON Type |
|-------------|-----------|
| `str`       | `"string"` |
| `int`       | `"integer"` |
| `float`     | `"number"` |
| `bool`      | `"boolean"` |
| `list`      | `"array"` |
| `dict`      | `"object"` |

Example:
```python
@register_tool(tags=["data"])
def process_data(
    name: str,
    count: int,
    enabled: bool = True
) -> dict:
    """Process data with various types."""
    return {
        "name": name,
        "count": count,
        "enabled": enabled
    }
```

## Using Tags to Filter Tools

Tags let you load only specific tools for different agents:

```python
# Load only file operation tools
agent = Agent(
    goals=[...],
    action_registry=PythonActionRegistry(tags=["file_operations"]),
    ...
)

# Load multiple categories
agent = Agent(
    goals=[...],
    action_registry=PythonActionRegistry(tags=["math", "text", "system"]),
    ...
)

# Load specific tools by name
agent = Agent(
    goals=[...],
    action_registry=PythonActionRegistry(tool_names=["add", "multiply"]),
    ...
)
```

## Tool Organization Best Practices

### 1. Group Related Tools
```
agent_framework/tools/
├── file_tools.py      # File operations
├── math_tools.py      # Mathematical operations
├── text_tools.py      # Text manipulation
├── api_tools.py       # API interactions
└── database_tools.py  # Database operations
```

### 2. Use Descriptive Tags
```python
# Good: Specific, hierarchical tags
@register_tool(tags=["api", "weather"])
@register_tool(tags=["database", "read"])
@register_tool(tags=["file", "json"])

# Less Good: Too generic
@register_tool(tags=["tools"])
@register_tool(tags=["helper"])
```

### 3. Write Clear Docstrings
```python
@register_tool(tags=["text"])
def count_words(text: str) -> int:
    """Count the number of words in a text string.
    
    Splits the text by whitespace and returns the count.
    Empty strings return 0.
    
    Args:
        text: The text to count words in
        
    Returns:
        The number of words found
    """
    return len(text.split()) if text else 0
```

## Available Tool Modules

### Current Built-in Tools

- **file_tools.py**: File operations (read, list, terminate)
- **system_tools.py**: System info, command execution, environment variables
- **text_tools.py**: String manipulation, text analysis

### Template

See `agent_framework/tools/_template.py` for a comprehensive template with examples.

## Disabling Specific Tools

To temporarily disable a tool without deleting it:

1. Rename the file to start with underscore: `_disabled_tools.py`
2. Or move it out of the tools directory
3. Or comment out the `@register_tool` decorator

## Viewing Available Tools

```python
from agent_framework import tools, tools_by_tag

# View all registered tools
print(tools.keys())

# View tools by tag
print(tools_by_tag["math"])
print(tools_by_tag["file_operations"])

# Get tool details
tool_info = tools["read_project_file"]
print(tool_info["description"])
print(tool_info["parameters"])
print(tool_info["tags"])
```

## Example: Complete Custom Tool Module

```python
# agent_framework/tools/weather_tools.py
"""Weather-related tools for the agent."""

from typing import Dict, Any
from ..tools import register_tool

@register_tool(tags=["weather", "api"])
def get_weather(city: str) -> Dict[str, Any]:
    """Get current weather for a city.
    
    Args:
        city: Name of the city
        
    Returns:
        Weather information dictionary
    """
    # Your API call here
    return {
        "city": city,
        "temperature": 72,
        "condition": "sunny"
    }

@register_tool(tags=["weather", "forecast"])
def get_forecast(city: str, days: int = 3) -> list:
    """Get weather forecast for upcoming days.
    
    Args:
        city: Name of the city
        days: Number of days to forecast (default: 3)
        
    Returns:
        List of daily forecasts
    """
    # Your forecast logic here
    return [
        {"day": 1, "temp": 72, "condition": "sunny"},
        {"day": 2, "temp": 68, "condition": "cloudy"},
        {"day": 3, "temp": 70, "condition": "partly cloudy"}
    ]
```

Then use it:
```python
agent = Agent(
    goals=[Goal(priority=1, name="Weather", description="Get weather info")],
    action_registry=PythonActionRegistry(tags=["weather"]),
    ...
)
```

## Troubleshooting

### Tool Not Found
- Check file name doesn't start with `_`
- Ensure `@register_tool` decorator is used
- Verify the file is in `agent_framework/tools/`
- Check for import errors in the module

### Tool Not Available to Agent
- Verify tags match in `PythonActionRegistry(tags=[...])`
- Or use `tool_names` parameter to explicitly include it
- Check tool is actually registered: `print(tools.keys())`

## Next Steps

1. Browse `agent_framework/tools/_template.py` for examples
2. Create your first custom tool module
3. Test it independently before using with agents
4. Share useful tools with your team!
