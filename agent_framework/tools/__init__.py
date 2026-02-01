"""
Tools package for agent framework.

This package provides a plugin-style architecture for tools:
- Drop any Python file in this directory
- Use @register_tool decorator on functions
- They'll be automatically discovered and available to agents

To create a new tool module:
1. Create a new .py file in this directory (e.g., my_tools.py)
2. Import the register_tool decorator
3. Decorate your functions with @register_tool()
4. That's it! Tools are automatically registered on import.
"""

import os
import importlib
from pathlib import Path


def load_all_tools():
    """
    Automatically discover and import all tool modules in this directory.
    
    This function scans the tools directory and imports all Python files
    (except __init__.py and files starting with _), which triggers the
    @register_tool decorators and registers all tools.
    """
    tools_dir = Path(__file__).parent
    
    # Find all Python files in the tools directory
    tool_files = [
        f.stem for f in tools_dir.glob("*.py")
        if f.is_file() 
        and f.stem != "__init__"
        and not f.stem.startswith("_")
    ]
    
    # Import each tool module to trigger registration
    imported_modules = []
    for tool_module in tool_files:
        try:
            module = importlib.import_module(f".{tool_module}", package="agent_framework.tools")
            imported_modules.append(tool_module)
        except Exception as e:
            print(f"Warning: Failed to import tool module '{tool_module}': {e}")
    
    return imported_modules


# Automatically load all tools when this package is imported
_loaded_tools = load_all_tools()

__all__ = ['load_all_tools']
