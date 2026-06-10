# ChromaDB operations
import chromadb
from chromadb.config import Settings

def store_vector(embedding_data=None):

    print("\n\nPhase 4: Vector storing starting...")

    if embedding_data is None:
        print('No vectors for storing!')
        return None
    
    # Connecting with ChromaDB using PersistanceSclient
    # Save db on disk, not in memory (create directory /chromadb)
    db_client = chromadb.PersistentClient(path='./chromadb')
    print('- Connection to ChromaDB successfully!')

    # Check collections that exist so there is no duplicated data
    try:
        # Collection exists - delete it
        db_client.delete_collection('nexus_docs')
        print('- Previous docs collection deleted!')
    except:
        # Collection dont exist - continue
        pass

    # Create collection
    collection = db_client.create_collection(
        name='nexus_docs',
        metadata={
            'description': 'Base project docs',
            'hnsw:space': 'cosine'
        }
    )

    # Prep data to save in db, list with units (id, embeddings, metadatas, documents)
    ids = []
    embeddings = []
    metadatas = []
    documents = []

    for i, data in enumerate(embedding_data):
        chunk = data['chunk']
        embedding = data['embedding']
        metadata = data['metadata']

        # Create unique id for each chunk
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

    # Save in db
    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas,
        documents=documents
    )

    print(f'- Number of vectors saved in ChromaDB: {len(ids)}')
    print("Phase 4: Vector storing finished!")
    
    return collection