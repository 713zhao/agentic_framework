# Agent Framework

A modular Python framework for building LLM-powered agents with goals, actions, memory, and environment execution.

## Project Structure

```
agent_framework/
├── __init__.py              # Package initialization and exports
├── core.py                  # Core data structures (Goal, Action, Memory, Environment)
├── tools.py                 # Tool registration system and decorators
├── agent_language.py        # Language interfaces and prompt formatting
├── agent.py                 # Main Agent class and PythonActionRegistry
└── tools/                   # 🔥 Plugin-style tools directory
    ├── __init__.py          # Auto-discovery of all tool modules
    ├── file_tools.py        # File operation tools
    ├── system_tools.py      # System and process tools
    ├── text_tools.py        # Text manipulation tools
    └── _template.py         # Template for creating new tools

main.py                      # Example usage and execution script
TOOL_DEVELOPMENT_GUIDE.md    # Comprehensive guide for creating tools
```

## ✨ Key Features

- **Modular Architecture**: Separate concerns into focused modules
- **Plugin-Style Tools**: Drop Python files in `tools/` folder - automatic discovery! 
- **Configurable LLM Providers**: Easy switching between Gemini, OpenAI, Ollama, Claude, and more
- **Tool Registration**: Simple decorator-based system for registering functions
- **Flexible Language Interface**: Support for different LLM communication patterns
- **Memory Management**: Track conversation history and agent decisions
- **Tag-Based Tool Filtering**: Load only the tools you need
- **Built-in Tools**: Ready-to-use tools for files, system, and text operations

## 🚀 Quick Start

### Installation

```bash
pip install litellm
```

Set your API key (for Gemini):
```bash
export Gemini_key="your-api-key-here"
```

Or use other providers - see [LLM_CONFIGURATION_GUIDE.md](LLM_CONFIGURATION_GUIDE.md)

### Basic Usage

```python
from agent_framework import (
    Goal, Agent, AgentFunctionCallingActionLanguage,
    PythonActionRegistry, Environment, generate_response,
    GEMINI_FLASH  # Or GPT4O, LLAMA_LOCAL, etc.
)

# Define goals
goals = [
    Goal(priority=1, name="Task", description="Do something useful")
]

# Create and run agent (tools auto-loaded!)
agent = Agent(
    goals=goals,
    agent_language=AgentFunctionCallingActionLanguage(),
    action_registry=PythonActionRegistry(tags=["file_operations", "system"]),
    generate_response=generate_response,
    environment=Environment(),
    llm_config=GEMINI_FLASH  # Easy LLM switching!
)

memory = agent.run("Your task here")
```

## 🤖 Switching LLM Providers

Easily switch between different LLM providers:

```python
from agent_framework import (
    GEMINI_FLASH,    # Google Gemini (default)
    GPT4O,           # OpenAI GPT-4
    CLAUDE_SONNET,   # Anthropic Claude
    LLAMA_LOCAL,     # Local Ollama
)

# Just change the config!
agent = Agent(
    ...,
    llm_config=LLAMA_LOCAL  # Use local model
)
```

**Supported Providers:**
- ✅ Google Gemini (via LiteLLM)
- ✅ OpenAI GPT-4/GPT-3.5
- ✅ Anthropic Claude
- ✅ Ollama (local models)
- ✅ Azure OpenAI
- ✅ Custom LLM providers

See [LLM_CONFIGURATION_GUIDE.md](docs/LLM_CONFIGURATION_GUIDE.md) for detailed setup and examples.

## 🔧 Creating Custom Tools (Super Easy!)

### Method 1: Drop-in File (Recommended)

Create `agent_framework/tools/my_tools.py`:

```python
from ..tools import register_tool

@register_tool(tags=["math"])
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b
```

**That's it!** The tool is automatically discovered and available.

### Method 2: Use the Template

1. Copy `agent_framework/tools/_template.py`
2. Rename it (e.g., `weather_tools.py`)
3. Add your functions with `@register_tool` decorator
4. Done!

See [TOOL_DEVELOPMENT_GUIDE.md](docs/TOOL_DEVELOPMENT_GUIDE.md) for detailed examples.

## 📦 Available Tool Categories

| Module | Tags | Description |
|--------|------|-------------|
| `file_tools.py` | `file_operations`, `read`, `list` | Read files, list directories |
| `system_tools.py` | `system`, `info`, `process`, `env` | System info, run commands, env vars |
| `text_tools.py` | `text`, `string`, `analysis` | String manipulation, word count, search |

Load specific tools:
```python
# Only file and system tools
PythonActionRegistry(tags=["file_operations", "system"])

# Only text tools
PythonActionRegistry(tags=["text"])

# Load specific tools by name
PythonActionRegistry(tool_names=["read_project_file", "get_system_info"])
```

## 📚 Documentation

- **[docs/TOOL_DEVELOPMENT_GUIDE.md](docs/TOOL_DEVELOPMENT_GUIDE.md)** - Complete guide to creating custom tools
- **[docs/LLM_CONFIGURATION_GUIDE.md](docs/LLM_CONFIGURATION_GUIDE.md)** - Configure different LLM providers
- **[examples_llm.py](examples_llm.py)** - Working examples for all supported LLMs
- **[main.py](main.py)** - Full example agent implementation

## 🎯 Running Examples

```bash
# Basic agent with Gemini
python main.py

# Try different LLM providers
python examples_llm.py
```

## 📖 Architecture Overview

### Core Modules

| Module | Purpose |
|--------|---------|
| `core.py` | Goal, Action, Memory, Environment classes |
| `tools.py` | Tool registration and metadata system |
| `agent_language.py` | Prompt formatting and LLM communication |
| `agent.py` | Main Agent class and registries |
| `config.py` | LLM provider configurations |
| `tools/` | Plugin directory for tool modules |

## License

MIT
