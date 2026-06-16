# Indexing pipeline 
import os
from typing import Optional

from ingestion.document_loader import load_documents
from ingestion.text_splitter import split_text
from retrieval.embedder import create_embeddings
from retrieval.vector_store import store_vector
from config import paths, chunking

def check_indexing() -> bool:
    """ 
    Checks if indexing is required. 

    Returns: 
    bool: True if indexing is required 
    """

    if not os.path.exists(paths.chroma_db_path):
        return True
    return not os.listdir(paths.chroma_db_path)

def build_index(verbose: bool = False) -> None:
    """ 
    Builds a vector index from documents. 

    Args: 
    verbose (bool): If True, prints the progress 
    """

    if verbose:
        print("=" * 50)
        print("Starting document indexing...")
        print("=" * 50)
    
    # Phase 1 - Document loading
    if verbose:
        print("\n[1/4] Loading documents...")
    documents = load_documents(path=paths.data_path, full=True, verbose=verbose)
    
    # Phase 2 - Text splitting
    if verbose:
        print(f"\n[2/4] Splitting text into chunks (size={chunking.chunk_size}, overlap={chunking.chunk_overlap})...")
    chunks = split_text(documents, chunking.chunk_size, chunking.chunk_overlap, verbose=verbose)
    
    # Phase 3 - Embedding model
    if verbose:
        print("\n[3/4] Creating embeddings...")
    embeddings = create_embeddings(chunks, verbose=verbose)
    
    # Phase 4 - Vector store
    if verbose:
        print("\n[4/4] Storing vectors in ChromaDB...")
    store_vector(embedding_data=embeddings, verbose=verbose)
    
    if verbose:
        print("\n" + "=" * 50)
        print("Indexing completed successfully!")
        print("=" * 50 + "\n")

def get_index_status() -> dict: 
    """ 
    Returns the index status. 

    Returns: 
    dict: Index information 
    """ 

    exists = os.path.exists(paths.chroma_db_path) 
    is_empty = not os.listdir(paths.chroma_db_path) if exists else True 

    return { 
        'exists': exists, 
        'is_empty': is_empty, 
        'needs_indexing': not exists or is_empty,
        'path': paths.chroma_db_path 
    }