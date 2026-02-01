"""Language interfaces for agent communication and prompt formatting."""

import json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from litellm import completion

from .core import Action, Environment, Goal, Memory
from .config import LLMConfig, GeminiConfig


@dataclass
class Prompt:
    """Represents a structured prompt with messages, tools, and metadata."""
    messages: List[Dict] = field(default_factory=list)
    tools: List[Dict] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


class AgentLanguage:
    """Base class for agent language/communication interfaces."""
    
    def __init__(self):
        pass

    def construct_prompt(
        self,
        actions: List[Action],
        environment: Environment,
        goals: List[Goal],
        memory: Memory
    ) -> Prompt:
        """Construct a prompt from agent components."""
        raise NotImplementedError("Subclasses must implement this method")

    def parse_response(self, response: str) -> dict:
        """Parse LLM response into structured format."""
        raise NotImplementedError("Subclasses must implement this method")


class AgentFunctionCallingActionLanguage(AgentLanguage):
    """Language interface using function calling format."""

    def __init__(self):
        super().__init__()

    def format_goals(self, goals: List[Goal]) -> List:
        """Format goals into system messages."""
        sep = "\n-------------------\n"
        goal_instructions = "\n\n".join([
            f"{goal.name}:{sep}{goal.description}{sep}"
            for goal in goals
        ])
        
        # Add explicit instructions for tool usage
        tool_usage_instruction = (
            "\n\n⚠️ IMPORTANT: You MUST respond by calling one of the available tools. "
            "Do NOT provide direct text responses. "
            "Always use the tool calling format to execute actions.\n"
        )
        
        return [{"role": "system", "content": goal_instructions + tool_usage_instruction}]

    def format_memory(self, memory: Memory) -> List:
        """Format memory items into message format."""
        items = memory.get_memories()
        mapped_items = []
        
        for item in items:
            content = item.get("content", None)
            if not content:
                content = json.dumps(item, indent=4)

            if item["type"] == "assistant":
                mapped_items.append({"role": "assistant", "content": content})
            elif item["type"] == "environment":
                mapped_items.append({"role": "assistant", "content": content})
            else:
                mapped_items.append({"role": "user", "content": content})

        return mapped_items

    def format_actions(self, actions: List[Action]) -> List:
        """Format actions into tool definitions."""
        tools = [
            {
                "type": "function",
                "function": {
                    "name": action.name,
                    "description": action.description[:1024],
                    "parameters": action.parameters,
                },
            } for action in actions
        ]
        return tools

    def construct_prompt(
        self,
        actions: List[Action],
        environment: Environment,
        goals: List[Goal],
        memory: Memory
    ) -> Prompt:
        """Construct a complete prompt with all components."""
        prompt = []
        prompt += self.format_goals(goals)
        prompt += self.format_memory(memory)
        tools = self.format_actions(actions)
        return Prompt(messages=prompt, tools=tools)

    def parse_response(self, response: str) -> dict:
        """Parse LLM response, handling both JSON and text responses."""
        try:
            return json.loads(response)
        except Exception as e:
            return {
                "tool": "terminate",
                "args": {"message": response}
            }


def generate_response(
    prompt: Prompt,
    llm_config: Optional[LLMConfig] = None
) -> str:
    """Generate response from LLM using the provided prompt.
    
    Args:
        prompt: The Prompt object containing messages and tools
        llm_config: LLM configuration (defaults to Gemini Flash if None)
        
    Returns:
        The response as a JSON string or text content
    """
    # Use default Gemini config if none provided
    if llm_config is None:
        llm_config = GeminiConfig()
    
    messages = prompt.messages
    tools = prompt.tools
    result = None
    
    # Get completion parameters from config
    completion_params = llm_config.to_completion_params()
    completion_params["messages"] = messages
    
    # Handle custom completion function
    if hasattr(llm_config, 'completion_function') and llm_config.completion_function:
        try:
            response = llm_config.completion_function(prompt)
            return response
        except Exception as e:
            print(f"Warning: Custom completion function failed: {e}")
            result = json.dumps({
                "tool": "terminate",
                "args": {"message": f"Error with custom LLM: {e}"}
            })
            return result

    if not tools:
        response = completion(**completion_params)
        if response.choices and len(response.choices) > 0:
            result = response.choices[0].message.content
        else:
            print(f"Warning: Empty response from LLM. Response: {response}")
            result = "Error: Empty response from LLM"
    else:
        completion_params["tools"] = tools
        response = completion(**completion_params)

        if response.choices and len(response.choices) > 0:
            if response.choices[0].message.tool_calls:
                tool = response.choices[0].message.tool_calls[0]
                result = {
                    "tool": tool.function.name,
                    "args": json.loads(tool.function.arguments),
                }
                result = json.dumps(result)
            else:
                result = response.choices[0].message.content
        else:
            print(f"Warning: Empty response from LLM. Response: {response}")
            result = json.dumps({
                "tool": "terminate",
                "args": {"message": "Error: Empty response from LLM"}
            })

    return result
