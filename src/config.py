# Central configuration for system

import os
from dotenv import load_dotenv
from dataclasses import dataclass

# Load API keys from .env file
load_dotenv()

@dataclass
class PathsConfig:
    """Paths to folders and files"""
    data_path: str = 'data'
    chroma_db_path: str = './chromadb'

@dataclass
class ChunkingConfig:
    """Text splitting parameters"""
    chunk_size: int = 800
    chunk_overlap: int = 150

@dataclass
class EmbeddingConfig:
    """Embedding model configuration"""
    model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    device: str = "cpu"
    normalize_embeddings: bool = True

@dataclass
class RetrievalConfig:
    """Search/retrieval parameters"""
    n_results: int = 5

@dataclass
class RerankingConfig:
    """Reranking model configuration"""
    enabled: bool = True
    model_name: str = "BAAI/bge-reranker-v2-m3"
    device: str = "cpu"
    n_candidates: int = 20
    n_final: int = 3

@dataclass
class LLMConfig:
    """Groq LLM configuration"""
    api_key: str = os.getenv('GROQ_API_KEY', '')
    model: str = 'llama-3.1-8b-instant'
    temperature: float = 0.15
    max_tokens: int = 512

# Singleton instances that will be used in all other files
paths = PathsConfig()
chunking = ChunkingConfig()
embedding = EmbeddingConfig()
retrieval = RetrievalConfig()
reranking = RerankingConfig()
llm = LLMConfig()