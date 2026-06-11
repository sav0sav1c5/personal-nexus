# Personal Nexus
A complete **Retrieval-Augmented Generation (RAG)** system built from scratch for learning purposes. The system loads your text documents, creates vector embeddings, and allows you to ask questions to your documents using a large language model.

---

## Screenshots

```
Personal nexus running...                                                              
Information:                   
 - To exit enter X
 - Verbose mode: type "v: " before your question (e.g., "v: What is Python?")
 - Time measurement is always ON for queries

Enter Query: Sta su funkcije u Pythonu?
Starting pipeline at: 22:07:39
Loading weights: 100%|████████████████████████████| 199/199 [00:00<00:00, 7337.02it/s]
Query time (retrieval + generation): 11.56 seconds


========== ANSWER ==========
Funkcije u Pythonu su blok koda koji se definiše jednom, a može se pozivati više puta. Definisanje funkcije koristi ključnu reč def.

[Source 3: functions.txt]
============================
Total pipeline time: 11.56 seconds
```

---

## What This Project Does

### 1. Document Indexing Pipeline
A complete pipeline that processes your documents:
- **Document loading** — Loads all `.txt` files from the `data/` folder
- **Text splitting** — Splits documents into chunks with natural boundaries and overlap
- **Embedding** — Converts chunks into vector embeddings using multilingual model
- **Vector storage** — Saves vectors to ChromaDB for persistent storage

### 2. Semantic Search
When you ask a question, the system:
- Converts your question into a vector using the same embedding model
- Finds the most similar chunks in ChromaDB using cosine similarity
- Returns the top 3 most relevant chunks with similarity scores

### 3. LLM-Powered Answer Generation
The retrieved chunks are sent to Groq's LLM (llama-3.3-70b-versatile) which:
- Answers based ONLY on the provided context
- Cites which sources were used
- Says "I don't know" if the answer isn't in the context

### 4. Interactive Console
- Ask unlimited questions in a loop
- Type `X` to exit
- Prefix with `v: ` for verbose/debug mode
- Time measurement for each query

### 5. Streaming Responses
Answers appear **word by word** as they are generated, instead of waiting 10+ seconds for the complete response. This dramatically improves perceived performance - you see the first words in ~1 second.

---

## Architecture

```
personal-nexus/
├── src/
│   ├── main.py                    ← Entry point, interactive console
│   └── utils/
│       ├── document_loader.py     ← Loads .txt files
│       ├── text_splitter.py       ← Chunking with overlap
│       ├── embedder.py            ← Vector embeddings
│       ├── vector_store.py        ← ChromaDB operations
│       ├── retriever.py           ← Semantic search
│       ├── generator.py           ← Groq LLM integration
│       ├── model_cache.py         ← Caches embedding model
│       └── pipeline.py            ← Orchestrates all phases
├── data/                          ← Your .txt documents
├── chromadb/                      ← Vector database (auto-created)
├── .env                           ← API keys (not in git)
└── requirements.txt               ← Python dependencies
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.9+ |
| Document loading | LangChain |
| Text splitting | Custom recursive splitter |
| Embeddings | sentence-transformers (paraphrase-multilingual-MiniLM-L12-v2) |
| Vector database | ChromaDB |
| LLM | Groq (llama-3.3-70b-versatile) |
| API integration | Groq SDK |
| Environment | python-dotenv |

---

## Pipeline Phases

| Phase | Component | What It Does |
|-------|-----------|--------------|
| 1 | Document Loader | Loads .txt files from `data/` folder |
| 2 | Text Splitter | Splits into chunks (300 chars, 50 overlap) |
| 3 | Embedding | Converts chunks to vectors (384 dimensions) |
| 4 | Vector Store | Saves vectors to ChromaDB |
| 5 | Retriever | Finds 3 most similar chunks for your question |
| 6 | Generator | LLM generates answer based on retrieved chunks |

---

## Running Locally

### Prerequisites
- Python 3.9+
- Groq API key (free, no credit card required)

### Step 1 — Clone and set up environment

```bash
git clone https://github.com/YOUR_USERNAME/personal-nexus.git
cd personal-nexus

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2 — Add your documents

Place your `.txt` files in the `data/` folder:

```
data/
├── python_basics.txt
├── functions.txt
├── lists_and_dicts.txt
├── pandas_basics.txt
├── numpy_basics.txt
├── visualization.txt
├── machine_learning.txt
├── sql_for_ds.txt
└── statistics.txt
```

### Step 3 — Configure API key

Create a `.env` file:

```bash
# .env
GROQ_API_KEY=gsk_your_groq_api_key_here
```

Get your free Groq API key at [console.groq.com](https://console.groq.com)

### Step 4 — Run the system

```bash
python src/main.py
```

### Step 5 — Ask questions

```
Personal nexus running...
Information:
 - To exit enter X
 - Verbose mode: type "v: " before your question (e.g., "v: What is Python?")
 - Time measurement is always ON for queries

Enter Query: Sta su funkcije u Pythonu?
```

---

## Configuration

### Chunk Size and Overlap

In `src/utils/pipeline.py`:

```python
chunks = split_text(documents, chunk_size=300, chunk_overlap=50)
```

| Parameter | Default | When to change |
|-----------|---------|----------------|
| `chunk_size` | 300 | Increase for longer documents, decrease for precise retrieval |
| `chunk_overlap` | 50 | Increase to preserve more context at boundaries (10-20% of chunk_size) |

### Number of Retrieved Chunks

In `src/utils/pipeline.py`:

```python
retrieved_chunks = retrieve(query=query, n_results=3, verbose=verbose)
```

Higher values = more context but larger prompts (slower, more expensive).

### Embedding Model

In `src/utils/embadder.py` and `src/utils/retriever.py`:

```python
EMBEDDING_MODEL = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
```

| Model | Dimensions | Languages | Size |
|-------|------------|-----------|------|
| all-MiniLM-L6-v2 | 384 | English only | 80MB |
| paraphrase-multilingual-MiniLM-L12-v2 | 384 | 50+ languages (Serbian!) | 120MB |

### LLM Model

In `src/utils/generator.py`:

```python
model='llama-3.3-70b-versatile'
```

| Parameter | Value | Effect |
|-----------|-------|--------|
| `temperature` | 0.2 | Lower = more factual, higher = more creative |
| `max_tokens` | 512 | Maximum length of generated answer |

---

## Time Measurement

Time is automatically measured for:
- **Query time** — retrieval + generation (the actual Q&A)
- **Total pipeline time** — including document loading and indexing

Use this to:
- Compare performance between different chunk sizes
- Identify bottlenecks (embedding vs. LLM generation)
- Track improvements

---

## Known Limitations & Future Improvements

| Limitation | Planned Improvement |
|------------|---------------------|
| Only `.txt` files | Add PDF, Word, HTML support |
| No chat memory | Add conversation history |
| Basic chunking | Add semantic chunking |
| No reranking | Add Cohere/Cross-encoder reranker |
| No HyDE | Add hypothetical document embeddings |

---

## Author

**GitHub:** [github.com/sav0sav1c5/](https://github.com/sav0sav1c5)

Built as a learning project to understand:
- How RAG systems work under the hood
- Vector embeddings and semantic search
- LLM integration and prompt engineering
- Building production-ready Python applications