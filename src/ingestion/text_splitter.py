# Splits text into chunks

from langchain_core.documents import Document
from typing import List
from config import system

def split_documents(documents: List[Document], chunk_size: int, chunk_overlap: int, verbose: bool = False) -> None:
    """
    Placeholder function (not implemented).

    Args:
        documents (List[Document]): List of documents to split
        chunk_size (int): Maximum size of each chunk
        chunk_overlap (int): Overlap between chunks
        verbose (bool): If True, prints progress messages
    """
    pass

def split_text(documents: List[Document], chunk_size: int, chunk_overlap: int) -> List[Document]:
    """
    Splits documents into smaller chunks with natural boundaries and overlap.

    Args:
        documents (List[Document]): List of Document objects to split
        chunk_size (int): Maximum characters per chunk
        chunk_overlap (int): Characters to overlap between chunks
        verbose (bool): If True, prints progress messages

    Returns:
        List[Document]: List of chunk Documents with metadata (chunk_id, start, end, etc.)
    """

    if system.verbose_splitting:
        print("\n\nPhase 2: Text splitting starting...")

    chunks = []

    for doc_idx, doc in enumerate(documents):
        content = doc.page_content
        org_metadata = doc.metadata.copy()

        # If document is smaller than chunk_size, keep as single chunk
        if len(content) <= chunk_size:
            chunk_doc = Document(
                page_content=content,
                metadata = {
                    **org_metadata,
                    'chunk_id': 0,
                    'chunk_total': 1,
                    'chunk_start': 0,
                    'chunk_end': len(content),
                    'chunk_size': len(content)
                }
            )

            chunks.append(chunk_doc)
            continue

        # Split into chunks
        start = 0
        chunk_id = 0

        while start < len(content):
            end = min(start+chunk_size, len(content))

            # Find natural boundary (don't cut words in half)
            if end < len(content):
                for i in range(end, max(end - 50, start), -1):
                    if content[i] in [' ', '.', ',', '!', '?', ';', '\n']:
                        # Include natural end, do not cut in the middle off word
                        end = i + 1 
                        break

            # Extract chunk
            chunk_text = content[start:end].strip()
            
            if chunk_text:
                chunk_metadata = {
                    **org_metadata,
                    'chunk_id': chunk_id,
                    'chunk_start': start,
                    'chunk_end': end,
                    'chunk_size': len(chunk_text),
                }

                chunk_doc = Document(
                    page_content=chunk_text,
                    metadata=chunk_metadata
                )

                chunks.append(chunk_doc)
                chunk_id += 1

            # Check if we are on the end
            if end >= len(content):
                break
            
            # If not next chunk starts with overlap
            start = end - chunk_overlap

    if system.verbose_splitting:
        print(f'Number of created chunks: {len(chunks)}')
        print("Phase 2: Text splitting finished!")

    return chunks