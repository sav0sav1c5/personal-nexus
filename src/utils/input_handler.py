# Handles user input adn commands

from typing import Tuple, Optional

def parse_user_input(user_input: str) -> Tuple[Optional[str], bool, Optional[str]]:
    """ 
    Parses user input and returns action, verbose flag and query. 

    Args: 
    user_input (str): User input 

    Returns: 
    Tuple[Optional[str], bool, Optional[str]]: 
    - action: 'exit', 'reset', 'eval', 'query' or 'empty' 
    - verbose: bool 
    - query: str or None 
    """

    user_input = user_input.strip()

    # Check for exit
    if user_input.upper() == 'X':
        return 'exit', False, None

    # Check for reset
    if user_input.lower() == 'reset':
        return 'reset', False, None
    
    # Check for evaluation
    if user_input.lower() == '/eval':
        return 'eval', False, None

    # Check for verbose evaluation
    if user_input.lower() == 'v: /eval':
        return 'eval', True, None
    
    # Check for empty import
    if not user_input:
        return 'empty', False, None
    
    # Check for verbose mode
    if user_input.lower().startswith('v: '):
        verbose = True
        query = user_input[3:].strip()
    else:
        verbose = False
        query = user_input
    
    # Check for empty query after verbose prefix
    if not query:
        return 'empty', False, None

    return 'query', verbose, query

def validate(query: str) -> bool:
    """Check if query is valid."""
    return bool(query and query.strip())


def format_help() -> str:
    """Returns a formatted help message."""

    return """
Personal Nexus Commands:
  - X          : Exit the application
  - reset      : Clear conversation history
  - v: <query> : Run in verbose mode (e.g., "v: What is Python?")
  - <query>    : Regular query

Time measurement is always ON for queries.
"""