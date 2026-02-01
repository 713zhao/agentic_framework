"""Agent framework package for building LLM-powered agents."""

from .core import Goal, Action, ActionRegistry, Memory, Environment
from .tool_registry import register_tool
from .agent_language import (
    Prompt,
    AgentLanguage,
    AgentFunctionCallingActionLanguage,
    generate_response
)
from .agent import Agent, PythonActionRegistry
from .config import (
    LLMConfig,
    GeminiConfig,
    OpenAIConfig,
    OllamaConfig,
    AnthropicConfig,
    AzureOpenAIConfig,
    CustomLLMConfig,
    create_gemini_config,
    create_openai_config,
    create_ollama_config,
    create_anthropic_config,
    create_azure_config,
    GEMINI_FLASH,
    GEMINI_PRO,
    GPT4O,
    GPT4O_MINI,
    CLAUDE_SONNET,
    LLAMA_LOCAL
)

# Auto-load all tools from the tools directory first
from . import tools as tools_package

# Now import the populated registries
from .tool_registry import tools, tools_by_tag

__all__ = [
    # Core classes
    'Goal',
    'Action',
    'ActionRegistry',
    'Memory',
    'Environment',
    
    # Tool system
    'register_tool',
    'tools',
    'tools_by_tag',
    
    # Language interfaces
    'Prompt',
    'AgentLanguage',
    'AgentFunctionCallingActionLanguage',
    'generate_response',
    
    # Agent classes
    'Agent',
    'PythonActionRegistry',
    
    # LLM Configuration
    'LLMConfig',
    'GeminiConfig',
    'OpenAIConfig',
    'OllamaConfig',
    'AnthropicConfig',
    'AzureOpenAIConfig',
    'CustomLLMConfig',
    'create_gemini_config',
    'create_openai_config',
    'create_ollama_config',
    'create_anthropic_config',
    'create_azure_config',
    'GEMINI_FLASH',
    'GEMINI_PRO',
    'GPT4O',
    'GPT4O_MINI',
    'CLAUDE_SONNET',
    'LLAMA_LOCAL',
]
