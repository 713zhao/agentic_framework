# LLM Configuration Guide

This guide shows you how to configure and switch between different LLM providers in the agent framework.

## Quick Start

```python
from agent_framework import Agent, GEMINI_FLASH, generate_response

agent = Agent(
    goals=[...],
    action_registry=...,
    generate_response=generate_response,
    llm_config=GEMINI_FLASH  # Just pass the config!
)
```

## Available LLM Providers

### 1. Google Gemini (via LiteLLM)

**Setup:**
```bash
export Gemini_key="your-api-key"
```

**Usage:**
```python
from agent_framework import GeminiConfig, GEMINI_FLASH, GEMINI_PRO

# Option 1: Use presets
llm_config = GEMINI_FLASH  # Fast, efficient
llm_config = GEMINI_PRO    # More powerful

# Option 2: Custom configuration
llm_config = GeminiConfig(
    model="gemini/gemini-1.5-pro",
    temperature=0.7,
    max_tokens=2048
)
```

### 2. OpenAI GPT

**Setup:**
```bash
export OPENAI_API_KEY="your-api-key"
```

**Usage:**
```python
from agent_framework import OpenAIConfig, GPT4O, GPT4O_MINI

# Option 1: Use presets
llm_config = GPT4O       # GPT-4 Optimized
llm_config = GPT4O_MINI  # Faster, cheaper

# Option 2: Custom configuration
llm_config = OpenAIConfig(
    model="openai/gpt-4o",
    temperature=0.5,
    max_tokens=1024
)
```

### 3. Ollama (Local Models)

**Setup:**
```bash
# Start Ollama server
ollama serve

# Pull a model
ollama pull llama3.2
```

**Usage:**
```python
from agent_framework import OllamaConfig, LLAMA_LOCAL, create_ollama_config

# Option 1: Use preset
llm_config = LLAMA_LOCAL

# Option 2: Custom local model
llm_config = create_ollama_config(
    model="ollama/mistral",
    api_base="http://localhost:11434",
    temperature=0.7
)

# Option 3: Full customization
llm_config = OllamaConfig(
    model="ollama/llama3.2",
    api_base="http://localhost:11434",
    temperature=0.8,
    max_tokens=2048
)
```

### 4. Anthropic Claude

**Setup:**
```bash
export ANTHROPIC_API_KEY="your-api-key"
```

**Usage:**
```python
from agent_framework import AnthropicConfig, CLAUDE_SONNET

# Option 1: Use preset
llm_config = CLAUDE_SONNET

# Option 2: Custom configuration
llm_config = AnthropicConfig(
    model="anthropic/claude-3-5-sonnet-20241022",
    temperature=0.6,
    max_tokens=1024
)
```

### 5. Azure OpenAI

**Setup:**
```bash
export AZURE_API_KEY="your-api-key"
```

**Usage:**
```python
from agent_framework import AzureOpenAIConfig, create_azure_config

llm_config = create_azure_config(
    model="azure/gpt-4o",
    api_base="https://your-resource.openai.azure.com",
    api_version="2024-02-15-preview"
)
```

### 6. Custom LLM Provider

**For any custom implementation:**
```python
from agent_framework import CustomLLMConfig

def my_custom_completion(prompt):
    """Your custom LLM logic."""
    # Process prompt
    # Return JSON string with tool call or text
    return '{"tool": "terminate", "args": {"message": "Done"}}'

llm_config = CustomLLMConfig(
    provider="custom",
    model="my-model",
    completion_function=my_custom_completion
)
```

## Configuration Options

All LLM configurations support these parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | str | varies | Model identifier |
| `api_key` | str | None | API key (auto-loads from env if None) |
| `api_base` | str | None | Custom API endpoint |
| `max_tokens` | int | 1024 | Maximum tokens in response |
| `temperature` | float | 0.7 | Randomness (0.0 = deterministic, 1.0 = creative) |
| `extra_params` | dict | {} | Provider-specific extra parameters |

### Example with all options:
```python
llm_config = GeminiConfig(
    model="gemini/gemini-1.5-pro",
    api_key="explicit-key",  # Optional, reads from env by default
    max_tokens=2048,
    temperature=0.8,
    extra_params={
        "top_p": 0.9,
        "top_k": 40
    }
)
```

## Switching Between Providers

### In your main script:
```python
from agent_framework import (
    GEMINI_FLASH,
    GPT4O,
    LLAMA_LOCAL,
    Agent,
    generate_response
)

# Just change this line!
llm_config = GEMINI_FLASH  # Switch to GPT4O or LLAMA_LOCAL

agent = Agent(
    goals=[...],
    action_registry=...,
    generate_response=generate_response,
    llm_config=llm_config
)
```

### Runtime switching:
```python
# Create different agents with different models
gemini_agent = Agent(..., llm_config=GEMINI_FLASH)
gpt_agent = Agent(..., llm_config=GPT4O)
local_agent = Agent(..., llm_config=LLAMA_LOCAL)

# Use based on task requirements
if task == "creative":
    result = gemini_agent.run(query)
elif task == "analytical":
    result = gpt_agent.run(query)
else:
    result = local_agent.run(query)
```

## Preset Configurations

Quick reference for built-in presets:

```python
from agent_framework import (
    GEMINI_FLASH,    # Google Gemini Flash 2.5
    GEMINI_PRO,      # Google Gemini Pro 1.5
    GPT4O,           # OpenAI GPT-4o
    GPT4O_MINI,      # OpenAI GPT-4o Mini
    CLAUDE_SONNET,   # Claude 3.5 Sonnet
    LLAMA_LOCAL,     # Local Llama 3.2 via Ollama
)
```

## Environment Variables

The framework automatically looks for these environment variables:

| Provider | Environment Variable |
|----------|---------------------|
| Gemini | `Gemini_key` or `GEMINI_API_KEY` |
| OpenAI | `OPENAI_API_KEY` |
| Anthropic | `ANTHROPIC_API_KEY` |
| Azure | `AZURE_API_KEY` |
| Ollama | None (local) |

## Examples

See [examples_llm.py](examples_llm.py) for complete working examples including:
- Basic usage for each provider
- Comparing multiple LLMs
- Custom LLM implementations
- Error handling

Run it:
```bash
python examples_llm.py
```

## Best Practices

### 1. Use Presets for Quick Development
```python
llm_config = GEMINI_FLASH  # Fast and easy
```

### 2. Custom Configs for Production
```python
llm_config = GeminiConfig(
    model="gemini/gemini-1.5-pro",
    temperature=0.3,  # More consistent
    max_tokens=4096   # Longer responses
)
```

### 3. Local Models for Privacy
```python
llm_config = LLAMA_LOCAL  # Everything stays local
```

### 4. Cost Optimization
```python
# Use cheaper models for simple tasks
simple_config = GPT4O_MINI

# Use powerful models for complex reasoning
complex_config = GPT4O
```

### 5. Fallback Strategy
```python
def create_agent_with_fallback():
    try:
        return Agent(..., llm_config=GEMINI_FLASH)
    except Exception:
        # Fallback to local model
        return Agent(..., llm_config=LLAMA_LOCAL)
```

## Troubleshooting

### API Key Not Found
```python
# Explicit key setting
import os
os.environ['GEMINI_API_KEY'] = 'your-key'

# Or in config
llm_config = GeminiConfig(api_key='your-key')
```

### Ollama Connection Error
```bash
# Make sure Ollama is running
ollama serve

# Check it's accessible
curl http://localhost:11434
```

### Model Not Available
```python
# Check available models
# For Ollama:
ollama list

# For OpenAI/Gemini: Check their documentation
```

### Rate Limits
```python
# Reduce request rate
llm_config = GeminiConfig(
    extra_params={"timeout": 60}
)

# Or use local models
llm_config = LLAMA_LOCAL
```

## Next Steps

1. Try different providers with [examples_llm.py](examples_llm.py)
2. Set up your preferred provider's API key
3. Experiment with temperature and max_tokens
4. Consider local models (Ollama) for privacy-sensitive tasks
5. Build your agent with the right LLM for your use case!
