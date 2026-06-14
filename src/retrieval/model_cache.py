# Cache embedding model so it doesn't load every time while retrieval

from langchain_huggingface import HuggingFaceEmbeddings
from config import embedding

class ModelCache():
    """ 
    A singleton class that holds the embedding model in memory 
    throughout the duration of the program. 

    Call ModelCache.get_model() instead of creating a new one 
    HuggingFaceEmbeddings object directly. 
    """
    _model = None

    @classmethod
    def get_model(cls) -> HuggingFaceEmbeddings:
        """ 
        Returns the embedding model. 
        If the model is not loaded yet — loads it (only once). 
        Each subsequent call returns the already loaded model from memory. 
        """
        if cls._model is None:
            cls._model = HuggingFaceEmbeddings(
                model_name=embedding.model_name,
                model_kwargs={'device': embedding.device},
                encode_kwargs={'normalize_embeddings': embedding.normalize_embeddings}
            )
        
        print('Embedding model loaded and cached.')
        return cls._model
    
    @classmethod
    def clear_model(cls):
        """ 
        Deletes the model from memory. 
        Useful for testing or if you want to free up RAM. 
        """
        cls._model = None