# Reads and loads files from data/

import os
from pathlib import Path
from langchain_core.documents import Document 

def full_load(path):

    folder_path = Path(path)
    documents = []

    # Using the .glob('*.txt') function which returns all objects with the given extension
    for file_path in folder_path.glob('*.txt'):
        with open(file_path, 'r', encoding='utf-8') as file: 
            file_content = file.read()
        
        metadata = {
            'source': file_path,
            'name': os.path.basename(file_path),
            'size': len(file_content)
        }

        doc = Document(
            page_content=file_content,
            metadata=metadata
        )
        
        documents.append(doc)
    
    print(documents)

    return documents

def load_documents(path, full=False):

    print("\n\nPhase 1: Document loading starting...")
    
    if full:
        return full_load(path=path)
    else:
        with open(f'{path}/python_basics.txt', 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)
    
        with open(f'{path}/functions.txt', 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)

        with open(f'{path}/lists_and_dicts.txt', 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)

    print("Phase 1: Document loading finished!")