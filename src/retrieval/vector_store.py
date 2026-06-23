# ChromaDB operations
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
from config import paths, system

def store_vector(embedding_data: Optional[List[Dict[str, Any]]] = None):
    """
    Stores vector embeddings in ChromaDB persistent database.

    Args:
        embedding_data (Optional[List[Dict[str, Any]]]): List from create_embeddings().
            Each dict contains 'chunk', 'embedding', and 'metadata'.
            If None, function returns early.
        verbose (bool): If True, prints progress messages

    Returns:
        Collection: ChromaDB collection object, or None if no data provided
    """

    if system.verbose_storing:
        print("\n\nPhase 4: Vector storing starting...")

    if embedding_data is None:
        if system.verbose_storing:
            print('No vectors for storing!')
        return None
    
    # Connecting with ChromaDB using PersistanceSclient
    # Save db on disk, not in memory (create directory /chromadb)
    db_client = chromadb.PersistentClient(path=paths.chroma_db_path)
    if system.verbose_storing:
        print('- Connection to ChromaDB successfully!')

    # Delete existing collection to avoid duplicates
    try:
        db_client.delete_collection('nexus_docs')
        if system.verbose_storing:
            print('- Previous docs collection deleted!')
    except:
        # Collection dont exist - continue
        pass

    # Create new collection
    collection = db_client.create_collection(
        name='nexus_docs',
        metadata={
            'description': 'Base project docs',
            'hnsw:space': 'cosine'
        }
    )

    # Prepare data for insertion with units (id, embeddings, metadatas, documents)
    ids = []
    embeddings = []
    metadatas = []
    documents = []

    for i, data in enumerate(embedding_data):
        chunk = data['chunk']
        embedding = data['embedding']
        metadata = data['metadata']

        # Create unique ID for each chunk
        file = metadata.get('name', 'unknown')
        chunk_id = metadata.get('chunk_id', i)
        unique_id = f'{file}_chunk_{chunk_id}'
        
        # Store data that will be saved in db for each chunk
        ids.append(unique_id)
        embeddings.append(embedding)
        metadatas.append({
            'source': str(metadata.get('source', 'unknown')),
            'name': file,
            'chunk_id': chunk_id,
            'size': metadata.get('chunk_size', 0)
        })
        documents.append(chunk.page_content)

    # Save to database
    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas,
        documents=documents
    )

    if system.verbose_storing:
        print(f'- Number of vectors saved in ChromaDB: {len(ids)}')
        print("Phase 4: Vector storing finished!")
    
    return collection