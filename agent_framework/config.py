"""LLM configuration for different providers."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Callable
import os


@dataclass
class LLMConfig:
    """Base configuration for LLM providers."""
    
    provider: str
    model: str
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    max_tokens: int = 1024
    temperature: float = 0.7
    extra_params: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate and set up configuration."""
        if self.api_key is None:
            self.api_key = self._get_api_key_from_env()
    
    def _get_api_key_from_env(self) -> Optional[str]:
        """Get API key from environment variables."""
        return None
    
    def to_completion_params(self) -> Dict[str, Any]:
        """Convert config to parameters for completion call."""
        params = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }
        
        if self.api_base:
            params["api_base"] = self.api_base
        
        params.update(self.extra_params)
        return params


@dataclass
class GeminiConfig(LLMConfig):
    """Configuration for Google Gemini via LiteLLM."""
    
    provider: str = "gemini"
    model: str = "gemini/gemini-2.5-flash"
    
    def _get_api_key_from_env(self) -> Optional[str]:
        """Get Gemini API key from environment."""
        key = os.environ.get('Gemini_key') or os.environ.get('GEMINI_API_KEY')
        if key:
            os.environ['GEMINI_API_KEY'] = key
        return key


@dataclass
class OpenAIConfig(LLMConfig):
    """Configuration for OpenAI."""
    
    provider: str = "openai"
    model: str = "openai/gpt-4o"
    
    def _get_api_key_from_env(self) -> Optional[str]:
        """Get OpenAI API key from environment."""
        return os.environ.get('OPENAI_API_KEY')


@dataclass
class OllamaConfig(LLMConfig):
    """Configuration for Ollama (local models)."""
    
    provider: str = "ollama"
    model: str = "ollama/llama3.2"
    api_base: str = "http://localhost:11434"
    
    def _get_api_key_from_env(self) -> Optional[str]:
        """Ollama doesn't require API key."""
        return None
    
    def to_completion_params(self) -> Dict[str, Any]:
        """Ollama-specific completion parameters."""
        params = super().to_completion_params()
        # Ollama uses api_base for local server
        params["api_base"] = self.api_base
        return params


@dataclass
class AnthropicConfig(LLMConfig):
    """Configuration for Anthropic Claude."""
    
    provider: str = "anthropic"
    model: str = "anthropic/claude-3-5-sonnet-20241022"
    
    def _get_api_key_from_env(self) -> Optional[str]:
        """Get Anthropic API key from environment."""
        return os.environ.get('ANTHROPIC_API_KEY')


@dataclass
class AzureOpenAIConfig(LLMConfig):
    """Configuration for Azure OpenAI."""
    
    provider: str = "azure"
    model: str = "azure/gpt-4o"
    api_base: Optional[str] = None  # e.g., "https://your-resource.openai.azure.com"
    api_version: str = "2024-02-15-preview"
    
    def _get_api_key_from_env(self) -> Optional[str]:
        """Get Azure OpenAI API key from environment."""
        return os.environ.get('AZURE_API_KEY')
    
    def to_completion_params(self) -> Dict[str, Any]:
        """Azure-specific completion parameters."""
        params = super().to_completion_params()
        if self.api_base:
            params["api_base"] = self.api_base
        params["api_version"] = self.api_version
        return params


@dataclass
class CustomLLMConfig(LLMConfig):
    """Configuration for custom LLM providers."""
    
    provider: str = "custom"
    model: str = "custom-model"
    completion_function: Optional[Callable] = None
    
    def __post_init__(self):
        """Validate custom configuration."""
        super().__post_init__()
        if self.completion_function is None:
            raise ValueError("CustomLLMConfig requires completion_function")


# Convenience factory functions
def create_gemini_config(
    model: str = "gemini/gemini-2.5-flash",
    **kwargs
) -> GeminiConfig:
    """Create Gemini configuration."""
    return GeminiConfig(model=model, **kwargs)


def create_openai_config(
    model: str = "openai/gpt-4o",
    **kwargs
) -> OpenAIConfig:
    """Create OpenAI configuration."""
    return OpenAIConfig(model=model, **kwargs)


def create_ollama_config(
    model: str = "ollama/llama3.2",
    api_base: str = "http://localhost:11434",
    **kwargs
) -> OllamaConfig:
    """Create Ollama configuration."""
    return OllamaConfig(model=model, api_base=api_base, **kwargs)


def create_anthropic_config(
    model: str = "anthropic/claude-3-5-sonnet-20241022",
    **kwargs
) -> AnthropicConfig:
    """Create Anthropic configuration."""
    return AnthropicConfig(model=model, **kwargs)


def create_azure_config(
    model: str = "azure/gpt-4o",
    api_base: str = None,
    **kwargs
) -> AzureOpenAIConfig:
    """Create Azure OpenAI configuration."""
    return AzureOpenAIConfig(model=model, api_base=api_base, **kwargs)


# Quick presets
GEMINI_FLASH = GeminiConfig(model="gemini/gemini-2.5-flash")
GEMINI_PRO = GeminiConfig(model="gemini/gemini-1.5-pro")
GPT4O = OpenAIConfig(model="openai/gpt-4o")
GPT4O_MINI = OpenAIConfig(model="openai/gpt-4o-mini")
CLAUDE_SONNET = AnthropicConfig(model="anthropic/claude-3-5-sonnet-20241022")
LLAMA_LOCAL = OllamaConfig(model="ollama/llama3.2")
