"""Examples of using different LLM providers with the agent framework."""

import os
from agent_framework import (
    Goal,
    Agent,
    AgentFunctionCallingActionLanguage,
    PythonActionRegistry,
    Environment,
    generate_response,
    # Import configurations
    GeminiConfig,
    OpenAIConfig,
    OllamaConfig,
    AnthropicConfig,
    create_ollama_config,
    GEMINI_FLASH,
    GEMINI_PRO,
    GPT4O,
    GPT4O_MINI,
    LLAMA_LOCAL,
)


def create_agent_with_llm(llm_config):
    """Helper to create an agent with specified LLM config."""
    goals = [
        Goal(
            priority=1,
            name="Task",
            description="Answer the user's question with the terminate tool. Call terminate(message='your answer') immediately."
        )
    ]
    
    # Create registry with ONLY the terminate tool
    action_registry = PythonActionRegistry(tool_names=["terminate"])
    action_registry.register_terminate_tool()
    
    return Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=action_registry,
        generate_response=generate_response,
        environment=Environment(),
        llm_config=llm_config
    )


# Example 1: Google Gemini (via LiteLLM)
def example_gemini():
    """Use Google Gemini."""
    print("=== Example 1: Google Gemini ===\n")
    
    # Option A: Use preset
    llm_config = GEMINI_FLASH
    
    # Option B: Custom configuration
    # llm_config = GeminiConfig(
    #     model="gemini/gemini-1.5-pro",
    #     temperature=0.5,
    #     max_tokens=1024
    # )
    
    agent = create_agent_with_llm(llm_config)
    print(f"Using: {llm_config.provider}/{llm_config.model}\n")
    
    memory = agent.run("What is 2+2?")
    print(f"\nCompleted with {len(memory.get_memories())} interactions\n")


# Example 2: OpenAI GPT-4
def example_openai():
    """Use OpenAI GPT-4."""
    print("=== Example 2: OpenAI GPT-4 ===\n")
    
    # Make sure OPENAI_API_KEY is set
    if not os.environ.get('OPENAI_API_KEY'):
        print("Skipping: OPENAI_API_KEY not set\n")
        return
    
    # Option A: Use preset
    llm_config = GPT4O
    
    # Option B: Custom configuration
    # llm_config = OpenAIConfig(
    #     model="openai/gpt-4o-mini",
    #     temperature=0.3,
    #     max_tokens=512
    # )
    
    agent = create_agent_with_llm(llm_config)
    print(f"Using: {llm_config.provider}/{llm_config.model}\n")
    
    memory = agent.run("What is the capital of France?")
    print(f"\nCompleted with {len(memory.get_memories())} interactions\n")


# Example 3: Local Ollama
def example_ollama():
    """Use local Ollama model."""
    print("=== Example 3: Local Ollama ===\n")
    
    # Option A: Use Phi3 (excellent function calling support!)
    llm_config = create_ollama_config(
        model="ollama/phi3:3.8b-mini-128k-instruct-q4_0",
        api_base="http://localhost:11434",
        temperature=0.7
    )
    
    # Option B: Use Gemma3 1B (best function calling support!)
    # llm_config = create_ollama_config(
    #     model="ollama/gemma3:1b",
    #     api_base="http://localhost:11434",
    #     temperature=0.7
    # )
    
    # Option C: Use Gemma2 2B text (supports function calling but less reliable)
    # llm_config = create_ollama_config(
    #     model="ollama/gemma2:2b-text-q8_0",
    #     api_base="http://localhost:11434",
    #     temperature=0.7
    # )
    
    # Note: Qwen3 1.7B does NOT support function calling properly
    # llm_config = create_ollama_config(
    #     model="ollama/qwen3:1.7b",
    #     api_base="http://localhost:11434",
    #     temperature=0.7
    # )
    
    # Option B: Use preset
    # llm_config = LLAMA_LOCAL
    
    # Option C: Custom local model
    # llm_config = create_ollama_config(
    #     model="ollama/mistral",
    #     api_base="http://localhost:11434",
    #     temperature=0.7
    # )
    
    agent = create_agent_with_llm(llm_config)
    print(f"Using: {llm_config.provider}/{llm_config.model}")
    print(f"API Base: {llm_config.api_base}\n")
    
    try:
        memory = agent.run("What is Python?")
        print(f"\nCompleted with {len(memory.get_memories())} interactions\n")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure Ollama is running: ollama serve\n")


# Example 4: Anthropic Claude
def example_anthropic():
    """Use Anthropic Claude."""
    print("=== Example 4: Anthropic Claude ===\n")
    
    # Make sure ANTHROPIC_API_KEY is set
    if not os.environ.get('ANTHROPIC_API_KEY'):
        print("Skipping: ANTHROPIC_API_KEY not set\n")
        return
    
    # Use preset configuration
    llm_config = AnthropicConfig(
        model="anthropic/claude-3-5-sonnet-20241022",
        temperature=0.5
    )
    
    agent = create_agent_with_llm(llm_config)
    print(f"Using: {llm_config.provider}/{llm_config.model}\n")
    
    memory = agent.run("What is machine learning?")
    print(f"\nCompleted with {len(memory.get_memories())} interactions\n")


# Example 5: Compare multiple LLMs
def example_compare_llms():
    """Compare responses from multiple LLMs."""
    print("=== Example 5: Compare Multiple LLMs ===\n")
    
    question = "What is AI?"
    
    configs = [
        ("Gemini Flash", GEMINI_FLASH),
    ]
    
    # Add others if API keys are available
    if os.environ.get('OPENAI_API_KEY'):
        configs.append(("GPT-4o Mini", GPT4O_MINI))
    
    for name, llm_config in configs:
        print(f"\n--- {name} ---")
        agent = create_agent_with_llm(llm_config)
        try:
            memory = agent.run(question)
            # Extract final answer
            for item in reversed(memory.get_memories()):
                if item.get("type") == "environment":
                    import json
                    result = json.loads(item["content"])
                    if result.get("tool_executed"):
                        print(f"Answer: {result['result'][:200]}...")
                    break
        except Exception as e:
            print(f"Error: {e}")


# Example 6: Custom completion function
def example_custom_llm():
    """Use a completely custom LLM implementation."""
    print("=== Example 6: Custom LLM ===\n")
    
    from agent_framework import CustomLLMConfig
    
    def my_custom_llm(prompt):
        """Custom LLM that just echoes back."""
        import json
        return json.dumps({
            "tool": "terminate",
            "args": {
                "message": f"Custom LLM received {len(prompt.messages)} messages"
            }
        })
    
    llm_config = CustomLLMConfig(
        provider="custom",
        model="my-model",
        completion_function=my_custom_llm
    )
    
    agent = create_agent_with_llm(llm_config)
    print(f"Using: Custom LLM\n")
    
    memory = agent.run("Test custom LLM")
    print(f"\nCompleted with {len(memory.get_memories())} interactions\n")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("LLM Provider Examples")
    print("="*60 + "\n")
    
    # Run examples
    # example_gemini()
    # example_openai()
    example_ollama()  # Using Qwen 3 1.7B
    # example_anthropic()
    # example_compare_llms()
    # example_custom_llm()
    
    print("\nUncomment other examples to try different providers!")
