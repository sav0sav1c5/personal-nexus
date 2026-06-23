# Retrieves relevant chunks from ChromaDB based on user query

import chromadb
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List, Dict, Any
from config import paths, embedding
from retrieval.model_cache import ModelCache
from config import system

def load_embedding_model():
    """
    Loads the HuggingFace embedding model.

    Returns:
        HuggingFaceEmbeddings: The embedding model instance
    """

    model = HuggingFaceEmbeddings(
        model_name=embedding.model_name,
        model_kwargs={'device': embedding.device},
        encode_kwargs={'normalize_embeddings': embedding.normalize_embeddings}
    )

    return model

def embed_query(query: str, embedding_model) -> List[float]:
    """
    Converts a query string into a vector embedding.

    Args:
        query (str): The user's question
        embedding_model: The embedding model instance

    Returns:
        List[float]: The query vector
    """

    return embedding_model.embed_query(query)

def retrieve(query: str, n_results: int = 3) -> List[Dict[str, Any]]:
    """
    Retrieves the most similar chunks from ChromaDB for a given query.

    Args:
        query (str): User's question
        n_results (int): Number of chunks to retrieve
        verbose (bool): If True, prints progress messages

    Returns:
        List[Dict[str, Any]]: List of retrieved chunks with content, metadata, distance, and similarity
    """

    if system.verbose_retrieval:
        print("\n\nPhase 5: Retrieval starting...")

    # Load the same embedding model used in Phase 3
    embedding_model = ModelCache.get_model()

    # Convert the query text into a vector
    query_vector = embed_query(query, embedding_model)
    if system.verbose_retrieval:
        print(f'- Query embedded into vector of dimension: {len(query_vector)}')

    # Connect to the existing ChromaDB on disk
    db_client = chromadb.PersistentClient(path=paths.chroma_db_path)
    collection = db_client.get_collection('nexus_docs')

    # Search for the n most similar chunks using cosine similarity
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=n_results,
        include=['documents', 'metadatas', 'distances']
    )

    # ChromaDB returns lists-of-lists (one list per query), we only have one query
    raw_documents = results['documents'][0]
    raw_metadatas = results['metadatas'][0]
    raw_distances = results['distances'][0]

    # Package results into a clean list of dicts
    retrieved_chunks = []

    for doc, metadata, distance in zip(raw_documents, raw_metadatas, raw_distances):
        retrieved_chunks.append({
            'content': doc,
            'metadata': metadata,
            'distance': distance,
            # Similarity score: closer distance = more similar (distance is between 0 and 2 for normalized vectors)
            'similarity': round(1 - distance, 4)
        })
    
    if system.verbose_retrieval:
        print(f'- Retrieved {len(retrieved_chunks)} chunks:')

        for i, chunk in enumerate(retrieved_chunks):
            source = chunk['metadata'].get('name', 'unknown')
            similarity = chunk['similarity']
            preview = chunk['content'][:80].replace('\n', ' ')
            print(f'  [{i+1}] Source: {source} | Similarity: {similarity} | "{preview}..."')

        print("Phase 5: Retrieval finished!")

    return retrieved_chunks