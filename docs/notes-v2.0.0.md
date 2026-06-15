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

(.venv) ... personal-nexus>
```