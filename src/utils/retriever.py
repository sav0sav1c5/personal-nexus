# Retrieves relevant chunks from ChromaDB based on user query

import chromadb
from langchain_huggingface import HuggingFaceEmbeddings

# Must match the model used in embadder.py exactly
EMBEDDING_MODEL = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'

def load_embedding_model():
    model = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

    return model

def embed_query(query, embedding_model):

    return embedding_model.embed_query(query)

def retrieve(query, n_results):

    print("\n\nPhase 5: Retrieval starting...")

    # Load the same embedding model used in Phase 3
    embedding_model = load_embedding_model()

    # Convert the query text into a vector
    query_vector = embed_query(query, embedding_model)
    print(f'- Query embedded into vector of dimension: {len(query_vector)}')

    # Connect to the existing ChromaDB on disk
    db_client = chromadb.PersistentClient(path='./chromadb')
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
    
    print(f'- Retrieved {len(retrieved_chunks)} chunks:')

    for i, chunk in enumerate(retrieved_chunks):
        source = chunk['metadata'].get('name', 'unknown')
        similarity = chunk['similarity']
        preview = chunk['content'][:80].replace('\n', ' ')
        print(f'  [{i+1}] Source: {source} | Similarity: {similarity} | "{preview}..."')

    print("Phase 5: Retrieval finished!")

    return retrieved_chunks