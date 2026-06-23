# Reads and loads files from data/

import os
from pathlib import Path
from typing import List, Optional
from langchain_core.documents import Document
from pypdf import PdfReader
from config import system

def load_documents(path: str, doc_types='txt') -> Optional[List[Document]]:
    """
    Main entry point for document loading.

    Depending on doc_types, delegates loading to the appropriate loader
    (TXT or PDF) and returns a list of LangChain Document objects.

    Args:
        path (str): Path to folder containing documents
        doc_types (str): Document type to load ('txt' or 'pdf')
        verbose (bool): If True, prints progress logs

    Returns:
        List[Document]: Loaded documents with content + metadata
    """
    
    # Convert string path into Path object for easier file handling
    folder_path = Path(path)
    
    documents = []

    # Route to appropriate loader based on document type
    if doc_types == 'txt':
        documents = load_txt(folder_path=folder_path)
    else:
        documents = load_pdf(folder_path=folder_path)

    if system.verbose_loading:
        print(documents)

    return documents

def load_txt(folder_path: str):
    """
    Loads all TXT files from the specified folder.

    Each TXT file becomes one LangChain Document object.

    Metadata includes:
    - source path
    - filename
    - text length
    - file type

    Args:
        folder_path (Path): Folder containing txt files
        verbose (bool): If True, prints progress logs

    Returns:
        List[Document]
    """

    documents = []
    
    # Using the .glob('*.txt') function which returns all objects with the given extension
    for file_path in folder_path.glob('*.txt'):
        if system.verbose_loading:
            print(f'Loading: {file_path}')
        
        # Read entire file content into memory
        with open(file_path, 'r', encoding='utf-8') as file: 
            file_content = file.read()
        
        metadata = {
            'source': file_path,
            'name': os.path.basename(file_path),
            'size': len(file_content),
            'type': 'txt'
        }

        # Create LangChain document
        doc = Document(
            page_content=file_content,
            metadata=metadata
        )
            
        documents.append(doc)
    
    return documents

def load_pdf(folder_path: str):
    """
    Loads all PDF files from the specified folder.

    Each PDF is parsed page by page using pypdf.
    Extracted page text is merged into a single string.

    Each PDF becomes one LangChain Document object.

    Metadata includes:
    - source path
    - filename
    - extracted text size
    - file type
    - number of pages

    Args:
        folder_path (Path): Folder containing pdf files
        verbose (bool): If True, prints progress logs

    Returns:
        List[Document]
    """

    documents = []

    # Using the .glob('*.pdf') function which returns all objects with the given extension
    for file_path in folder_path.glob('*.pdf'):
        if system.verbose_loading:
            print(f'Loading: {file_path}')

        # Create PDF reader object
        reader = PdfReader(file_path)

        # Reset text accumulator for each PDF file
        complete_file = ""


        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                complete_file += page_text + "\n"
        
        metadata = {
            'source': file_path,
            'name': os.path.basename(file_path),
            'size': len(complete_file),
            'type': 'pdf',
            'pages': len(reader.pages)
        }

        # Create LangChain document
        doc = Document(
            page_content=complete_file,
            metadata=metadata
        )

        documents.append(doc)

    return documents