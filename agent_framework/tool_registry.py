"""Tool registration system for dynamic function registration with metadata."""

import inspect
from typing import get_type_hints, List, Dict, Callable, Any

# Global tool registries
tools = {}
tools_by_tag = {}


def to_openai_tools(tools_metadata: List[dict]) -> List[dict]:
    """Convert tool metadata to OpenAI tool format.
    
    Args:
        tools_metadata: List of tool metadata dictionaries
        
    Returns:
        List of tools in OpenAI format
    """
    openai_tools = [
        {
            "type": "function",
            "function": {
                "name": t['tool_name'],
                "description": t.get('description', "")[:1024],
                "parameters": t.get('parameters', {}),
            },
        } for t in tools_metadata
    ]
    return openai_tools


def get_tool_metadata(
    func: Callable,
    tool_name: str = None,
    description: str = None,
    parameters_override: dict = None,
    terminal: bool = False,
    tags: List[str] = None
) -> dict:
    """Extract metadata for a function to use in tool registration.

    Args:
        func: The function to extract metadata from
        tool_name: The name of the tool (defaults to function name)
        description: Description of the tool (defaults to docstring)
        parameters_override: Override for the argument schema
        terminal: Whether the tool is terminal
        tags: List of tags to associate with the tool

    Returns:
        Dictionary containing tool metadata
    """
    tool_name = tool_name or func.__name__
    description = description or (func.__doc__.strip() if func.__doc__ else "No description provided.")

    if parameters_override is None:
        signature = inspect.signature(func)
        type_hints = get_type_hints(func)

        args_schema = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        for param_name, param in signature.parameters.items():
            if param_name in ["action_context", "action_agent"]:
                continue

            def get_json_type(param_type):
                type_map = {
                    str: "string",
                    int: "integer",
                    float: "number",
                    bool: "boolean",
                    list: "array",
                    dict: "object"
                }
                return type_map.get(param_type, "string")

            param_type = type_hints.get(param_name, str)
            param_schema = {"type": get_json_type(param_type)}
            args_schema["properties"][param_name] = param_schema

            if param.default == inspect.Parameter.empty:
                args_schema["required"].append(param_name)
    else:
        args_schema = parameters_override

    return {
        "tool_name": tool_name,
        "description": description,
        "parameters": args_schema,
        "function": func,
        "terminal": terminal,
        "tags": tags or []
    }


def register_tool(
    tool_name: str = None,
    description: str = None,
    parameters_override: dict = None,
    terminal: bool = False,
    tags: List[str] = None
):
    """Decorator to dynamically register a function in the tools dictionary.

    Args:
        tool_name: The name of the tool to register (defaults to function name)
        description: Override for the tool's description
        parameters_override: Override for the argument schema
        terminal: Whether the tool is terminal
        tags: List of tags to associate with the tool

    Returns:
        The wrapped function
    """
    def decorator(func):
        metadata = get_tool_metadata(
            func=func,
            tool_name=tool_name,
            description=description,
            parameters_override=parameters_override,
            terminal=terminal,
            tags=tags
        )

        tools[metadata["tool_name"]] = {
            "description": metadata["description"],
            "parameters": metadata["parameters"],
            "function": metadata["function"],
            "terminal": metadata["terminal"],
            "tags": metadata["tags"] or []
        }

        for tag in metadata["tags"]:
            if tag not in tools_by_tag:
                tools_by_tag[tag] = []
            tools_by_tag[tag].append(metadata["tool_name"])

        return func
    return decorator
