# Cache embedding model so it doesn't load every time while retrieval

from langchain_huggingface import HuggingFaceEmbeddings
from config import embedding

class ModelCache():

    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            cls._model = HuggingFaceEmbeddings(
                model_name=embedding.model_name,
                model_kwargs={'device': embedding.device},
                encode_kwargs={'normalize_embeddings': embedding.normalize_embedding}
            )
        
        print('Embedding model loaded and cached.')
        return cls._model
    
    @classmethod
    def clear_model(cls):
        cls._model = None