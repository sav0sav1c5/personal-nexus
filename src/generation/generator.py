# Generates an answer using Groq LLM based on retrieved context

import os
from groq import Groq
from dotenv import load_dotenv
from typing import List, Dict, Any, Generator
from generation.prompt_builder import build_prompt

load_dotenv()

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
