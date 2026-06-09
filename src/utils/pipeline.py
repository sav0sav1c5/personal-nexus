# Merges everything together into one RAG flow

from utils.document_loader import load_documents
from utils.text_splitter import split_text
from utils.embadder import create_embeddings
from utils.vector_store import store_vector

DATA_PATH = 'data'

def pipeline():

    # Phase 1 - Document loading
    load_documents(path=DATA_PATH)
    
    # Phase 2 - Text splitting
    split_text()

    # Phase 3 - Embedding model
    create_embeddings()

    # Phase 4 - Vector store
    store_vector()