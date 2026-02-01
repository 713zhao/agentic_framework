"""
Template for creating new tool modules.

Copy this file and rename it to create your own tool module.
Example: my_custom_tools.py

All tools defined here will be automatically discovered and registered
when the agent framework is imported.
"""

from typing import Any

from ..tool_registry import register_tool


# Example 1: Simple tool with no parameters
@register_tool(tags=["example"], terminal=False)
def example_tool() -> str:
    """A simple example tool that returns a greeting.
    
    This docstring will be used as the tool description for the LLM.
    Be clear and concise about what the tool does.
    
    Returns:
        A greeting message
    """
    return "Hello from example tool!"


# Example 2: Tool with parameters
@register_tool(tags=["example", "math"])
def calculate_sum(a: int, b: int) -> int:
    """Add two numbers together.
    
    The type hints (int, str, float, bool, list, dict) are automatically
    converted to JSON schema for the LLM.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The sum of a and b
    """
    return a + b


# Example 3: Terminal tool (ends agent execution)
@register_tool(tags=["example"], terminal=True)
def example_terminate(message: str) -> str:
    """Example of a terminal tool that ends execution.
    
    Terminal tools stop the agent loop when called.
    Useful for cleanup, final reports, etc.
    
    Args:
        message: Final message to return
        
    Returns:
        The formatted final message
    """
    return f"Terminating with message: {message}"


# Example 4: Tool with custom parameter schema
@register_tool(
    tags=["example", "custom"],
    description="Custom description override",
    parameters_override={
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "The name to process"
            },
            "count": {
                "type": "integer",
                "description": "How many times to repeat",
                "minimum": 1,
                "maximum": 10
            }
        },
        "required": ["name"]
    }
)
def advanced_tool(name: str, count: int = 1) -> str:
    """Advanced tool with custom parameter schema.
    
    You can override the automatically generated schema if you need
    more control over parameter validation.
    
    Args:
        name: Name to process
        count: Repetition count (default: 1)
        
    Returns:
        Processed result
    """
    return f"{name} " * count


# Best Practices:
# 1. Use clear, descriptive function names
# 2. Add comprehensive docstrings (they become tool descriptions)
# 3. Use type hints for automatic schema generation
# 4. Tag tools logically for easy filtering
# 5. Handle errors gracefully and return informative messages
# 6. Keep tools focused on a single responsibility
# 7. Test tools independently before using with agents
