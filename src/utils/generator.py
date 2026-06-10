# Generates an answer using Groq LLM based on retrieved context

# Suppress loading messages from sentence-transformers
import os
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

import logging
logging.getLogger('sentence_transformers').setLevel(logging.WARNING)
logging.getLogger('transformers').setLevel(logging.WARNING)
logging.getLogger('huggingface_hub').setLevel(logging.WARNING)

from groq import Groq
from dotenv import load_dotenv
from typing import List, Dict, Any, Generator

load_dotenv()

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


def generate(query: str, retrieved_chunks: List[Dict[str, Any]], verbose: bool = False) -> Generator[str, None, None]:
    """
    Generates an answer using Groq LLM based on retrieved context.

    Args:
        query (str): User's question
        retrieved_chunks (List[Dict[str, Any]]): List of chunks from retriever
        verbose (bool): If True, prints progress messages

    Returns:
        str: Generated answer from the LLM
    """

    if verbose:
        print("\n\nPhase 6: Answer generation starting...")

    if not retrieved_chunks:
        if verbose:
            print('- No chunks provided, cannot generate answer!')
        return "No relevant information found."

    # Build the full prompt
    prompt = build_prompt(query, retrieved_chunks)
    if verbose:
        print(f'- Prompt built with {len(retrieved_chunks)} context chunks')

    # Initialize Groq client
    client = Groq(api_key=os.getenv('GROQ_API_KEY'))

    # Send request to LLM
    if verbose:
        print('- Sending request to Groq (llama-3.3-70b-versatile)...')
    
    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ],
        # Low temperature = more focused, less creative answers
        temperature=0.2,
        max_tokens=512,
        stream=True
    )

    # Extract the text answer from the response object
    # answer = response.choices[0].message.content

    # Yield each chunk as it arrives from the API
    for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

    if verbose:
        print("Phase 6: Answer generation finished!")
