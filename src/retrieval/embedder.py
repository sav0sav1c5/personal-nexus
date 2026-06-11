# Makes embeddings

import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from typing import List, Dict, Any
from langchain_huggingface import HuggingFaceEmbeddings

# Load API key from .env file
load_dotenv()

# Defining model name as constant so it's easy to change and hard to mismatch
EMBEDDING_MODEL = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'

def create_embeddings(chunks: List[Document], verbose: bool = False) -> List[Dict[str, Any]]:
    """
    Converts a list of text chunks into vector embeddings.

    Args:
        chunks (List[Document]): List of Document objects with page_content
        verbose (bool): If True, prints progress messages and preview

    Returns:
        List[Dict[str, Any]]: List of dicts containing 'chunk', 'embedding', and 'metadata'
    """

    if verbose:
        print("\n\nPhase 3: Document embedding starting...")

    if not chunks:
        if verbose:
            print('No chunks for embedding!')
        return []
    
    # Initialize embedding model
    embedding_model = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

    # Extract text from chunks
    chunks_content = [c.page_content for c in chunks]
    if verbose:
        print(f'Creating vectors for {len(chunks_content)} chunks...')

    # Generate vectors
    vectors = embedding_model.embed_documents(chunks_content)
    if verbose:
        print(f'Vectors created! Dimension of each: {len(vectors[0])}')

    # Connect chunks with their vectors
    embedding_data = []
    for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
        embedding_data.append({
            'chunk': chunk,
            'embedding': vector,
            'metadata': chunk.metadata.copy(),
        })

    # Optional verbose output with preview
    if verbose:
        print('Embedding preview:')
        first_chunk = embedding_data[0]['chunk']
        first_vector = embedding_data[0]['embedding']
        first_metadata = embedding_data[0]['metadata']

        print(f'- Source {first_metadata.get('name', 'unknown')}')
        
        chunk_preview = first_chunk.page_content[:150].replace('\n', ' ')
        if len(first_chunk.page_content) > 150:
            chunk_preview += "..."
        print(f'- Chunk content: {chunk_preview}')
        print(f'- {[round(x, 3) for x in first_vector[:10]]}...')
        print("Phase 3: Document embedding finished!")

    return embedding_data