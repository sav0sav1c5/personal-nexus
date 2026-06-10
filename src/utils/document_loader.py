# Reads and loads files from data/

import os
from pathlib import Path
from typing import List, Optional
from langchain_core.documents import Document

def full_load(path: str, verbose: bool = False) -> List[Document]:
    """
    Loads all .txt files from a folder and returns a list of Document objects.

    Args:
        path (str): Path to the folder (e.g., "data")
        verbose (bool): If True, prints progress messages
    
    Returns:
        List[Document]: List of documents with content and metadata (source, name, size)
    """

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
    
    if verbose:
        print(documents)

    return documents

def load_documents(path: str, full: bool = False, verbose: bool = False) -> Optional[List[Document]]:
    """
    Main function for loading documents.

    Args:
        path (str): Path to the folder
        full (bool): True = load all files, False = test mode (prints 3 examples)
        verbose (bool): If True, prints progress messages
    
    Returns:
        Optional[List[Document]]: List of documents if full=True, otherwise None
    """
    
    if verbose:
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

    if verbose:
        print("Phase 1: Document loading finished!")
        
    return None