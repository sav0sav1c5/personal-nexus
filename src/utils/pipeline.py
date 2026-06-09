# Merges everything together into one RAG flow

from utils.document_loader import load_documents
from utils.text_splitter import split_text
from utils.embadder import create_embeddings
from utils.vector_store import store_vector

DATA_PATH = '../data'

def pipeline():

    load_documents(path=DATA_PATH)
    pass