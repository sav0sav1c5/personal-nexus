# Splits text into chunks

from langchain_core.documents import Document

def split_documents(documents, chunk_size, chunk_overlap):

    pass

def split_text(documents, chunk_size, chunk_overlap):

    print("\n\nPhase 2: Text splitting starting...")

    chunks = []

    for doc_idx, doc in enumerate(documents):
        content = doc.page_content
        org_metadata = doc.metadata.copy()

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

        # Splitting text into chunks
        start = 0
        chunk_id = 0

        while start < len(content):
            end = min(start+chunk_size, len(content))

            if end < len(content):
                for i in range(end, max(end - 50, start), -1):
                    if content[i] in [' ', '.', ',', '!', '?', ';', '\n']:
                        # Include natural end, do not cut in the middle off word
                        end = i + 1 
                        break

            # Cut chunk
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

    print(f'Number of created chunks: {len(chunks)}')
    print("Phase 2: Text splitting finished!")

    return chunks