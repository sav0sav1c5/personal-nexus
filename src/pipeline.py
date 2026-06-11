# Merges everything together into one RAG flow

import os
import time
from typing import Optional
from ingestion.document_loader import load_documents
from ingestion.text_splitter import split_text
from retrieval.embedder import create_embeddings
from retrieval.vector_store import store_vector
from retrieval.retriever import retrieve
from generation.generator import generate
from config import paths, chunking, retrieval

def pipeline(query: Optional[str] = None, verbose: bool = False, measure_time: bool = False):
    """
    Main RAG pipeline that processes documents and answers queries.

    Args:
        query (Optional[str]): User's question. If None, only indexing is performed.
        verbose (bool): If True, prints progress messages for all phases

    Returns:
        str: Answer if query provided, otherwise None
    """

    db_exists = os.path.exists(paths.chroma_db_path) and os.listdir(paths.chroma_db_path)
    
    if not db_exists:
        # Phase 1 - Document loading
        documents = load_documents(path=paths.data_path, full=True, verbose=verbose)
        
        # Phase 2 - Text splitting
        chunks = split_text(documents, chunking.chunk_size, chunking.chunk_overlap, verbose=verbose)

        # Phase 3 - Embedding model
        embeddings = create_embeddings(chunks, verbose=verbose)

        # Phase 4 - Vector store
        store_vector(embedding_data=embeddings, verbose=verbose)

    
    start_time = time.time() if measure_time else None
    
    if measure_time:
        print(f'Starting pipeline at: {time.strftime("%H:%M:%S")}')

    # Phase 5 & 6 - Query pipeline (only if a question is provided)
    if query:
        # Measure retrieval + generation separately
        query_start = time.time() if measure_time else None

        retrieved_chunks = retrieve(query=query, n_results=retrieval.n_results, verbose=verbose)
        
        # First retrieval time (before streaming)
        if measure_time:
            retrieval_time = time.time() - query_start
            print(f'Retrieval time: {retrieval_time:.2f} seconds')
            print('Starting generation (streaming)...')
        
        print("\n\n========== ANSWER ==========")
        
        # Streaming of response
        for chunk in generate(query=query, retrieved_chunks=retrieved_chunks, verbose=verbose):
            print(chunk, end='', flush=True)
        
        print("\n============================")

        if measure_time:
            total_elapsed = time.time() - start_time
            print(f'Total pipeline time: {total_elapsed:.2f} seconds')

        return None
    
    return None