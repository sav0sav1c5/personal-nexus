import os
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from ragas.metrics import Faithfulness, AnswerRelevancy, ContextPrecision, ContextRecall
from ragas.run_config import RunConfig

# Configure Groq LLM through the LangChain wrapper
groq_llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv('GROQ_API_KEY', ''),
    temperature=0,
    max_tokens=512,
    max_retries=2,
    timeout=15,
    n=1
)

ragas_llm = LangchainLLMWrapper(groq_llm)

run_config = RunConfig(
    timeout=120,    # seconds per call (default is 60)
    max_retries=3,  # number of retries before giving up
    max_wait=30     # maximum wait between attempts
)

# Configure the embedding model through the LangChain wrapper
hf_embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
ragas_embeddings = LangchainEmbeddingsWrapper(hf_embeddings)

# Instantiate metrics and inject LLM/embeddings into them
# In 0.4.x, metrics are classes you instantiate, not out-of-the-box instances
METRICS = [
    Faithfulness(llm=ragas_llm,),
    AnswerRelevancy(llm=ragas_llm, embeddings=ragas_embeddings),
    ContextPrecision(llm=ragas_llm),
    ContextRecall(llm=ragas_llm),
]

TEST_QUESTIONS = [
    # ============================================================
    # FUNKCIJE (functions.txt)
    # ============================================================
    {
        'question': 'Kako definišemo funkciju u Pythonu i zašto su funkcije važne u programiranju?',
        'ground_truth': 'Funkcija je blok koda koji se definiše jednom, a može se pozivati više puta. Definiše se korišćenjem ključne reči def, nakon čega sledi ime funkcije, parametri u zagradama, i telo funkcije koje se piše sa uvlačenjem (indentacijom). Osnovna sintaksa je: def ime_funkcije(parametri): \"\"\"Dokumentacija (docstring)\"\"\" # Telo funkcije return vrednost. Funkcije omogućavaju: ponovno korišćenje koda (DRY - Don\'t Repeat Yourself), modularnost (razbijanje koda na manje celine), lakše testiranje i održavanje, i apstrakciju (skrivanje složenosti).'
    },
    # Metadata: functions.txt -> "ŠTA SU FUNKCIJE?" i "DEFINISANJE FUNKCIJE"
    
    {
        'question': 'Koja je razlika između parametra i argumenta u Python funkcijama? Navedi primere.',
        'ground_truth': 'Parametar je promenljiva koja se navodi u definiciji funkcije. To je "šablon" za vrednosti koje će funkcija primiti. Argument je stvarna vrednost koja se prosleđuje funkciji prilikom poziva. Primer: def info(ime, godine, grad): # ime, godine, grad su PARAMETRI print(f"{ime} ima {godine} godina i živi u {gradu}.") info("Ana", 25, "Beograd") # "Ana", 25, "Beograd" su ARGUMENTI. Postoje dve vrste argumenata: pozicioni argumenti - redosled je bitan: info("Ana", 25, "Beograd") i imenovani argumenti - redosled nije bitan: info(grad="Niš", ime="Marko", godine=30).'
    },
    # Metadata: functions.txt -> "PARAMETRI I ARGUMENTI"
    
    {
        'question': 'Kako Python tretira podrazumevane vrednosti parametara? Zašto je sledeći kod problematičan: def problematcna_funkcija(item, lista=[]): lista.append(item) return lista i kako ga ispraviti?',
        'ground_truth': 'Podrazumevane vrednosti parametara se u Pythonu evaluiraju samo jednom - u trenutku definisanja funkcije, a ne prilikom svakog poziva. To znači da ako se kao podrazumevana vrednost koristi promenljivi objekat (poput liste), taj objekat će biti deljen između svih poziva funkcije. Problem: print(problematcna_funkcija(1)) # [1], print(problematcna_funkcija(2)) # [1, 2] - NE OČEKUJE SE! Lista se ne resetuje pri svakom pozivu. Ispravan način je korišćenje None kao podrazumevane vrednosti: def ispravna_funkcija(item, lista=None): if lista is None: lista = [] lista.append(item) return lista.'
    },
    # Metadata: functions.txt -> "PODRAZUMEVANE VREDNOSTI PARAMETARA"
    
    {
        'question': 'Šta su *args i **kwargs u Pythonu i kada se koriste? Navedi primere.',
        'ground_truth': '*args omogućava funkciji da primi proizvoljan broj pozicionih argumenata koji se unutar funkcije tretiraju kao tuple. **kwargs omogućava funkciji da primi proizvoljan broj imenovanih argumenata koji se tretiraju kao dictionary. Primer sa *args: def suma(*brojevi): return sum(brojevi) print(suma(1, 2, 3)) # 6. Primer sa **kwargs: def info(**podaci): for kljuc, vrednost in podaci.items(): print(f"{kljuc}: {vrednost}") info(ime="Ana", godine=25, grad="Beograd"). Kombinovanje: def sve_zajedno(obavezni, *args, **kwargs): print(f"Obavezni: {obavezni}") print(f"Args: {args}") print(f"Kwargs: {kwargs}"). Ovi konstrukti su posebno korisni za fleksibilne API pozive, dekoratore, i situacije kada unapred ne znamo koliko argumenata će funkcija primiti.'
    },
    # Metadata: functions.txt -> "PROIZVOLJAN BROJ ARGUMENATA"
    
    # ============================================================
    # LISTE I REČNICI (lists_and_dicts.txt)
    # ============================================================
    {
        'question': 'Kako se kreira rečnik (dictionary) u Pythonu i koje su najvažnije metode za rad sa njim?',
        'ground_truth': 'Rečnici se kreiraju pomoću vitičastih zagrada {} sa parovima ključ: vrednost. Ključevi moraju biti jedinstveni i nepromenljivi (string, broj, tuple). Primer: student = { "ime": "Ana", "godine": 20, "prosek": 9.5, "aktivan": True }. Najvažnije metode: get(kljuc, default) - bezbedan pristup vrednosti, keys() - vraća sve ključeve, values() - vraća sve vrednosti, items() - vraća parove (ključ, vrednost), update(dict) - dodaje ili ažurira više ključeva, pop(kljuc) - uklanja i vraća vrednost, clear() - briše sve elemente. Provera postojanja: if "ime" in student.'
    },
    # Metadata: lists_and_dicts.txt -> "REČNICI"
    
    {
        'question': 'Šta je list comprehension i kako se koristi? Navedi primere sa i bez uslova.',
        'ground_truth': 'List comprehension je elegantan i efikasan način za kreiranje listi. Sintaksa: [izraz for element in iterable if uslov]. Primer bez uslova: kvadrati = [i ** 2 for i in range(10)] # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]. Primer sa uslovom: parni_kvadrati = [i ** 2 for i in range(20) if i % 2 == 0]. Primer sa if-else: znakovi = ["pozitivan" if x > 0 else "negativan" if x < 0 else "nula" for x in [-3, 0, 5]]. Ugnježdena lista: matrica = [[i + j for j in range(3)] for i in range(3)]. List comprehension je efikasniji i čitljiviji od tradicionalnih petlji za jednostavne transformacije podataka.'
    },
    # Metadata: lists_and_dicts.txt -> "List comprehension"
    
    {
        'question': 'Kako funkcioniše defaultdict iz collections modula? Navedi primere za brojanje i grupisanje.',
        'ground_truth': 'defaultdict je specijalan tip rečnika koji automatski kreira podrazumevanu vrednost za ključ koji ne postoji, umesto da baca KeyError. Prilikom kreiranja, prosleđuje se funkcija koja vraća podrazumevanu vrednost. Primer za brojanje: from collections import defaultdict; brojac = defaultdict(int); for slovo in "abracadabra": brojac[slovo] += 1 # {"a": 5, "b": 2, ...}. Primer za grupisanje: ocene = [("Ana", 5), ("Marko", 4), ("Ana", 4)]; ocene_po_studentu = defaultdict(list); for student, ocena in ocene: ocene_po_studentu[student].append(ocena) # {"Ana": [5, 4], "Marko": [4]}. Ovo je posebno korisno u RAG sistemima za grupisanje relevantnih chunkova po metapodacima.'
    },
    # Metadata: lists_and_dicts.txt -> "DefaultDict"
    
    # ============================================================
    # MAŠINSKO UČENJE (machine_learning.txt)
    # ============================================================
    {
        'question': 'Koja je razlika između train_test_split i unakrsne validacije (cross-validation) u Scikit-learnu?',
        'ground_truth': 'train_test_split deli podatke jednom na trening i test skup (npr. 80% za trening, 20% za test). Ovo je jednostavno i brzo, ali procena modela zavisi od toga kako su podaci podeljeni. Unakrsna validacija (cross-validation) deli podatke više puta na različite načine. Na primer, 5-fold unakrsna validacija deli podatke na 5 delova, trenira model na 4 dela, testira na preostalom delu, i ponavlja ovaj proces 5 puta. Rezultat je prosek performansi iz svih 5 iteracija. Primer: from sklearn.model_selection import train_test_split, cross_val_score, KFold; X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42); kfold = KFold(n_splits=5, shuffle=True, random_state=42); scores = cross_val_score(model, X, y, cv=kfold, scoring="accuracy"). Prednosti cross-validation: robusnija procena performansi, bolje korišćenje podataka, manja zavisnost od slučajne podele.'
    },
    # Metadata: machine_learning.txt -> "1. PRIPREMA PODATAKA"
    
    {
        'question': 'Objasni koncept standardizacije podataka (StandardScaler) u Scikit-learnu. Zašto je važna i kako se primenjuje?',
        'ground_truth': 'Standardizacija je proces transformacije podataka tako da imaju sredinu (mean) 0 i standardnu devijaciju 1. Formula: z = (x - μ) / σ. U Scikit-learnu se koristi StandardScaler: from sklearn.preprocessing import StandardScaler; scaler = StandardScaler(); X_scaled = scaler.fit_transform(X_train); X_test_scaled = scaler.transform(X_test). Važna je jer: mnogi ML algoritmi (SVM, logistička regresija, PCA, KNN) su osetljivi na skalu karakteristika, karakteristike sa većim vrednostima dominiraju u izračunavanju udaljenosti, i poboljšava konvergenciju optimizacionih algoritama. VAŽNO: fit_transform se koristi samo na trening podacima, a transform na test podacima - ovo sprečava "curenje" informacija iz test skupa u trening.'
    },
    # Metadata: machine_learning.txt -> "2. STANDARDIZACIJA I NORMALIZACIJA"
    
    {
        'question': 'Kako se evaluiraju klasifikacioni modeli? Objasni metrike: accuracy, precision, recall i F1-score.',
        'ground_truth': 'Accuracy (tačnost): procenat tačno klasifikovanih primera, formula: (TP + TN) / (TP + TN + FP + FN). Korisna kada su klase uravnotežene. Precision (preciznost): od svih primera koje je model klasifikovao kao pozitivne, koliko je zaista pozitivnih, formula: TP / (TP + FP). Važna kada su lažno pozitivni skupi (npr. spam filteri). Recall (osetljivost): od svih stvarno pozitivnih primera, koliko je model uspeo da detektuje, formula: TP / (TP + FN). Važna kada su lažno negativni skupi (npr. medicinska dijagnostika). F1-score: harmonijska sredina precision i recall, formula: 2 * (Precision * Recall) / (Precision + Recall). Korisna kada imamo nebalansirane klase. Primer: from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score; y_pred = model.predict(X_test); accuracy = accuracy_score(y_test, y_pred).'
    },
    # Metadata: machine_learning.txt -> "5. EVALUACIJA KLASIFIKATORA"
    
    # ============================================================
    # NUMPY (numpy_basics.txt)
    # ============================================================
    {
        'question': 'Šta je NumPy i koje su njegove osnovne strukture podataka? Kako se kreiraju nizovi?',
        'ground_truth': 'NumPy (Numerical Python) je osnovna biblioteka za rad sa višedimenzionalnim nizovima i matricama. Omogućava brze matematičke operacije i predstavlja temelj za pandas, scikit-learn, tensorflow i druge DS biblioteke. Osnovna struktura je ndarray (N-dimenzionalni niz), koji može biti 1D (vektor), 2D (matrica) ili 3D+ (tenzori). Kreiranje: import numpy as np; arr = np.array([1, 2, 3, 4, 5]); zeros_arr = np.zeros((3, 4)); ones_arr = np.ones((2, 3)); identity = np.eye(3); range_arr = np.arange(0, 10, 2); linspace_arr = np.linspace(0, 1, 5); random_uniform = np.random.rand(3, 3); random_normal = np.random.randn(3, 3).'
    },
    # Metadata: numpy_basics.txt -> "ŠTA JE NUMPY?" i "KREIRANJE NUMPY NIZOVA"
    
    {
        'question': 'Kako se u NumPy-u izračunava kosinusna sličnost između dva vektora? Zašto je ovo važno za RAG sisteme?',
        'ground_truth': 'Kosinusna sličnost se izračunava kao kosinus ugla između dva vektora. Formula: cos(θ) = (a · b) / (||a|| * ||b||). U NumPy-u: def cosine_similarity(a, b): return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)). Primer: vector1 = np.array([1, 2, 3]); vector2 = np.array([2, 4, 6]); cosine_similarity(vector1, vector2) # 1.0. Važnost za RAG: embedding vektori su upravo NumPy nizovi - predstavljaju semantičke reprezentacije dokumenata i upita; kosinusna sličnost se koristi za pronalaženje najsličnijih vektora - osnovni mehanizam pretrage u RAG-u; normalizacija vektora (norm = 1) je ključna za efikasnu pretragu; brzina NumPy operacija omogućava efikasnu pretragu kroz velike kolekcije vektora.'
    },
    # Metadata: numpy_basics.txt -> "PRAKTIČNI PRIMERI" (Primer 3)
    
    # ============================================================
    # PANDAS (pandas_basics.txt)
    # ============================================================
    {
        'question': 'Koje su osnovne strukture podataka u Pandas biblioteci i kako se kreiraju?',
        'ground_truth': 'Pandas uvodi dve ključne strukture podataka: Series - jednodimenzionalni niz (jedna kolona) sa indeksom, i DataFrame - dvodimenzionalna tabela sa redovima i kolonama (više Series objekata). Kreiranje DataFrame-a iz rečnika: import pandas as pd; df = pd.DataFrame({ "ime": ["Ana", "Marko", "Jelena"], "godine": [25, 30, 22], "grad": ["Beograd", "Novi Sad", "Niš"] }). Kreiranje iz liste: data = [[1, "Ana", 25], [2, "Marko", 30]]; df = pd.DataFrame(data, columns=["id", "ime", "godine"]). Učitavanje iz fajlova: df_csv = pd.read_csv("podaci.csv"); df_excel = pd.read_excel("podaci.xlsx"); df_json = pd.read_json("podaci.json").'
    },
    # Metadata: pandas_basics.txt -> "ŠTA JE PANDAS?" i "KREIRANJE DATAFRAME-OVA"
    
    {
        'question': 'Kako se u Pandas-u vrši filtriranje podataka i grupisanje sa agregacijama? Navedi primere.',
        'ground_truth': 'Filtriranje se vrši korišćenjem uslova unutar []: filtered = df[df["godine"] > 25]; filtered = df[(df["godine"] > 25) & (df["plata"] > 50000)]; filtered = df[df["ime"].str.startswith("A")]. Grupisanje i agregacije se vrše pomoću groupby() i agg(): grouped = df.groupby("grad")["plata"].mean(); result = df.groupby("grad").agg({ "plata": ["mean", "min", "max", "count"], "godine": "mean" }); result = df.groupby("grad").agg( prosecna_plata=("plata", "mean"), max_plata=("plata", "max"), prosecne_godine=("godine", "mean"), broj_zaposlenih=("ime", "count") ).'
    },
    # Metadata: pandas_basics.txt -> "SELEKCIJA PODATAKA" i "GRUPISANJE I AGREGACIJE"
    
    {
        'question': 'Objasni upotrebu apply funkcije u Pandas-u. Kako se primenjuje na redove i kolone?',
        'ground_truth': 'apply funkcija omogućava primenu korisnički definisane funkcije na svaki red ili kolonu DataFrame-a. Parametar axis=0 (podrazumevano) primenjuje funkciju na kolone, a axis=1 na redove. Primena na kolone: def kategorija_plate(plata): if plata < 50000: return "Niska" elif plata < 70000: return "Srednja" else: return "Visoka"; df["kategorija_plate"] = df["plata"].apply(kategorija_plate). Primena na redove: def calculate_bonus(row): return row["plata"] * 0.1 if row["godine"] > 25 else row["plata"] * 0.05; df["bonus"] = df.apply(calculate_bonus, axis=1). Alternativa - map za preslikavanje: grad_map = {"Beograd": "BG", "Novi Sad": "NS"}; df["grad_kod"] = df["grad"].map(grad_map).'
    },
    # Metadata: pandas_basics.txt -> "PRIMENA FUNKCIJA NAD PODACIMA"
    
    # ============================================================
    # SQL (sql_for_ds.txt)
    # ============================================================
    {
        'question': 'Kako se u SQL-u vrši grupisanje podataka i koja je razlika između WHERE i HAVING klauze?',
        'ground_truth': 'Grupisanje se vrši pomoću GROUP BY klauze, koja grupiše redove sa istim vrednostima u određenim kolonama, a zatim se primenjuju agregatne funkcije (COUNT, AVG, SUM, MIN, MAX). Primer: SELECT grad, COUNT(*) AS broj_studenata, AVG(godine) AS prosecne_godine FROM studenti GROUP BY grad. WHERE filtrira redove PRE grupisanja - koristi se za uslove nad pojedinačnim redovima. HAVING filtrira grupe POSLE grupisanja - koristi se za uslove nad agregatnim vrednostima. Primer: SELECT grad, COUNT(*) AS broj_studenata FROM studenti WHERE godine > 18 GROUP BY grad HAVING COUNT(*) > 100.'
    },
    # Metadata: sql_for_ds.txt -> "GROUP BY - Grupisanje podataka"
    
    {
        'question': 'Šta su Window Functions u SQL-u i kako se koriste? Navedi primere sa ROW_NUMBER, RANK i LAG.',
        'ground_truth': 'Window Functions izvršavaju izračunavanja na skupu redova koji su povezani sa trenutnim redom, ali ne grupišu redove u jedan izlazni red (za razliku od GROUP BY). One čuvaju sve redove i dodaju nove kolone sa izračunatim vrednostima. ROW_NUMBER dodeljuje jedinstveni redni broj: SELECT ime, godine, ROW_NUMBER() OVER (ORDER BY godine DESC) AS rang FROM studenti. RANK dodeljuje rang sa preskakanjem za iste vrednosti (1,2,2,4...): SELECT ime, godine, RANK() OVER (ORDER BY godine DESC) AS rank FROM studenti. LAG pristupa prethodnoj vrednosti: SELECT datum, prodaja, LAG(prodaja, 1) OVER (ORDER BY datum) AS prodaja_prethodni_dan FROM dnevna_prodaja. PARTITION BY omogućava grupisanje unutar window funkcije: SELECT grad, ime, godine, ROW_NUMBER() OVER (PARTITION BY grad ORDER BY godine DESC) AS rang_u_grad FROM studenti.'
    },
    # Metadata: sql_for_ds.txt -> "WINDOW FUNCTIONS"
    
    # ============================================================
    # STATISTIKA (statistics.txt)
    # ============================================================
    {
        'question': 'Objasni mere centralne tendencije i mere disperzije u statistici. Koje se koriste i zašto?',
        'ground_truth': 'Mere centralne tendencije pokazuju tipičnu vrednost u skupu podataka: Mean (sredina) - suma svih vrednosti / broj vrednosti, osetljiva na outlier-e; Median (medijana) - srednja vrednost kada se podaci sortiraju, robusna na outlier-e; Mod (modus) - vrednost koja se najčešće pojavljuje, korisna za kategoričke podatke. Mere disperzije pokazuju koliko su podaci rasuti: Range (opseg) - max - min, jednostavan ali neinformativan; Variance (varijansa) - prosečno kvadratno odstupanje od sredine, var = Σ(x - mean)² / (n-1); Standard Deviation - kvadratni koren varijanse, vraća se u originalne jedinice; IQR (Interkvartilni rang) - Q3 - Q1, robusan na outlier-e. Kada šta koristiti: Mean za simetrične distribucije bez outlier-a; Median za asimetrične distribucije ili podatke sa outlier-ima; Mod za kategoričke podatke.'
    },
    # Metadata: statistics.txt -> "1. MERE CENTRALNE TENDENCIJE" i "2. MERE DISPERZIJE"
    
    {
        'question': 'Šta je normalna distribucija i koje je njeno značenje u statistici? Objasni 68-95-99.7 pravilo.',
        'ground_truth': 'Normalna distribucija (Gausova kriva) je simetrična, zvonolika distribucija kod koje su mean = median = mod. Opisana je sa dva parametra: sredinom (μ) i standardnom devijacijom (σ). Karakteristike: simetrična oko sredine, mean = median = mod, oblik određen sa μ i σ. 68-95-99.7 pravilo (Empirijsko pravilo): 68% podataka se nalazi unutar ±1σ od sredine (μ ± σ); 95% podataka se nalazi unutar ±2σ od sredine (μ ± 2σ); 99.7% podataka se nalazi unutar ±3σ od sredine (μ ± 3σ). Značaj: osnova za mnoge statističke testove (t-test, ANOVA); Centralna granična teorema omogućava korišćenje normalne distribucije za zaključke o sredini; Z-score (standardizacija) omogućava poređenje vrednosti iz različitih distribucija.'
    },
    # Metadata: statistics.txt -> "4. NORMALNA DISTRIBUCIJA"
    
    # ============================================================
    # VIZUELIZACIJA (visualization_basics.txt)
    # ============================================================
    {
        'question': 'Koje su osnovne vrste vizuelizacija u Matplotlib-u i za šta se koriste? Navedi najvažnije tipove grafova.',
        'ground_truth': 'Matplotlib nudi različite vrste vizuelizacija: Line plot (linijski graf) - za vremenske serije i trendove, prikazuje promenu vrednosti kroz vreme: plt.plot(x, y). Scatter plot (tačkasti graf) - za odnose između dve numeričke varijable, prikazuje korelaciju: plt.scatter(x, y). Histogram - za distribuciju jedne numeričke varijable, prikazuje frekvenciju vrednosti u intervalima: plt.hist(data, bins=30). Bar chart (trakasti graf) - za kategoričke podatke, poređenje vrednosti između kategorija: plt.bar(categories, values). Box plot - za prikaz distribucije i detekciju outlier-a, prikazuje medijanu, kvartile i ekstremne vrednosti: plt.boxplot([data1, data2, data3]). Kombinovanje više grafova pomoću subplots(): fig, axes = plt.subplots(2, 2, figsize=(12, 10)); axes[0, 0].plot(x, y).'
    },
    # Metadata: visualization_basics.txt -> "MATPLOTLIB OSNOVE"
]

TEST_QUESTIONS_SUBSET = TEST_QUESTIONS[:3]