### Progress of project:

#### Personal Nexus - version 1.0.0

**Infrastructure:**
```terminal
User asks: "Objasni mi funkcije u Python-u?"
                    ↓
        1. Document loader (loads files)
                    ↓
        2. Text splitter (divides into chunks)
                    ↓
        3. Embedding (converting into vectors)
                    ↓
        4. Vector store (stores in ChromaDB)
                    ↓
        5. Retriever (finds the 3 most similar chunks)
                    ↓
        6. Generator (Groq LLM provides the answer)
                    ↓
        Answer: "Funkcije se definišu sa def..."
```

##### Part 1: Document loading

Output:
```terminal
(.venv) ... personal-nexus> python src/main.py
Personal nexus running...


Phase 1: Document loading starting...
[Document(metadata={'source': WindowsPath('data/functions.txt'), 'name': 'functions.txt', 'size': 661}, page_content='Funkcija je blok koda koji se definiše jednom, a može se pozivati više puta.\n\nDefinisanje funkcije koristi ključnu reč def:\n\ndef pozdrav(ime):\n    return f"Zdravo, {ime}!"\n\nrezultat = pozdrav("Marko")\nprint(rezultat)  # Zdravo, Marko!\n\nParametri i argumenti:\n- Parametar je promenljiva u definiciji funkcije (ime)\n- Argument je vrednost koja se prosleđuje pri pozivu ("Marko")\n\nPodrazumevane vrednosti parametara:\ndef pozdrav(ime, jezik="srpski"):\n    if jezik == "srpski":\n        return f"Zdravo, {ime}!"\n    return f"Hello, {ime}!"\n\nLambda funkcije:\nLambda je anonimna funkcija koja se piše u jednoj liniji.\nkvadrat = lambda x: x ** 2\nprint(kvadrat(5))  # 25'), Document(metadata={'source': WindowsPath('data/lists_and_dicts.txt'), 'name': 'lists_and_dicts.txt', 'size': 725}, page_content='Lista je uređena kolekcija elemenata koji mogu biti različitih tipova.\n\nKreiranje i indeksiranje:\nvoce = ["jabuka", "kruška", "banana"]\nprint(voce[0])   # jabuka\nprint(voce[-1])  # banana (poslednji element)\n\nMetode liste:\nvoce.append("grožđe")    # dodaje na kraj\nvoce.insert(1, "mango")  # dodaje na poziciju\nvoce.remove("kruška")    # briše po vrednosti\nvoce.pop()               # briše i vraća poslednji\n\nRečnik (dict) čuva podatke u parovima ključ-vrednost:\nstudent = {\n    "ime": "Ana",\n    "godine": 20,\n    "prosek": 9.5\n}\n\nPristup vrednostima:\nprint(student["ime"])           # Ana\nprint(student.get("godine"))    # 20\n\nIteracija kroz rečnik:\nfor kljuc, vrednost in student.items():\n    print(f"{kljuc}: {vrednost}")'), Document(metadata={'source': WindowsPath('data/python_basics.txt'), 'name': 'python_basics.txt', 'size': 601}, page_content='Python je interpretirani programski jezik visokog nivoa, kreiran od strane Gvida van Rosuma 1991. godine.\n\nKarakteristike Python-a:\n- Čitljiva i jasna sintaksa koja podseća na pseudokod\n- Dinamično tipiziran jezik — ne mora se deklarisati tip promenljive\n- Interpretiran jezik — kod se izvršava liniju po liniju\n- Bogata standardna biblioteka poznata kao "batteries included"\n\nPromenljive u Python-u:\nPromenljiva se kreira jednostavnim dodeljivanjem vrednosti.\nime = "Ana"\ngodina = 2024\nvisina = 1.75\naktivna = True\n\nPython podržava više tipova podataka: int, float, str, bool, list, dict, tuple, set.')]


Phase 2: Text splitting starting...
Phase 2: Text splitting finished!


Phase 3: Document embadding starting...
Phase 3: Document embadding finished!


Phase 4: Vector storing starting...
Phase 4: Vector storing finished!
```

##### Part 2: Text splitting into chunks

Output:
```terminal
(.venv) ... personal-nexus> python src/main.py
Personal nexus running...


Phase 1: Document loading starting...
[Document(metadata={'source': WindowsPath('data/functions.txt'), 'name': 'functions.txt', 'size': 661}, page_content='Funkcija je blok koda koji se definiše jednom, a može se pozivati više puta.\n\nDefinisanje funkcije koristi ključnu reč def:\n\ndef pozdrav(ime):\n    return f"Zdravo, {ime}!"\n\nrezultat = pozdrav("Marko")\nprint(rezultat)  # Zdravo, Marko!\n\nParametri i argumenti:\n- Parametar je promenljiva u definiciji funkcije (ime)\n- Argument je vrednost koja se prosleđuje pri pozivu ("Marko")\n\nPodrazumevane vrednosti parametara:\ndef pozdrav(ime, jezik="srpski"):\n    if jezik == "srpski":\n        return f"Zdravo, {ime}!"\n    return f"Hello, {ime}!"\n\nLambda funkcije:\nLambda je anonimna funkcija koja se piše u jednoj liniji.\nkvadrat = lambda x: x ** 2\nprint(kvadrat(5))  # 25'), Document(metadata={'source': WindowsPath('data/lists_and_dicts.txt'), 'name': 'lists_and_dicts.txt', 'size': 725}, page_content='Lista je uređena kolekcija elemenata koji mogu biti različitih tipova.\n\nKreiranje i indeksiranje:\nvoce = ["jabuka", "kruška", "banana"]\nprint(voce[0])   # jabuka\nprint(voce[-1])  # banana (poslednji element)\n\nMetode liste:\nvoce.append("grožđe")    # dodaje na kraj\nvoce.insert(1, "mango")  # dodaje na poziciju\nvoce.remove("kruška")    # briše po vrednosti\nvoce.pop()               # briše i vraća poslednji\n\nRečnik (dict) čuva podatke u parovima ključ-vrednost:\nstudent = {\n    "ime": "Ana",\n    "godine": 20,\n    "prosek": 9.5\n}\n\nPristup vrednostima:\nprint(student["ime"])           # Ana\nprint(student.get("godine"))    # 20\n\nIteracija kroz rečnik:\nfor kljuc, vrednost in student.items():\n    print(f"{kljuc}: {vrednost}")'), Document(metadata={'source': WindowsPath('data/python_basics.txt'), 'name': 'python_basics.txt', 'size': 601}, page_content='Python je interpretirani programski jezik visokog nivoa, kreiran od strane Gvida van Rosuma 1991. godine.\n\nKarakteristike Python-a:\n- Čitljiva i jasna sintaksa koja podseća na pseudokod\n- Dinamično tipiziran jezik — ne mora se deklarisati tip promenljive\n- Interpretiran jezik — kod se izvršava liniju po liniju\n- Bogata standardna biblioteka poznata kao "batteries included"\n\nPromenljive u Python-u:\nPromenljiva se kreira jednostavnim dodeljivanjem vrednosti.\nime = "Ana"\ngodina = 2024\nvisina = 1.75\naktivna = True\n\nPython podržava više tipova podataka: int, float, str, bool, list, dict, tuple, set.')]


Phase 2: Text splitting starting...
Number of created chunks: 9
Phase 2: Text splitting finished!


Phase 3: Document embadding starting...
Phase 3: Document embadding finished!


Phase 4: Vector storing starting...
Phase 4: Vector storing finished!
```


##### Part 3: Document embedding

Output:
```terminal
(.venv) ... personal-nexus> python src/main.py
Personal nexus running...


Phase 1: Document loading starting...
[Document(metadata={'source': WindowsPath('data/functions.txt'), 'name': 'functions.txt', 'size': 661}, page_content='Funkcija je blok koda koji se definiše jednom, a može se pozivati više puta.\n\nDefinisanje funkcije koristi ključnu reč def:\n\ndef pozdrav(ime):\n    return f"Zdravo, {ime}!"\n\nrezultat = pozdrav("Marko")\nprint(rezultat)  # Zdravo, Marko!\n\nParametri i argumenti:\n- Parametar je promenljiva u definiciji funkcije (ime)\n- Argument je vrednost koja se prosleđuje pri pozivu ("Marko")\n\nPodrazumevane vrednosti parametara:\ndef pozdrav(ime, jezik="srpski"):\n    if jezik == "srpski":\n        return f"Zdravo, {ime}!"\n    return f"Hello, {ime}!"\n\nLambda funkcije:\nLambda je anonimna funkcija koja se piše u jednoj liniji.\nkvadrat = lambda x: x ** 2\nprint(kvadrat(5))  # 25'), Document(metadata={'source': WindowsPath('data/lists_and_dicts.txt'), 'name': 'lists_and_dicts.txt', 'size': 725}, page_content='Lista je uređena kolekcija elemenata koji mogu biti različitih tipova.\n\nKreiranje i indeksiranje:\nvoce = ["jabuka", "kruška", "banana"]\nprint(voce[0])   # jabuka\nprint(voce[-1])  # banana (poslednji element)\n\nMetode liste:\nvoce.append("grožđe")    # dodaje na kraj\nvoce.insert(1, "mango")  # dodaje na poziciju\nvoce.remove("kruška")    # briše po vrednosti\nvoce.pop()               # briše i vraća poslednji\n\nRečnik (dict) čuva podatke u parovima ključ-vrednost:\nstudent = {\n    "ime": "Ana",\n    "godine": 20,\n    "prosek": 9.5\n}\n\nPristup vrednostima:\nprint(student["ime"])           # Ana\nprint(student.get("godine"))    # 20\n\nIteracija kroz rečnik:\nfor kljuc, vrednost in student.items():\n    print(f"{kljuc}: {vrednost}")'), Document(metadata={'source': WindowsPath('data/python_basics.txt'), 'name': 'python_basics.txt', 'size': 601}, page_content='Python je interpretirani programski jezik visokog nivoa, kreiran od strane Gvida van Rosuma 1991. godine.\n\nKarakteristike Python-a:\n- Čitljiva i jasna sintaksa koja podseća na pseudokod\n- Dinamično tipiziran jezik — ne mora se deklarisati tip promenljive\n- Interpretiran jezik — kod se izvršava liniju po liniju\n- Bogata standardna biblioteka poznata kao "batteries included"\n\nPromenljive u Python-u:\nPromenljiva se kreira jednostavnim dodeljivanjem vrednosti.\nime = "Ana"\ngodina = 2024\nvisina = 1.75\naktivna = True\n\nPython podržava više tipova podataka: int, float, str, bool, list, dict, tuple, set.')]


Phase 2: Text splitting starting...
Number of created chunks: 9
Phase 2: Text splitting finished!


Phase 3: Document embadding starting...
Loading weights: 100%|████████████████████████████| 103/103 [00:00<00:00, 6781.89it/s]
Cretaing vectors for 9 chunks...
Vectors created! Dimension of each: 384
Embedding preview:
- Source unknown
- Chunk content: Funkcija je blok koda koji se definiše jednom, a može se pozivati više puta.  Definisanje funkcije koristi ključnu reč def:  def pozdrav(ime):     ret...
- [-0.067, 0.11, -0.055, -0.034, -0.116, -0.019, 0.136, 0.041, 0.024, -0.027]...
Phase 3: Document embadding finished!


Phase 4: Vector storing starting...
Phase 4: Vector storing finished!
```

##### Part 4: Vector store

Output:
```terminal
(.venv) ... personal-nexus> python src/main.py
Personal nexus running...


Phase 1: Document loading starting...
[Document(metadata={'source': WindowsPath('data/functions.txt'), 'name': 'functions.txt', 'size': 661}, page_content='Funkcija je blok koda koji se definiše jednom, a može se pozivati više puta.\n\nDefinisanje funkcije koristi ključnu reč def:\n\ndef pozdrav(ime):\n    return f"Zdravo, {ime}!"\n\nrezultat = pozdrav("Marko")\nprint(rezultat)  # Zdravo, Marko!\n\nParametri i argumenti:\n- Parametar je promenljiva u definiciji funkcije (ime)\n- Argument je vrednost koja se prosleđuje pri pozivu ("Marko")\n\nPodrazumevane vrednosti parametara:\ndef pozdrav(ime, jezik="srpski"):\n    if jezik == "srpski":\n        return f"Zdravo, {ime}!"\n    return f"Hello, {ime}!"\n\nLambda funkcije:\nLambda je anonimna funkcija koja se piše u jednoj liniji.\nkvadrat = lambda x: x ** 2\nprint(kvadrat(5))  # 25'), Document(metadata={'source': WindowsPath('data/lists_and_dicts.txt'), 'name': 'lists_and_dicts.txt', 'size': 725}, page_content='Lista je uređena kolekcija elemenata koji mogu biti različitih tipova.\n\nKreiranje i indeksiranje:\nvoce = ["jabuka", "kruška", "banana"]\nprint(voce[0])   # jabuka\nprint(voce[-1])  # banana (poslednji element)\n\nMetode liste:\nvoce.append("grožđe")    # dodaje na kraj\nvoce.insert(1, "mango")  # dodaje na poziciju\nvoce.remove("kruška")    # briše po vrednosti\nvoce.pop()               # briše i vraća poslednji\n\nRečnik (dict) čuva podatke u parovima ključ-vrednost:\nstudent = {\n    "ime": "Ana",\n    "godine": 20,\n    "prosek": 9.5\n}\n\nPristup vrednostima:\nprint(student["ime"])           # Ana\nprint(student.get("godine"))    # 20\n\nIteracija kroz rečnik:\nfor kljuc, vrednost in student.items():\n    print(f"{kljuc}: {vrednost}")'), Document(metadata={'source': WindowsPath('data/python_basics.txt'), 'name': 'python_basics.txt', 'size': 601}, page_content='Python je interpretirani programski jezik visokog nivoa, kreiran od strane Gvida van Rosuma 1991. godine.\n\nKarakteristike Python-a:\n- Čitljiva i jasna sintaksa koja podseća na pseudokod\n- Dinamično tipiziran jezik — ne mora se deklarisati tip promenljive\n- Interpretiran jezik — kod se izvršava liniju po liniju\n- Bogata standardna biblioteka poznata kao "batteries included"\n\nPromenljive u Python-u:\nPromenljiva se kreira jednostavnim dodeljivanjem vrednosti.\nime = "Ana"\ngodina = 2024\nvisina = 1.75\naktivna = True\n\nPython podržava više tipova podataka: int, float, str, bool, list, dict, tuple, set.')]


Phase 2: Text splitting starting...
Number of created chunks: 9
Phase 2: Text splitting finished!


Phase 3: Document embadding starting...
Loading weights: 100%|████████████████████████████| 103/103 [00:00<00:00, 6781.89it/s]
Cretaing vectors for 9 chunks...
Vectors created! Dimension of each: 384
Embedding preview:
- Source unknown
- Chunk content: Funkcija je blok koda koji se definiše jednom, a može se pozivati više puta.  Definisanje funkcije koristi ključnu reč def:  def pozdrav(ime):     ret...
- [-0.067, 0.11, -0.055, -0.034, -0.116, -0.019, 0.136, 0.041, 0.024, -0.027]...
Phase 3: Document embadding finished!


Phase 4: Vector storing starting...
- Connection to ChromaDB successfully!
- Previous docs collection deleted!
- Number of vectors saved in ChromaDB: 9
Phase 4: Vector storing finished!
```

##### Part 5: Retrieval

Output:
```terminal
(.venv) ... personal-nexus> python src/main.py
Personal nexus running...


Phase 1: Document loading starting...
[Document(metadata={'source': WindowsPath('data/functions.txt'), 'name': 'functions.txt', 'size': 661}, page_content='Funkcija je blok koda koji se definiše jednom, a može se pozivati više puta.\n\nDefinisanje funkcije koristi ključnu reč def:\n\ndef pozdrav(ime):\n    return f"Zdravo, {ime}!"\n\nrezultat = pozdrav("Marko")\nprint(rezultat)  # Zdravo, Marko!\n\nParametri i argumenti:\n- Parametar je promenljiva u definiciji funkcije (ime)\n- Argument je vrednost koja se prosleđuje pri pozivu ("Marko")\n\nPodrazumevane vrednosti parametara:\ndef pozdrav(ime, jezik="srpski"):\n    if jezik == "srpski":\n        return f"Zdravo, {ime}!"\n    return f"Hello, {ime}!"\n\nLambda funkcije:\nLambda je anonimna funkcija koja se piše u jednoj liniji.\nkvadrat = lambda x: x ** 2\nprint(kvadrat(5))  # 25'), Document(metadata={'source': WindowsPath('data/lists_and_dicts.txt'), 'name': 'lists_and_dicts.txt', 'size': 725}, page_content='Lista je uređena kolekcija elemenata koji mogu biti različitih tipova.\n\nKreiranje i indeksiranje:\nvoce = ["jabuka", "kruška", "banana"]\nprint(voce[0])   # jabuka\nprint(voce[-1])  # banana (poslednji element)\n\nMetode liste:\nvoce.append("grožđe")    # dodaje na kraj\nvoce.insert(1, "mango")  # dodaje na poziciju\nvoce.remove("kruška")    # briše po vrednosti\nvoce.pop()               # briše i vraća poslednji\n\nRečnik (dict) čuva podatke u parovima ključ-vrednost:\nstudent = {\n    "ime": "Ana",\n    "godine": 20,\n    "prosek": 9.5\n}\n\nPristup vrednostima:\nprint(student["ime"])           # Ana\nprint(student.get("godine"))    # 20\n\nIteracija kroz rečnik:\nfor kljuc, vrednost in student.items():\n    print(f"{kljuc}: {vrednost}")'), Document(metadata={'source': WindowsPath('data/python_basics.txt'), 'name': 'python_basics.txt', 'size': 601}, page_content='Python je interpretirani programski jezik visokog nivoa, kreiran od strane Gvida van Rosuma 1991. godine.\n\nKarakteristike Python-a:\n- Čitljiva i jasna sintaksa koja podseća na pseudokod\n- Dinamično tipiziran jezik — ne mora se deklarisati tip promenljive\n- Interpretiran jezik — kod se izvršava liniju po liniju\n- Bogata standardna biblioteka poznata kao "batteries included"\n\nPromenljive u Python-u:\nPromenljiva se kreira jednostavnim dodeljivanjem vrednosti.\nime = "Ana"\ngodina = 2024\nvisina = 1.75\naktivna = True\n\nPython podržava više tipova podataka: int, float, str, bool, list, dict, tuple, set.')]


Phase 2: Text splitting starting...
Number of created chunks: 9
Phase 2: Text splitting finished!


Phase 3: Document embadding starting...
Loading weights: 100%|████████████████████████████| 103/103 [00:00<00:00, 6781.89it/s]
Cretaing vectors for 9 chunks...
Vectors created! Dimension of each: 384
Embedding preview:
- Source unknown
- Chunk content: Funkcija je blok koda koji se definiše jednom, a može se pozivati više puta.  Definisanje funkcije koristi ključnu reč def:  def pozdrav(ime):     ret...
- [-0.067, 0.11, -0.055, -0.034, -0.116, -0.019, 0.136, 0.041, 0.024, -0.027]...
Phase 3: Document embadding finished!


Phase 4: Vector storing starting...
- Connection to ChromaDB successfully!
- Previous docs collection deleted!
- Number of vectors saved in ChromaDB: 9
Phase 4: Vector storing finished!

Phase 5: Retrieval starting...
Loading weights: 100%|██████████████████████████████████| 199/199 [00:00<00:00, 5779.68it/s]
- Query embedded into vector of dimension: 384
- Retrieved 3 chunks:
  [1] Source: python_basics.txt | Similarity: 0.5868 | "Python je interpretirani programski jezik visokog nivoa, kreiran od strane Gvida..."
  [2] Source: python_basics.txt | Similarity: 0.5631 | "1.75 aktivna = True  Python podržava više tipova podataka: int, float, str, bool..."
  [3] Source: functions.txt | Similarity: 0.5607 | "Funkcija je blok koda koji se definiše jednom, a može se pozivati više puta.  De..."
Phase 5: Retrieval finished!
```

##### Part 6: Answer generator

Output:
```terminal
(.venv) ... personal-nexus> python src/main.py
Personal nexus running...


Phase 1: Document loading starting...
[Document(metadata={'source': WindowsPath('data/functions.txt'), 'name': 'functions.txt', 'size': 661}, page_content='Funkcija je blok koda koji se definiše jednom, a može se pozivati više puta.\n\nDefinisanje funkcije koristi ključnu reč def:\n\ndef pozdrav(ime):\n    return f"Zdravo, {ime}!"\n\nrezultat = pozdrav("Marko")\nprint(rezultat)  # Zdravo, Marko!\n\nParametri i argumenti:\n- Parametar je promenljiva u definiciji funkcije (ime)\n- Argument je vrednost koja se prosleđuje pri pozivu ("Marko")\n\nPodrazumevane vrednosti parametara:\ndef pozdrav(ime, jezik="srpski"):\n    if jezik == "srpski":\n        return f"Zdravo, {ime}!"\n    return f"Hello, {ime}!"\n\nLambda funkcije:\nLambda je anonimna funkcija koja se piše u jednoj liniji.\nkvadrat = lambda x: x ** 2\nprint(kvadrat(5))  # 25'), Document(metadata={'source': WindowsPath('data/lists_and_dicts.txt'), 'name': 'lists_and_dicts.txt', 'size': 725}, page_content='Lista je uređena kolekcija elemenata koji mogu biti različitih tipova.\n\nKreiranje i indeksiranje:\nvoce = ["jabuka", "kruška", "banana"]\nprint(voce[0])   # jabuka\nprint(voce[-1])  # banana (poslednji element)\n\nMetode liste:\nvoce.append("grožđe")    # dodaje na kraj\nvoce.insert(1, "mango")  # dodaje na poziciju\nvoce.remove("kruška")    # briše po vrednosti\nvoce.pop()               # briše i vraća poslednji\n\nRečnik (dict) čuva podatke u parovima ključ-vrednost:\nstudent = {\n    "ime": "Ana",\n    "godine": 20,\n    "prosek": 9.5\n}\n\nPristup vrednostima:\nprint(student["ime"])           # Ana\nprint(student.get("godine"))    # 20\n\nIteracija kroz rečnik:\nfor kljuc, vrednost in student.items():\n    print(f"{kljuc}: {vrednost}")'), Document(metadata={'source': WindowsPath('data/python_basics.txt'), 'name': 'python_basics.txt', 'size': 601}, page_content='Python je interpretirani programski jezik visokog nivoa, kreiran od strane Gvida van Rosuma 1991. godine.\n\nKarakteristike Python-a:\n- Čitljiva i jasna sintaksa koja podseća na pseudokod\n- Dinamično tipiziran jezik — ne mora se deklarisati tip promenljive\n- Interpretiran jezik — kod se izvršava liniju po liniju\n- Bogata standardna biblioteka poznata kao "batteries included"\n\nPromenljive u Python-u:\nPromenljiva se kreira jednostavnim dodeljivanjem vrednosti.\nime = "Ana"\ngodina = 2024\nvisina = 1.75\naktivna = True\n\nPython podržava više tipova podataka: int, float, str, bool, list, dict, tuple, set.')]


Phase 2: Text splitting starting...
Number of created chunks: 9
Phase 2: Text splitting finished!


Phase 3: Document embadding starting...
Loading weights: 100%|████████████████████████████| 103/103 [00:00<00:00, 6781.89it/s]
Cretaing vectors for 9 chunks...
Vectors created! Dimension of each: 384
Embedding preview:
- Source unknown
- Chunk content: Funkcija je blok koda koji se definiše jednom, a može se pozivati više puta.  Definisanje funkcije koristi ključnu reč def:  def pozdrav(ime):     ret...
- [-0.067, 0.11, -0.055, -0.034, -0.116, -0.019, 0.136, 0.041, 0.024, -0.027]...
Phase 3: Document embadding finished!


Phase 4: Vector storing starting...
- Connection to ChromaDB successfully!
- Previous docs collection deleted!
- Number of vectors saved in ChromaDB: 9
Phase 4: Vector storing finished!

Phase 5: Retrieval starting...
Loading weights: 100%|██████████████████████████████████| 199/199 [00:00<00:00, 5779.68it/s]
- Query embedded into vector of dimension: 384
- Retrieved 3 chunks:
  [1] Source: python_basics.txt | Similarity: 0.5868 | "Python je interpretirani programski jezik visokog nivoa, kreiran od strane Gvida..."
  [2] Source: python_basics.txt | Similarity: 0.5631 | "1.75 aktivna = True  Python podržava više tipova podataka: int, float, str, bool..."
  [3] Source: functions.txt | Similarity: 0.5607 | "Funkcija je blok koda koji se definiše jednom, a može se pozivati više puta.  De..."
Phase 5: Retrieval finished!


Phase 6: Answer generation starting...
- Prompt built with 3 context chunks
- Sending request to Groq (llama-3.3-70b-versatile)...
Phase 6: Answer generation finished!


========== ANSWER ==========
Funkcija u Python-u je blok koda koji se definiše jednom, a može se pozivati više puta. Definisanje funkcije koristi ključnu reč def. Funkcija može imati parametre, koji su promenljive u definiciji funkcije. Kada se funkcija poziva, u nju se prosleđuju argumenti koji se zatim koriste u funkciji.

[Source 3: functions.txt]
```
