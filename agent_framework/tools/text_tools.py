"""String and text manipulation tools."""

from typing import List, Dict, Any

from ..tool_registry import register_tool


@register_tool(tags=["text", "string"])
def count_words(text: str) -> int:
    """Count the number of words in a text string.
    
    Args:
        text: The text to count words in
        
    Returns:
        The number of words
    """
    return len(text.split())


@register_tool(tags=["text", "string"])
def reverse_string(text: str) -> str:
    """Reverse a string.
    
    Args:
        text: The text to reverse
        
    Returns:
        The reversed text
    """
    return text[::-1]


@register_tool(tags=["text", "string"])
def to_uppercase(text: str) -> str:
    """Convert text to uppercase.
    
    Args:
        text: The text to convert
        
    Returns:
        The text in uppercase
    """
    return text.upper()


@register_tool(tags=["text", "string"])
def to_lowercase(text: str) -> str:
    """Convert text to lowercase.
    
    Args:
        text: The text to convert
        
    Returns:
        The text in lowercase
    """
    return text.lower()


@register_tool(tags=["text", "analysis"])
def find_substring(text: str, substring: str) -> Dict[str, Any]:
    """Find all occurrences of a substring in text.
    
    Args:
        text: The text to search in
        substring: The substring to find
        
    Returns:
        Dictionary with count and positions
    """
    positions = []
    start = 0
    while True:
        pos = text.find(substring, start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + 1
    
    return {
        "count": len(positions),
        "positions": positions,
        "found": len(positions) > 0
    }
