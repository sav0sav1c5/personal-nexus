# Single retrieval entry point shared by the pipeline and the evaluation.
# Keeps "how we fetch context for a query" in ONE place, so the app and the
# RAGAS evaluation always measure the exact same retrieval behavior.

from typing import List, Dict, Any
from config import retrieval, reranking
from retrieval.retriever import retrieve
from retrieval.reranker import rerank

def get_relevant_chunks(query: str) -> List[Dict[str, Any]]:
    """
    Returns the final context chunks for a query.

    Two-stage retrieval when reranking is enabled:
      1. bi-encoder pulls a WIDE candidate set (reranking.n_candidates)
      2. cross-encoder reranks + thresholds them down to reranking.n_final

    Falls back to plain bi-encoder retrieval when reranking is disabled.

    Args:
        query (str): User's question

    Returns:
        List[Dict[str, Any]]: Final chunks to feed into the generator
    """

    if reranking.enabled:
        candidate_chunks = retrieve(query=query, n_results=reranking.n_candidates)
        return rerank(query=query, chunks=candidate_chunks, top_n=reranking.n_final)

    return retrieve(query=query, n_results=retrieval.n_results)
