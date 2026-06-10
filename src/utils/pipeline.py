# Merges everything together into one RAG flow

from utils.document_loader import load_documents
from utils.text_splitter import split_text
from utils.embadder import create_embeddings
from utils.vector_store import store_vector
from utils.retriever import retrieve
from utils.generator import generate

DATA_PATH = 'data'

def pipeline(query=None):

    # Phase 1 - Document loading
    documents = load_documents(path=DATA_PATH, full=True)
    
    # Phase 2 - Text splitting
    chunks = split_text(documents, chunk_size=300, chunk_overlap=50)

    # Phase 3 - Embedding model
    embeddings = create_embeddings(chunks, verbose=True)

    # Phase 4 - Vector store
    store_vector(embedding_data=embeddings)

    # Phase 5 & 6 - Query pipeline (only if a question is provided)
    if query:
        retrieved_chunks = retrieve(query=query, n_results=3)
        answer = generate(query=query, retrieved_chunks=retrieved_chunks)

        print("\n\n========== ANSWER ==========")
        print(answer)
        print("============================")

        return answer