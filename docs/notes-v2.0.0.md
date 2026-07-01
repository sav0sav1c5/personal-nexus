### Progress of project:

#### Personal Nexus - version 2.0.0

##### Phase 1: Add model caching
Output:
```terminal
(.venv) ... personal-nexus> python src/main.py
Personal nexus running...
Information:
 - To exit enter X
 - Verbose mode: type "v: " before your question (e.g., "v: What is Python?")
 - Time measurement is always ON for queries

Enter Query: Sta su funkcije u Pythonu?
Starting pipeline at: 21:21:38
Loading weights: 100%|███████████████████████████████████| 199/199 [00:00<00:00, 4981.39it/s]
Embedding model loaded and cached.
Retrieval time: 11.10 seconds
Starting generation (streaming)...


========== ANSWER ==========
Funkcije u Pythonu su blokovi koda koji se mogu pozivati više puta sa različitim ulaznim parametrima. One omogućavaju ponavljanje koda i olakšavaju održavanje programa. Funkcije se mogu definisati koristeći ključnu reč def, a mogu primati argumente i vratiti vrijednosti.

Npr. funkcija saberi(a: int, b: int) -> int sabira dva cela broja i vraća njihov zbir, a funkcija podeli(a: float, b: float) -> tuple vraća količnik i ostatak.

[Source 3: functions.txt]
============================
Total pipeline time: 12.16 seconds
Enter Query: Mozes li mi reci nesto vise o Pandasu, za sta se koristi, kao i primere koricenja sa objasnjenjima?
Starting pipeline at: 21:21:53
Embedding model loaded and cached.
Retrieval time: 0.02 seconds
Starting generation (streaming)...


========== ANSWER ==========
Pandas je najvažnija biblioteka za rad sa tabelarnim podacima u Pythonu. Ona uvodi dve ključne strukture: Series (jednodimenzionalni niz, jedna kolona) i DataFrame (dvodimenzionalna tabela, više kolona). 

Pandas se koristi za manipulaciju i analizu podataka. Može se koristiti za učitavanje podataka iz različitih izvora, kao što je CSV datoteka, a zatim za kreiranje DataFrame-a koji se možedalje obrađivati.

Primer korišćenja Pandas-a je kreiranje DataFrame-a iz rečnika:
import pandas as pd

df = pd.DataFrame({
    'ime': ['Ana', 'Marko', 'Jelena', 'Nikola'],
    'godine': [25, 30, 22, 28],
    'grad': ['Beograd', 'Novi Sad', 'Niš', 'Beograd'],
})

Takođe, Pandas se može koristiti za učitavanje podataka iz CSV datoteke:
df = pd.read_csv('data.csv')

Nakon što su podaci učitani, mogu se dalje obrađivati i analizirati pomoću različitih funkcija i metoda koje Pandas nudi.

[Source 1: pandas_basics.txt, Source 3: pandas_basics.txt]
============================
Total pipeline time: 1.56 seconds
Enter Query: X
Goodbye!
(.venv) ... personal-nexus>
```

**Time for each query with model cache:**
- **Query 1:** from *11.56s* to *12.16s* (**same speed cuz model loading**)
- **Query 2:** from *8.90s* to *1.56s* (**model laoded - 7.34s faster**)


**Key learnings:**

1. **Singleton pattern:** Class-level variables live the entire program (while the module exists)
2. **`@classmethod` vs instance methods:** 
- Instance methods (`def method(self)`) require object creation
- Class methods (`@classmethod`) work directly on the class, without an instance

##### Phase 2: Chat Memory

Output:
```terminal
(.venv) ... personal-nexus> python src/main.py
Personal Nexus Commands:
  - X          : Exit the application
  - reset      : Clear conversation history
  - v: <query> : Run in verbose mode (e.g., "v: What is Python?")
  - <query>    : Regular query

Time measurement is always ON for queries.

Index found at: ./chromadb
Enter Query: Sta je Pandas?

Starting pipeline at: 14:45:02
Loading weights: 100%|█████████████████████████████| 199/199 [00:00<00:00, 8196.50it/s]
Embedding model loaded and cached.
Retrieval time: 10.97 seconds
Starting generation (streaming)...


========== ANSWER ==========
Pandas je najvažnija biblioteka za rad sa tabelarnim podacima u Pythonu. Ona uvodi dve ključne strukture: Series (jednodimenzionalni niz) i DataFrame (dvodimenzionalna tabela).

[Source 1: pandas_basics.txt]
============================
Total pipeline time: 11.59 seconds
Enter Query: Mozes li mi dati neke promere koricenja?

Starting pipeline at: 14:45:25
Embedding model loaded and cached.
Retrieval time: 0.02 seconds
Starting generation (streaming)...


========== ANSWER ==========
Da, mogu ti dati neke primere korišćenja funkcija sa parametrima i povratnom vrednošću.

Na primer, funkcija `pozdrav_osobu` iz [Source 1: functions.txt] prihvata ime kao parametar i vraća pozdravnu poruku. Može se koristiti na sledeći način:
rezultat = pozdrav_osobu("Marko")
print(rezultat)  # "Zdravo, Marko!"

Takođe, funkcija `pozdrav` iz [Source 2: functions.txt] prihvata ime i jezik kao parametre, i vraća pozdravnu poruku na odgovarajućem jeziku. Može se koristiti na sledeći način:
print(pozdrav("Ana"))                 # "Zdravo, Ana!"
print(pozdrav("Marko", "engleski"))   # "Hello, Marko!"
print(pozdrav("Lena", "nemački"))     # "Hallo, Lena!"

[Source 1: functions.txt], [Source 2: functions.txt]
============================
Total pipeline time: 1.10 seconds
Enter Query: X
Goodbye!
(.venv) ... personal-nexus>
```

##### Phase 3: PDF loading

Output:
```terminal
(.venv) ... personal-nexus> python src/main.py
Personal Nexus Commands:
  - X          : Exit the application
  - reset      : Clear conversation history
  - v: <query> : Run in verbose mode (e.g., "v: What is Python?")
  - <query>    : Regular query

Time measurement is always ON for queries.

No index found. Indexes will be created on first query!
Enter Query: Sta je RAGAS i kako se koristi za evaluaciju RAG sistema?

Loading weights: 100%|██████████████████████████████████████████████████████████████████████| 199/199 [00:00<00:00, 7224.67it/s]
Starting pipeline at: 10:36:17
Loading weights: 100%|██████████████████████████████████████████████████████████████████████| 199/199 [00:00<00:00, 7336.57it/s]
Embedding model loaded and cached.
Retrieval time: 8.01 seconds
Starting generation (streaming)...


========== ANSWER ==========
Evaluacija RAG sistema procenjuje kvalitet celog pipeline-a, koji obuhvata retrieval (pretraga) i generation (generisanje odgovora). To znači da se ne testira samo model, već ceo sistem. Glavne dimenzije evaluacije su Context Relevancy, koja se odnosi na to da li su pronađeni chunkovi zaista relevantni za pitanje, i Groundness. 

RAGAS se koristi u Python svetu, ali u C# ekosistemu moramo biti kreativni. 

[Source 1: evaluation-rag.pdf, Source 2: evaluation-rag.pdf]
============================
Total pipeline time: 8.92 seconds
Enter Query: Mozes li mi objasniti kako bi ziledala njegova implementacija u C#?

Starting pipeline at: 10:37:00
Embedding model loaded and cached.
Retrieval time: 0.03 seconds
Starting generation (streaming)...


========== ANSWER ==========
Implementacija RAGAS metrika u C# bi se odvijala kroz nekoliko koraka:

1. **Definisanje metrika**: Prvo, bi trebalo definisati metrike koje će se koristiti za evaluaciju RAG sistema. Ove metrike su:
 * Faithfulness
 * Answer relevancy
 * Context relevancy
 * Context recall

2. **Kreiranje prompt-a**: Za svaku metriku, bi trebalo kreirati prompt koji će se koristiti za evaluaciju. Na primer, za faithfulness metriku, prompt bi bio "Da li je odgovor koji je generisan od strane modela isti kao i odgovor koji je očekivan?"

3. **Pozivanje LLM-a**: Nakon što su prompt-i kreirani, bi trebalo pozvati LLM (Large Language Model) da oceni odgovore. Ovo se može učiniti koristeći Azure OpenAI ili Semantic Kernel.

4. **Parsiranje ocena**: Nakon što LLM vrati ocene, bi trebalo parsirati te ocene i agregirati rezultate.

5. **Integracija sa SearchController-om**: Konačno, bi trebalo integrirati evaluator sa SearchController-om kako bi se omogućilo automatsko evaluiranje RAG sistema.

Na primer, implementacija FaithfulnessMetric i Evaluator bi izgledala ovako:
```csharp
public class FaithfulnessMetric
{
    public string Prompt { get; set; }
    public string ExpectedAnswer { get; set; }
    public string GeneratedAnswer { get; set; }

    public bool Evaluate()
    {
        // Pozovi LLM da oceni odgovor
        var ocena = LLM.Evaluate(Prompt, ExpectedAnswer, GeneratedAnswer);

        // Parsiraj ocenu
        var rezultat = ParseOcena(ocena);

        return rezultat;
    }

    private bool ParseOcena(string ocena)
    {
        // Parsiraj ocenu i vrati rezultat
    }
}

public class Evaluator
{
    public List<FaithfulnessMetric> Metrike { get; set; }

    public void Evaluate()
    {
        foreach (var metrika in Metrike)
        {
            var rezultat
============================
Total pipeline time: 2.01 seconds
Enter Query: X
Goodbye!
(.venv) ... personal-nexus>
```

**Note:** Check what response size is because it returns unfinished part of code here - maybe configuration of LLM tokens and what he can return.

##### Phase 4: Evaluation using RAGAS

Evaluation needs to contain next 4 steps:
- **Dataset loading**
- **Metric definition** - answer relevancy, faithfullness, context precision and recall
  Metrics that exist in RAGAS (Context Precision, Context Recall, Context Entities Recall, Noise Sensitivity, Response Relevancy, Faithfulness, Multimodal Faithfulness, Multimodal Relevance)
- **Experiment execution**
- **Store results**

**What was implemented (RAGAS 0.4.x):**

The evaluation lives in `src/evaluation/` split into two files:
- `eval_config.py` - wires up the LLM judge, the embeddings, the metrics and the test dataset
- `evaluate.py` - the actual evaluation flow (collect -> format -> evaluate -> show)

Triggered from the interactive console with the `/eval` command (`parse_user_input` returns the `eval` action, `main.py` calls `run_evaluation`).

**1. Dataset loading**
- A hand-written "golden" dataset `TEST_QUESTIONS` (20 question / ground-truth pairs) covering every source document: functions, lists & dicts, machine learning, numpy, pandas, sql, statistics, visualization.
- `TEST_QUESTIONS_SUBSET = TEST_QUESTIONS[:3]` is used for quick runs so the Groq free-tier rate limits are not hit during every test.

**2. Metric definition**
Four core RAG metrics are instantiated as classes (0.4.x style) and the LLM/embeddings are injected into them:
- `Faithfulness` - is the answer grounded in the retrieved context (no hallucination)?
- `AnswerRelevancy` - does the answer actually address the question? (needs embeddings)
- `ContextPrecision` - are the retrieved chunks relevant / ranked well?
- `ContextRecall` - did retrieval bring back everything needed to cover the ground truth?

Judge configuration:
- **LLM judge:** Groq `llama-3.1-8b-instant` wrapped in `LangchainLLMWrapper` (temperature 0 for deterministic scoring).
- **Embeddings:** same multilingual MiniLM model wrapped in `LangchainEmbeddingsWrapper`.
- **RunConfig:** `timeout=120`, `max_retries=3`, `max_wait=30` - tuned to survive Groq rate-limit hiccups.

**3. Experiment execution**
`collect_data()` runs the RAG pipeline for each test question and packs the result into a `SingleTurnSample` (`user_input`, `response`, `retrieved_contexts`, `reference`). These are wrapped into a RAGAS `EvaluationDataset`, then `evaluate()` runs all four metrics.

**4. Store / show results**
`show_data()` prints the aggregate scores plus a per-question breakdown via `results.to_pandas()`.

Expected output shape (scores are illustrative):
```terminal
========== EVALUATION RESULTS ==========
{'faithfulness': 0.87, 'answer_relevancy': 0.91, 'context_precision': 0.79, 'context_recall': 0.83}

--- Detailed breakdown per question ---
                                     user_input  faithfulness  answer_relevancy  context_precision  context_recall
0   Kako definišemo funkciju u Pythonu...              1.00              0.94               0.83            1.00
1   Koja je razlika između parametra...               0.75              0.88               0.66            0.75
...
========================================
```

**Key learnings:**

1. **Golden dataset is the hard part:** the code is small; writing accurate `ground_truth` answers for every document is what actually determines whether the scores mean anything.
2. **LLM-as-a-judge:** RAGAS uses an LLM to grade an LLM. Temperature 0 on the judge makes scores reproducible.
3. **`SingleTurnSample` / `EvaluationDataset`** replaced the old HuggingFace `Dataset` format in RAGAS 0.4.x.
4. **Retrieval vs. full pipeline mismatch (known caveat):** `collect_data()` currently calls `retrieve(n_results=3)` directly and does **not** run the reranker (Phase 5). So the evaluation measures the *bi-encoder-only* pipeline, not the reranked one that the app actually serves. `TODO`: route eval through the same `pipeline()` path (or share a common retrieval function) so eval and production match.

##### Phase 5: Reranker

By adding the reranker I am trying to solve a problem that occurs and I have seen it: Irrelevant chenks with close vectors keep coming back from the retriever.

**The idea - two-stage retrieval:**

A single bi-encoder (the embedding model) is fast but imprecise: it compares the query vector to chunk vectors independently, so semantically "close but wrong" chunks slip through. A cross-encoder reads the query and the chunk *together* and scores them jointly, which is far more accurate but too slow to run over the whole database. The fix is to combine them:

```terminal
Query
  │
  ▼
Stage 1: bi-encoder (fast, wide net)   ──►  retrieve n_candidates = 20
  │
  ▼
Stage 2: cross-encoder (slow, precise) ──►  rerank + threshold, keep n_final = 3
  │
  ▼
Generator
```

**What was implemented (`src/retrieval/reranker.py`):**
- **Model:** `BAAI/bge-reranker-v2-m3` (multilingual cross-encoder, works with Serbian) via `sentence-transformers` `CrossEncoder`.
- **`RerankerCache`** singleton - same class-level caching pattern as `ModelCache` from Phase 1, so the cross-encoder loads only once.
- **Scoring:** the cross-encoder outputs raw logits (unbounded, can be negative). They are pushed through `torch.sigmoid` to normalize into `[0, 1]`, so the threshold has a stable, model-independent meaning.
- **Relevance threshold:** `min_rerank_score = 0.1` filters out weak chunks **before** the top-N cut. This is the actual solution to the "irrelevant close-vector chunks" problem - a chunk that survives the bi-encoder but scores low on the cross-encoder is dropped even if it would have made the top 3.
- **Config toggle:** `RerankingConfig.enabled`. `pipeline()` branches on it - if reranking is off it falls back to the plain `retrieve(n_results=5)` behavior, which keeps the old path testable.

**Config (`RerankingConfig` in `config.py`):**

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `enabled` | `True` | master on/off switch |
| `model_name` | `BAAI/bge-reranker-v2-m3` | cross-encoder |
| `n_candidates` | `20` | how many chunks the bi-encoder pulls (stage 1) |
| `n_final` | `3` | how many survive after reranking (stage 2) |
| `min_rerank_score` | `0.1` | drop anything below this after sigmoid |

**Key learnings:**

1. **Bi-encoder vs. cross-encoder:** bi-encoder = two separate vectors compared by cosine (fast, cacheable). Cross-encoder = one model pass over the (query, chunk) pair (accurate, not cacheable). Retrieve wide + rerank narrow gets both.
2. **Normalize before thresholding:** raw logits are not comparable across models; sigmoid gives a fixed `[0, 1]` scale so `min_rerank_score` is meaningful.
3. **Filter before truncating:** applying the threshold *before* `top_n` means a query with few good matches can return fewer than 3 chunks instead of padding with junk.

##### Phase 6: Centralized system config & verbose refactor

Motivation: in v1.0.0 a `verbose` (and later `measure_time`) flag was threaded through **every** function signature - `load_documents(..., verbose)`, `retrieve(..., verbose)`, `generate(..., verbose)`, etc. Adding one new toggle meant editing the whole call chain. This phase removes that.

**What changed (`config.py`):**
- Added a `SystemConfig` dataclass holding `measure_time` plus one verbose flag **per pipeline stage** (`verbose_loading`, `verbose_splitting`, `verbose_embedding`, `verbose_storing`, `verbose_retrieval`, `verbose_reranking`, `verbose_generation`, `verbose_indexing`).
- Exposed as a singleton `system = SystemConfig()`.
- Every module now imports `from config import system` and reads `system.verbose_*` directly instead of receiving a `verbose` parameter.
- All the `verbose` parameters were removed from function signatures across ingestion / retrieval / generation.
- Config values are now singleton dataclass instances (`paths`, `chunking`, `embedding`, `retrieval`, `reranking`, `llm`, `system`) - a single source of truth.

**Side effect:** the old `"v: "` per-query verbose prefix mode is gone. Verbose logging is now configured centrally rather than per query (the help text and `parse_user_input` no longer advertise it), and you can enable logging for a **single** stage (e.g. only reranking) instead of all-or-nothing.

**Key learnings:**

1. **Single source of truth beats parameter threading:** central config removes the "change 8 files to add one flag" problem.
2. **Per-stage granularity:** splitting one `verbose` into per-stage flags makes debugging one phase (e.g. only the reranker) much cleaner.
3. **Dataclass singletons** give typed, discoverable, IDE-autocompletable settings versus scattered module-level constants.

---

### Suggestions / next steps (for the CV project)

Ideas ranked roughly by learning-value-per-effort. These are things that are *not yet done* and would each make a strong bullet point / demo.

**High value, small effort**
- **README is out of date** - it still documents `src/utils/pipeline.py`, `llama-3.3-70b-versatile`, chunk size 300, and the `v:` verbose mode. None of these match the current code (modular `ingestion/retrieval/generation`, `llama-3.1-8b-instant`, chunk 800/overlap 150, central config). Update it - recruiters read the README first.
- **Fix the `/eval` control flow** - in `main.py`, after `run_evaluation()` the code falls through into `pipeline(query=None, ...)` instead of `continue`-ing back to the prompt. Also `format_help()` never mentions the `/eval` command.
- **Make eval measure the real pipeline** - route `collect_data()` through the reranked retrieval path (see Phase 4 caveat) so the RAGAS scores reflect what users actually get.
- **Add unit tests (pytest)** - even a handful (text splitter boundaries, `parse_user_input`, context builder formatting, reranker threshold logic). "Has tests" is a big signal on a CV.
- **`.env.example` + config via env vars** - lets anyone clone and run; shows you think about onboarding.

**Medium effort, high signal**
- **Before/after evaluation table** - run RAGAS with reranking off vs. on and record the metric deltas in these notes. This turns Phase 5 from "I added a reranker" into "I measured a +X% context-precision gain" - a quantified, interview-ready result.
- **Wrap it in a REST API (FastAPI)** - `POST /query`, `POST /eval`, streaming via SSE. Turns a console script into a deployable service.
- **Minimal web UI (Streamlit or a tiny React page)** - a chat box + shows retrieved sources. Very demo-able / screenshottable for a portfolio.
- **Source citations with scores in the UI** - you already carry `similarity` and `rerank_score` on each chunk; surface them so answers are explainable.
- **Dockerize** - a `Dockerfile` + `docker-compose` (app + ChromaDB). "Containerized" is a common JD keyword.

**Bigger, resume-headline features**
- **Incremental / smart indexing** - right now `store_vector` deletes and rebuilds the whole collection every run. Hash files and only re-embed changed ones (upsert). Good systems-thinking talking point.
- **HyDE (Hypothetical Document Embeddings)** - generate a hypothetical answer, embed *that*, retrieve on it. Pairs naturally with the reranker and is a recognizable advanced-RAG technique.
- **Query rewriting / multi-query retrieval** - use the LLM to expand or rephrase the query into several, retrieve for each, merge. Helps with the "close but wrong" problem too.
- **Semantic / structure-aware chunking** - the README already lists this as a limitation; implementing it (e.g. splitting on headings/code blocks) shows depth beyond fixed-size chunks.
- **CI (GitHub Actions)** - run the tests + linter on push. Green badge on the README.
- **Observability** - log per-query retrieval scores / latencies to a file or lightweight dashboard; ties back nicely to the "Designing Machine Learning Systems" book already in `data/`.

**Portfolio polish**
- Record a short GIF/asciinema of a live query + `/eval` run and embed it in the README.
- Write a short "architecture decisions" section (why cross-encoder reranking, why multilingual MiniLM, why Groq) - shows reasoning, not just code.

