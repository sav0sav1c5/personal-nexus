# Merges everything together into one RAG flow

import os
import time
from typing import Optional, List, Dict

from retrieval.retriever import retrieve
from retrieval.reranker import rerank
from generation.generator import generate
from config import retrieval, reranking
from utils.indexing import check_indexing, build_index

def pipeline(query: Optional[str] = None,
             verbose: bool = False, 
             measure_time: bool = False, 
             conversation_history: Optional[List[Dict[str, str]]] = None
            ):
    """
    Main RAG pipeline that processes documents and answers queries.

    Args:
        query (Optional[str]): User's question. If None, only indexing is performed.
        verbose (bool): If True, prints progress messages for all phases
        measure_time (bool): If True, measures and prints execution time
        conversation_history (Optional[List[Dict[str, str]]]): History of conversation

    Returns:
        str: Answer if query provided, otherwise None
    """

    if conversation_history is None:
        conversation_history = []
    
    # Build index if needed
    if check_indexing():
        build_index(verbose=verbose)

    start_time = time.time() if measure_time else None
    
    if measure_time:
        print(f'Starting pipeline at: {time.strftime("%H:%M:%S")}')

    # Phase 5 & 6 - Query pipeline (only if a question is provided)
    if query:
        # Measure retrieval + generation separately
        query_start = time.time() if measure_time else None

        if reranking.enabled: 
            # Phase 1: pull a WIDER set of candidates (eg 20) with a cheap bi-encoder search 
            candidate_chunks = retrieve( 
                query=query, 
                n_results=reranking.n_candidates, 
                verbose=verbose 
            ) 

            # Phase 2: precisely sort the candidates with the cross-encoder, keep only the best 
            retrieved_chunks = rerank( 
                query=query, 
                chunks=candidate_chunks, 
                top_n=reranking.n_final, 
                verbose=verbose 
            ) 
        else: 
                # Fallback to old behavior if reranking is turned off in config 
                retrieved_chunks = retrieve( 
                query=query,
                n_results=retrieval.n_results,
                verbose=verbose
            )

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
                              conversation_history=conversation_history, 
                              verbose=verbose
                              ):
            print(chunk, end='', flush=True)
            full_response += chunk

        print("\n============================")

        if measure_time:
            total_elapsed = time.time() - start_time
            print(f'Total pipeline time: {total_elapsed:.2f} seconds')

        return full_response
    
    return None