# Reranks retrieved chunks using a cross-encoder model for higher precision

from typing import List, Dict, Any
from sentence_transformers import CrossEncoder
from config import reranking
import torch

class RerankerCache:
    """
    Singleton class that holds the cross-encoder model in memory,
    following the same pattern as ModelCache for the embedding model.
    """

    _model = None

    @classmethod
    def get_model(cls) -> CrossEncoder:
        if cls._model is None:
            cls._model = CrossEncoder(
                reranking.model_name,
                device=reranking.device
            )
        return cls._model

    @classmethod
    def clear_model(cls):
        cls._model = None

def rerank(
        query: str,
        chunks: List[Dict[str, Any]],
        top_n: int = 3,
        verbose: bool = False
) -> List[Dict[str, Any]]:
    """
    Reranks retrieved chunks using a cross-encoder for higher precision
    relevance scoring than cosine similarity alone.

    Args:
        query (str): User's question
        chunks (List[Dict[str, Any]]): Chunks returned by retrieve()
        top_n (int): Number of top chunks to keep after reranking
        verbose (bool): If True, prints progress messages

    Returns:
        List[Dict[str, Any]]: Reranked chunks, sorted by rerank_score descending,
                               truncated to top_n
    """

    if verbose:
        print("\n\nPhase 5b: Reranking starting...")

    if not chunks:
        if verbose:
            print('- No chunks to rerank!')
        return []

    model = RerankerCache.get_model()

    # Cross-encoder expects pairs of [query, document_text]
    pairs = [[query, chunk['content']] for chunk in chunks]

    # predict() returns a list of relevance scores, one per pair
    # Raw logits from the model (can be negative, unlimited range)
    raw_scores = model.predict(pairs)

    # Normalize to [0, 1] via sigmoid function, so that the threshold has a stable meaning
    normalized_scores = torch.sigmoid(torch.tensor(raw_scores)).tolist()
    
    # Attach the score to each chunk dict so it survives downstream
    for chunk, score in zip(chunks, normalized_scores):
        chunk['rerank_score'] = float(score)

    # Filtering BEFORE cutting on top_n - this is the essence of the relevance threshold
    filtered_chunks = [
        chunk for chunk in chunks
        if chunk['rerank_score'] >= reranking.min_rerank_score
    ]

    if verbose:
        discarded = len(chunks) - len(filtered_chunks)
        if discarded > 0:
            print(f'- Discarded {discarded} chunks below threshold {reranking.min_rerank_score}')

    # Sort by rerank_score, highest first
    reranked_chunks = sorted(
        chunks,
        key=lambda c: c['rerank_score'],
        reverse=True
    )

    result = reranked_chunks[:top_n]

    if verbose:
        print(f'- Reranked {len(chunks)} chunks down to top {len(result)}:')
        for i, chunk in enumerate(result):
            source = chunk['metadata'].get('name', 'unknown')
            score = chunk['rerank_score']
            preview = chunk['content'][:80].replace('\n', ' ')
            print(f'  [{i+1}] Source: {source} | Rerank score: {score:.4f} | "{preview}..."')
        
        print("Phase 5b: Reranking finished!")

    return result