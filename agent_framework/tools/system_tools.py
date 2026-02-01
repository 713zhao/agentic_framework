"""System and process management tools."""

import os
import sys
import subprocess
from typing import Dict, Any

from ..tool_registry import register_tool


@register_tool(tags=["system", "info"])
def get_system_info() -> Dict[str, str]:
    """Get basic system information.
    
    Returns information about the current system including:
    - Operating system
    - Python version
    - Current working directory
    
    Returns:
        Dictionary containing system information
    """
    import platform
    
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "python_version": sys.version,
        "cwd": os.getcwd(),
        "platform": platform.platform()
    }


@register_tool(tags=["system", "process"])
def run_command(command: str) -> Dict[str, Any]:
    """Execute a shell command and return the output.
    
    WARNING: Use with caution! Only execute trusted commands.
    
    Args:
        command: The shell command to execute
        
    Returns:
        Dictionary with stdout, stderr, and return code
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Command timed out after 30 seconds"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@register_tool(tags=["system", "env"])
def get_environment_variable(name: str) -> str:
    """Get the value of an environment variable.
    
    Args:
        name: The name of the environment variable
        
    Returns:
        The value of the environment variable, or an error message
    """
    value = os.environ.get(name)
    if value is None:
        return f"Environment variable '{name}' not found"
    return value
