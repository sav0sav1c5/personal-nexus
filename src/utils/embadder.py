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

def create_embeddings(chunks: List[Document], verbose=False) -> List[Dict[str, Any]]:

    print("\n\nPhase 3: Document embadding starting...")

    if not chunks:
        print('No chunks for embedding!')
        return []
    
    # Embedding model initialization
    embedding_model = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

    # Prep chunks text for embedding
    chunks_content = [c.page_content for c in chunks]
    print(f'Cretaing vectors for {len(chunks_content)} chunks...')

    # Creating vectors chunks text
    vectors = embedding_model.embed_documents(chunks_content)
    print(f'Vectors created! Dimension of each: {len(vectors[0])}')

    # Prep returnign data - connecting chunks with their vectors
    embedding_data = []

    for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
        embedding_data.append({
            'chunk': chunk,
            'embedding': vector,
            'metadata': chunk.metadata.copy(),
        })

    if verbose:
        print('Embedding preview:')
        first_chunk = embedding_data[0]['chunk']
        first_vector = embedding_data[0]['embedding']
        first_metadata = embedding_data[0]['metadata']

        # Show file source
        print(f'- Source {first_metadata.get('name', 'unknown')}')
        
        # Show part of chunk
        chunk_preview = first_chunk.page_content[:150].replace('\n', ' ')
        if len(first_chunk.page_content) > 150:
            chunk_preview += "..."
        print(f'- Chunk content: {chunk_preview}')

        print(f'- {[round(x, 3) for x in first_vector[:10]]}...')

    print("Phase 3: Document embadding finished!")

    return embedding_data