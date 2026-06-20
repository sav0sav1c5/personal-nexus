# Reranks retrieved chunks using a cross-encoder model for higher precision

from config import reranking

class RerankerCache:

    _model = None