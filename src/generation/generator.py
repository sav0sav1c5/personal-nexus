# Generates an answer using Groq LLM based on retrieved context

import os
from groq import Groq
from dotenv import load_dotenv
from typing import List, Dict, Any, Generator
from generation.context_builder import build_context_block
from config import llm, system

MAX_HISTORY_PAIRS = 5

SYSTEM_PROMPT = """Ti si asistent za pitanja i odgovore koji KORISTI SAMO DOSTAVLJENI KONTEKST.

STROGA PRAVILA:
1. ODGOVARAJ SAMO NA OSNOVU KONTEKSTA ISPOD
2. AKO KONTEKST NE SADRŽI ODGOVOR, ODGOVORI: "Nemam dovoljno informacija u dostupnom kontekstu."
3. NIKADA NE KORISTI SOPSTVENO ZNANJE - čak i ako znaš odgovor
4. CITIRAJ ILI PARAFRAZIRAJ DIREKTNO IZ KONTEKSTA
5. UVIEK NAVEDI IZVORE: [Izvor: ime_fajla.txt]

Kontekst je dat ispod. Koristi istoriju konverzacije za razumevanje referenci."""

def get_windowed_history(
    history: List[Dict[str, str]],
    max_pairs: int = MAX_HISTORY_PAIRS
) -> List[Dict[str, str]]:
    """
    Returns only the last max_pairs exchanges from conversation history.
    Prevents context window overflow for long conversations.

    Args:
        history: Full conversation history as list of message dicts
        max_pairs: Maximum number of user/assistant pairs to keep

    Returns:
        List[Dict]: Trimmed history with at most max_pairs*2 messages
    """
   
    max_messages = max_pairs * 2

    if len(history) <= max_messages:
        return history
    
    return history[-max_messages:]

def generate(
        query: str,
        retrieved_chunks: List[Dict[str, Any]],
        conversation_history: List[Dict[str, str]]
) -> Generator[str, None, None]:
    """
    Generates a streaming answer using Groq LLM.
    Uses conversation history for multi-turn context awareness.

    Args:
        query (str): Current user question
        retrieved_chunks (List[Dict[str, Any]]): Retrieved chunks from ChromaDB
        conversation_history (List[Dict[str, str]]): Full chat history so far
        verbose (bool): If True, prints progress messages

    Yields:
        str: Text chunks as they stream from the API
    """

    if system.verbose_generation:
        print("\n\nPhase 6: Answer generation starting...")

    if not retrieved_chunks:
            if system.verbose_generation:
                print('- No chunks provided, cannot generate answer!')
            yield "No relevant information found."
            return
    
    # Build context block from retrieved chunks
    context_block = build_context_block(retrieved_chunks)
    if system.verbose_generation:
        print(f'- Context built from {len(retrieved_chunks)} chunks')

    # Get windowd history
    windowed_history = get_windowed_history(conversation_history)
    if system.verbose_generation:
        print(f'- History window: {len(windowed_history) // 2} exchanges')

    # We are building a message list: 
    # [system] + [previous messages from history] + [current query with context] 
    messages = [ 
        {"role": "system", "content": SYSTEM_PROMPT} 
    ] 

    # Add all messages from the history window 
    messages.extend(windowed_history) 

    # Current query — we add the context block HERE, along with the current question. 
    # We don't add it to the history because it's only relevant to this query. 
    current_message = f"""Context from knowledge base: {context_block}

    Question: {query}""" 

    messages.append({"role": "user", "content": current_message}) 

    if system.verbose_generation:
        print(f'- Total messages sent to LLM: {len(messages)}')

    # Initialize Groq client
    client = Groq(api_key=llm.api_key)

    # Send request to LLM
    if system.verbose_generation:
        print('- Sending request to Groq (llama-3.3-70b-versatile)...')
    
    response = client.chat.completions.create(
        model=llm.model,
        messages=messages,
        temperature=llm.temperature,
        max_tokens=llm.max_tokens,
        stream=True
    )

    # Extract the text answer from the response object
    # answer = response.choices[0].message.content

    # Yield each chunk as it arrives from the API
    for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

    if system.verbose_generation:
        print("Phase 6: Answer generation finished!")
