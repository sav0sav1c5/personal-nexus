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