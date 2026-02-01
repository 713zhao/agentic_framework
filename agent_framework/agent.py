"""Main Agent class and specialized registries."""

import json
from typing import List, Callable, Optional

from .core import Goal, Action, ActionRegistry, Memory, Environment
from .agent_language import AgentLanguage, Prompt
from .config import LLMConfig
from .tool_registry import tools


class PythonActionRegistry(ActionRegistry):
    """Action registry that loads tools from the global tool registry with filtering."""
    
    def __init__(self, tags: List[str] = None, tool_names: List[str] = None):
        """Initialize registry with optional tag or name filtering.
        
        Args:
            tags: Only load tools with these tags
            tool_names: Only load tools with these names
        """
        super().__init__()
        self.terminate_tool = None

        for tool_name, tool_desc in tools.items():
            if tool_name == "terminate":
                self.terminate_tool = tool_desc

            if tool_names and tool_name not in tool_names:
                continue

            tool_tags = tool_desc.get("tags", [])
            if tags and not any(tag in tool_tags for tag in tags):
                continue

            self.register(Action(
                name=tool_name,
                function=tool_desc["function"],
                description=tool_desc["description"],
                parameters=tool_desc.get("parameters", {}),
                terminal=tool_desc.get("terminal", False)
            ))

    def register_terminate_tool(self):
        """Explicitly register the terminate tool if it exists."""
        if self.terminate_tool:
            self.register(Action(
                name="terminate",
                function=self.terminate_tool["function"],
                description=self.terminate_tool["description"],
                parameters=self.terminate_tool.get("parameters", {}),
                terminal=self.terminate_tool.get("terminal", False)
            ))
        else:
            raise Exception("Terminate tool not found in tool registry")


class Agent:
    """Main agent class implementing the GAME loop (Goals, Actions, Memory, Environment)."""
    
    def __init__(
        self,
        goals: List[Goal],
        agent_language: AgentLanguage,
        action_registry: ActionRegistry,
        generate_response: Callable[[Prompt], str],
        environment: Environment,
        llm_config: Optional[LLMConfig] = None
    ):
        """Initialize agent with core GAME components.
        
        Args:
            goals: List of goals the agent should pursue
            agent_language: Language interface for communication
            action_registry: Registry of available actions
            generate_response: Function to generate LLM responses
            environment: Environment for action execution
            llm_config: Optional LLM configuration (uses default if None)
        """
        self.goals = goals
        self.generate_response = generate_response
        self.agent_language = agent_language
        self.actions = action_registry
        self.environment = environment
        self.llm_config = llm_config

    def construct_prompt(
        self,
        goals: List[Goal],
        memory: Memory,
        actions: ActionRegistry
    ) -> Prompt:
        """Build prompt with memory context."""
        return self.agent_language.construct_prompt(
            actions=actions.get_actions(),
            environment=self.environment,
            goals=goals,
            memory=memory
        )

    def get_action(self, response: str):
        """Parse response and retrieve the corresponding action."""
        invocation = self.agent_language.parse_response(response)
        action = self.actions.get_action(invocation["tool"])
        return action, invocation

    def should_terminate(self, response: str) -> bool:
        """Check if the agent should terminate based on response."""
        action_def, _ = self.get_action(response)
        return action_def.terminal if action_def else False

    def set_current_task(self, memory: Memory, task: str):
        """Set the current task in memory."""
        memory.add_memory({"type": "user", "content": task})

    def update_memory(self, memory: Memory, response: str, result: dict):
        """Update memory with agent's decision and environment's response."""
        new_memories = [
            {"type": "assistant", "content": response},
            {"type": "environment", "content": json.dumps(result)}
        ]
        for m in new_memories:
            memory.add_memory(m)

    def prompt_llm_for_action(self, full_prompt: Prompt) -> str:
        """Generate LLM response for the given prompt."""
        # Pass LLM config if generate_response accepts it
        if self.llm_config is not None:
            try:
                # Try calling with llm_config parameter
                response = self.generate_response(full_prompt, self.llm_config)
            except TypeError:
                # Fallback if function doesn't accept llm_config
                response = self.generate_response(full_prompt)
        else:
            response = self.generate_response(full_prompt)
        return response

    def run(
        self,
        user_input: str,
        memory: Memory = None,
        max_iterations: int = 50
    ) -> Memory:
        """Execute the GAME loop for this agent.
        
        Args:
            user_input: The user's task or query
            memory: Optional existing memory (creates new if None)
            max_iterations: Maximum number of iterations before stopping
            
        Returns:
            The final memory state after execution
        """
        memory = memory or Memory()
        self.set_current_task(memory, user_input)

        for iteration in range(max_iterations):
            # Construct prompt with current state
            prompt = self.construct_prompt(self.goals, memory, self.actions)

            print("Agent thinking...")
            # Generate response from agent
            response = self.prompt_llm_for_action(prompt)
            print(f"Agent Decision: {response}")

            # Determine which action to execute
            action, invocation = self.get_action(response)
            
            if action is None:
                print(f"\n⚠️  LLM Response Error:")
                print(f"   The LLM returned text instead of calling a tool.")
                print(f"   This usually means:")
                print(f"   - The model doesn't fully support function calling")
                print(f"   - The model decided to answer directly")
                print(f"   - Try using a different model or adjusting temperature")
                print(f"\n   Raw response: {response[:200]}...")
                print(f"\n   Treating as 'terminate' with the response as message.\n")
                
                # Try to recover by treating response as terminate message
                terminate_action = self.actions.get_action("terminate")
                if terminate_action:
                    action = terminate_action
                    invocation = {
                        "tool": "terminate",
                        "args": {"message": response[:500]}  # Truncate if too long
                    }
                else:
                    print("   Could not find 'terminate' tool. Stopping agent.")
                    break

            # Execute action in environment
            result = self.environment.execute_action(action, invocation["args"])
            print(f"Action Result: {result}")

            # Update memory with what happened
            self.update_memory(memory, response, result)

            # Check for termination
            if self.should_terminate(response):
                break

        return memory
