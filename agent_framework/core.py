"""Core data structures and classes for the agent framework."""

import time
import traceback
from dataclasses import dataclass
from typing import List, Dict, Any, Callable


@dataclass(frozen=True)
class Goal:
    """Represents an agent's goal with priority and description."""
    priority: int
    name: str
    description: str


class Action:
    """Represents an executable action with metadata."""
    
    def __init__(
        self,
        name: str,
        function: Callable,
        description: str,
        parameters: Dict,
        terminal: bool = False
    ):
        self.name = name
        self.function = function
        self.description = description
        self.terminal = terminal
        self.parameters = parameters

    def execute(self, **args) -> Any:
        """Execute the action's function with provided arguments."""
        return self.function(**args)


class ActionRegistry:
    """Registry for managing available actions."""
    
    def __init__(self):
        self.actions = {}

    def register(self, action: Action):
        """Register an action in the registry."""
        self.actions[action.name] = action

    def get_action(self, name: str) -> Action:
        """Retrieve an action by name."""
        return self.actions.get(name, None)

    def get_actions(self) -> List[Action]:
        """Get all registered actions."""
        return list(self.actions.values())


class Memory:
    """Manages conversation history and working memory."""
    
    def __init__(self):
        self.items = []

    def add_memory(self, memory: dict):
        """Add a memory item to working memory."""
        self.items.append(memory)

    def get_memories(self, limit: int = None) -> List[Dict]:
        """Get conversation history, optionally limited."""
        return self.items[:limit] if limit else self.items

    def copy_without_system_memories(self):
        """Return a copy of memory without system messages."""
        filtered_items = [m for m in self.items if m.get("type") != "system"]
        memory = Memory()
        memory.items = filtered_items
        return memory


class Environment:
    """Manages action execution and result formatting."""
    
    def execute_action(self, action: Action, args: dict) -> dict:
        """Execute an action and return the formatted result."""
        try:
            result = action.execute(**args)
            return self.format_result(result)
        except Exception as e:
            return {
                "tool_executed": False,
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    def format_result(self, result: Any) -> dict:
        """Format the result with metadata."""
        return {
            "tool_executed": True,
            "result": result,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z")
        }
