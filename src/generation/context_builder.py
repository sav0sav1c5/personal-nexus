from typing import List, Dict, Any

def build_context_block(retrieved_chunks: List[Dict[str, Any]]) -> str:
    """
    Builds a formatted context block from retrieved chunks.
    This context block is included in the current user message.

    Args:
        retrieved_chunks (List[Dict[str, Any]]): List of chunks with 'content' and 'metadata'

    Returns:
        str: Formatted context string to inject into the user message
    """

    context_parts = []

    for i, chunk in enumerate(retrieved_chunks):
        source = chunk['metadata'].get('name', 'unknown')
        content = chunk['content']
        context_parts.append(f"[Source {i+1}: {source}]\n{content}")

    context_block = "\n\n".join(context_parts)

    return context_block