# Documentation Index

Welcome to the Agent Framework documentation!

## Core Documentation

### Getting Started
- **[../README.md](../README.md)** - Main project documentation, quick start guide

### Development Guides
- **[TOOL_DEVELOPMENT_GUIDE.md](TOOL_DEVELOPMENT_GUIDE.md)** - Comprehensive guide for creating custom tools
- **[LLM_CONFIGURATION_GUIDE.md](LLM_CONFIGURATION_GUIDE.md)** - Configure different LLM providers

### Examples
- **[../examples_llm.py](../examples_llm.py)** - Working examples for all supported LLMs
- **[../main.py](../main.py)** - Full example agent implementation

## Architecture

### Module Structure

```
agent_framework/
├── core.py              # Goal, Action, Memory, Environment
├── tool_registry.py     # Tool registration system
├── agent_language.py    # LLM communication interfaces
├── agent.py             # Main Agent class
├── config.py            # LLM provider configurations
└── tools/               # Plugin-style tool modules
    ├── file_tools.py
    ├── system_tools.py
    ├── text_tools.py
    └── _template.py
```

## Quick Links

| Topic | File |
|-------|------|
| Creating Tools | [TOOL_DEVELOPMENT_GUIDE.md](TOOL_DEVELOPMENT_GUIDE.md) |
| LLM Configuration | [LLM_CONFIGURATION_GUIDE.md](LLM_CONFIGURATION_GUIDE.md) |
| API Reference | See inline docstrings in modules |
| Examples | [../examples_llm.py](../examples_llm.py) |

## Additional Resources

### Tool Categories
- **File Operations**: Read, write, list files
- **System Tools**: System info, commands, env vars
- **Text Tools**: String manipulation, analysis

### Supported LLM Providers
- Google Gemini
- OpenAI GPT-4/3.5
- Anthropic Claude
- Ollama (Local)
- Azure OpenAI
- Custom providers

## Contributing

When adding new documentation:
1. Place `.md` files in this `docs/` directory
2. Update this index
3. Link from the main README if needed
4. Follow the existing documentation style

## Support

- Issues: Report on GitHub
- Questions: Check existing documentation first
- Examples: See `examples_llm.py` for working code
