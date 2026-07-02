# Handles user input adn commands

from typing import Tuple, Optional

def parse_user_input(user_input: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Parses user input and returns action and query.
    
    Returns:
        Tuple[Optional[str], Optional[str]]:
        - action: 'exit', 'reset', 'eval', 'query' or 'empty'
        - query: str or None
    """

    user_input = user_input.strip()

    # Check for exit
    if user_input.upper() == 'X':
        return 'exit', None

    # Check for reset
    if user_input.lower() == 'reset':
        return 'reset', None
    
    # Check for evaluation
    if user_input.lower() == '/eval':
        return 'eval', None
    
    # Check for empty input
    if not user_input:
        return 'empty', None

    return 'query', user_input

def validate(query: str) -> bool:
    """Check if query is valid."""
    return bool(query and query.strip())


def format_help() -> str:
    """Returns a formatted help message."""

    return """
Personal Nexus Commands:
  - X          : Exit the application
  - reset      : Clear conversation history
  - /eval      : Run RAGAS evaluation on the test dataset
  - <query>    : Regular query

Time measurement is always ON for queries.
"""