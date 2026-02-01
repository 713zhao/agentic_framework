"""Main execution script demonstrating the agent framework."""

import os

from agent_framework import (
    Goal,
    Agent,
    AgentFunctionCallingActionLanguage,
    PythonActionRegistry,
    Environment,
    generate_response,
    # LLM Configurations
    GEMINI_FLASH,
    GeminiConfig,
    # Uncomment to try other providers:
    # GPT4O,
    # CLAUDE_SONNET,
    # LLAMA_LOCAL,
)

# Tools are automatically loaded when agent_framework is imported!
# No need to manually import tool modules anymore.


def main():
    """Run the agent with a README generation task."""
    
    # Configure your LLM (pick one):
    
    # Option 1: Use preset configurations
    llm_config = GEMINI_FLASH
    
    # Option 2: Create custom Gemini config
    # llm_config = GeminiConfig(
    #     model="gemini/gemini-1.5-pro",
    #     temperature=0.7,
    #     max_tokens=2048
    # )
    
    # Option 3: Use OpenAI
    # llm_config = GPT4O
    
    # Option 4: Use local Ollama
    # llm_config = LLAMA_LOCAL
    
    # Option 5: Create custom config
    # from agent_framework import create_ollama_config
    # llm_config = create_ollama_config(
    #     model="ollama/mistral",
    #     api_base="http://localhost:11434"
    # )
    
    print(f"Using LLM: {llm_config.provider}/{llm_config.model}\n")
    
    # Define the agent's goals
    goals = [
        Goal(
            priority=1,
            name="Gather Information",
            description="Read each file in the project in order to build a deep understanding of the project in order to write a README"
        ),
        Goal(
            priority=1,
            name="Terminate",
            description="Call terminate when done and provide a complete README for the project in the message parameter"
        )
    ]

    # Create an agent instance with tag-filtered actions
    agent = Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=PythonActionRegistry(tags=["file_operations", "system"]),
        generate_response=generate_response,
        environment=Environment(),
        llm_config=llm_config  # Pass LLM config here
    )

    # Run the agent with user input
    user_input = "Write a Instructions for this project."
    print(f"Starting agent with task: {user_input}\n")
    
    final_memory = agent.run(user_input)
    
    print("\n" + "="*50)
    print("Agent execution completed!")
    print("="*50 + "\n")
    
    # Print final memory summary
    memories = final_memory.get_memories()
    print(f"Total memory items: {len(memories)}\n")
    
    # Print the final result
    if memories:
        last_memory = memories[-1]
        if last_memory.get("type") == "environment":
            import json
            result = json.loads(last_memory["content"])
            if result.get("tool_executed"):
                print("Final Output:")
                print(result["result"])


if __name__ == "__main__":
    main()
