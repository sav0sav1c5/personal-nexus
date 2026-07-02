# Merges everything together into one RAG flow

import time
from typing import Optional, List, Dict

from retrieval.search import get_relevant_chunks
from generation.generator import generate
from utils.indexing import check_indexing, build_index

def pipeline(query: Optional[str] = None,
             measure_time: bool = False, 
             conversation_history: Optional[List[Dict[str, str]]] = None
            ):
    """
    Main RAG pipeline that processes documents and answers queries.

    Args:
        query (Optional[str]): User's question. If None, only indexing is performed.
        measure_time (bool): If True, measures and prints execution time
        conversation_history (Optional[List[Dict[str, str]]]): History of conversation

    Returns:
        str: Answer if query provided, otherwise None
    """

    if conversation_history is None:
        conversation_history = []
    
    # Build index if needed
    if check_indexing():
        build_index()

    start_time = time.time() if measure_time else None
    
    if measure_time:
        print(f'Starting pipeline at: {time.strftime("%H:%M:%S")}')

    # Phase 5 & 6 - Query pipeline (only if a question is provided)
    if query:
        # Measure retrieval + generation separately
        query_start = time.time() if measure_time else None

        # Two-stage retrieve + rerank (or plain retrieval), shared with evaluation
        retrieved_chunks = get_relevant_chunks(query)

        # First retrieval time (before streaming)
        if measure_time:
            retrieval_time = time.time() - query_start
            print(f'Retrieval time: {retrieval_time:.2f} seconds')
            print('Starting generation (streaming)...')
        
        print("\n\n========== ANSWER ==========")
        
        # Streaming of response
        full_response = ""
        for chunk in generate(query=query, 
                              retrieved_chunks=retrieved_chunks,
                              conversation_history=conversation_history
                              ):
            print(chunk, end='', flush=True)
            full_response += chunk

        print("\n============================")

        if measure_time:
            total_elapsed = time.time() - start_time
            print(f'Total pipeline time: {total_elapsed:.2f} seconds')

        return full_response
    
    return None