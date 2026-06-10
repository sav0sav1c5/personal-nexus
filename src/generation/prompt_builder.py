from typing import List, Dict, Any

def build_prompt(query: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
    """
    Builds a prompt for the LLM with context and question.

    Args:
        query (str): User's question
        retrieved_chunks (List[Dict[str, Any]]): List of chunks with 'content' and 'metadata'

    Returns:
        str: Formatted prompt for the LLM
    """

    context_parts = []

    for i, chunk in enumerate(retrieved_chunks):
        source = chunk['metadata'].get('name', 'unknown')
        content = chunk['content']
        context_parts.append(f"[Source {i+1}: {source}]\n{content}")

    context_block = "\n\n".join(context_parts)

    prompt = f"""You are a helpful assistant. Answer the user's question based ONLY on the provided context.
If the answer is not found in the context, say that you don't have enough information.
Always cite which source(s) you used at the end of your answer.

Context:
{context_block}

Question: {query}

Answer:"""

    return prompt