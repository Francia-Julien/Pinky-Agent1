"""Tool definitions for agents"""

from langchain_core.tools import tool
import httpx
import json
from typing import Optional


@tool
def search_web(query: str, num_results: int = 5) -> str:
    """
    Search the web for information
    
    Args:
        query: Search query
        num_results: Number of results to return
        
    Returns:
        Search results
    """
    # Placeholder implementation - replace with actual web search
    return f"Search results for '{query}' (simulated)"


@tool
def fetch_url(url: str) -> str:
    """
    Fetch content from a URL
    
    Args:
        url: URL to fetch
        
    Returns:
        Page content
    """
    try:
        response = httpx.get(url, timeout=10.0)
        return response.text[:2000]  # Return first 2000 chars
    except Exception as e:
        return f"Error fetching URL: {str(e)}"


@tool
def parse_json(data: str) -> str:
    """
    Parse and validate JSON data
    
    Args:
        data: JSON string to parse
        
    Returns:
        Parsed JSON or error message
    """
    try:
        parsed = json.loads(data)
        return json.dumps(parsed, indent=2)
    except json.JSONDecodeError as e:
        return f"JSON parsing error: {str(e)}"


@tool
def calculate_expression(expression: str) -> str:
    """
    Safely evaluate mathematical expressions
    
    Args:
        expression: Mathematical expression (safe subset)
        
    Returns:
        Calculation result
    """
    try:
        # Only allow safe operations
        safe_dict = {"__builtins__": {}}
        result = eval(expression, safe_dict)
        return str(result)
    except Exception as e:
        return f"Calculation error: {str(e)}"


def get_default_tools():
    """Get all default tools for agents"""
    return [search_web, fetch_url, parse_json, calculate_expression]
