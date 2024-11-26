**Corso di laurea triennale in Lettere**

# Metodologie informatiche nelle discipline umanistiche

**Prof. Alfio Ferrara**

*Dipartimento di Informatica, Università degli Studi di Milano
Stanza 7012 via Celoria 18, 20133 Milano, Italia <a href="mailto:alfio.ferrara@unimi.it">alfio.ferrara@unimi.it</a>*



# Idee per i progetti finali



[TOC]

## Istruzioni

Il progetto finale è disponibile come prova sostitutiva della prova scritta d'esame solo per gli studenti frequentanti e solo dopo averne dato comunicazione al docente. La prova consiste nella preparazione di uno studio breve su uno degli argomenti trattati nel corso, identificando una precisa domanda di ricerca. 

Il progetto dovrà proporre una metodologia per risolvere la domanda di ricerca e prevedere una verifica sperimentale dei risultati ottenuti, secondo metriche di valutazione dei risultati. L'enfasi non è posta sulla realizzazione della soluzione, ma piuttosto sulla discussione critica dei metodi e degli eventuali risultati ottenuti, al fine di comprendere la potenziale efficacia della metodologia proposta.

I risultati devono essere documentati in un breve articolo di non meno di 4 pagine e non più di 8. Nel caso il progetto preveda la scrittura di software, gli studenti dovranno fornire l'accesso a un <a href="https://github.com/">repository GitHub</a> contenente il codice stesso e gli eventuali risultati sperimentali riproducibili.

Infine, il progetto sarà discusso dopo una presentazione di 10 minuti con diapositive. La prova d'esame consiste nella consegna del materiale, pertanto la discussione e presentazione può avvenire anche online previo appuntamento col docente.

Il criterio di valutazione terrà in conto dell'uso adeguato di strumenti concettuali visti a lezione nello svolgimento del progetto, dell'estinzione del lavoro, della originalità delle idee proposte, della coerenza e rigore metodologico sia nella realizzazione del progetto sia nella sua presentazione.

## Procedura

Per chi sceglie questa modalità d'esame, le date di appello sono indicative, servono solo per l'iscrizione al registro. La discussione col docente si svolge su appuntamento, secondo la seguente procedura:

1. Inscriversi a un qualsiasi appello
2. Contattare il Prof. Ferrara non appena:
   1. Il progetto è finito e pronto per la discussione 
   2. In una data successiva a quella di chiusura dell'appello a cui si è iscritti

3. Fissare un appuntamento e presentare il progetto

**Esempio**: siete iscritti alla data [Mese] [Giorno]. **In qualsiasi momento dopo [Mese] [Giorno]**, quando il **progetto è ultimato** contattate il Prof. Ferrara e concordate un appuntamento nel quale presentare e discutere il progetto.

## Strumenti utili

Il progetto può avvalersi di tutti gli strumenti, incluse le librerie Python, introdotti durante il corso o anche di strumenti individuati dagli studenti. Di seguito si riportano alcuni esempi di strumenti che possono risultare utili per vari scopi nel corso della preparazione del progetto.

#### Reperimento di dati e *dataset*

- Kaggle: https://www.kaggle.com/datasets
- Hugging Face: https://huggingface.co/docs/datasets/en/index
- Wikisource: https://it.wikisource.org/wiki/Pagina_principale
- Biblioteca Italiana: http://www.bibliotecaitaliana.it/

#### Manipolazione del testo e dei dati

- NLTK: https://www.nltk.org/
- SpaCy: https://spacy.io/
- Gensim: https://radimrehurek.com/gensim/ 
- Sentiment (TextBlob): https://textblob.readthedocs.io/en/dev/
- Scikit-learn: https://scikit-learn.org/stable/
- Modelli Hugging Face: https://huggingface.co/models 
- Qualsiasi AI generativa (ChatGPT, Claude, Mistral, etc.)

#### Visualizzazione dei dati

- Matplotlib: https://matplotlib.org/
- Seaborn: https://seaborn.pydata.org/
- Bokeh: https://bokeh.org/

## Idee di progetto

Di seguito sono presentate alcune idee per i progetti. Per ciascuna idea viene fornita una breve descrizione, e, quando necessario, un esempio di *dataset* utilizzabile. Le idee qui presentate sono volutamente generiche e non vanno intese come un esercizio ma piuttosto come una traccia a partire dalla quale sviluppare ulteriori idee e metodi. Gli studenti possono scegliere una delle seguenti idee come tema del proprio progetto oppure proporre una propria idea, strutturando la proposta in modo simile a quelle presentate in questo documento. In quest’ultimo caso, è sufficiente inviare la descrizione del progetto al Prof. Ferrara.

### Leggere a macchina

Partendo da uno o più testi letterari e da un insieme di temi, che possono essere specificati da parole-chiave, collezioniamo tutte le porzioni del testo (può trattarsi di frasi o interi paragrafi) in cui il tema viene trattato. Per ognuna di queste porzioni si procede poi a valutare un *sentiment*, ovvero una polarità positiva o negativa del testo nei confronti del tema trattato. Il progetto mira a eseguire questa analisi con strumenti diversi ti tipo tradizionale (per esempio TextBlog) e per mezzo di AI generativa. Lo scopo del progetto è comparare l'esito ottenuto da strumenti diversi e/o su testi diversi, definendo anche una rappresentazione grafica di questi dati che consenta di apprezzare tali differenze.

### Che parole usi?

Usando *Word2Vec*, il progetto mira a confrontare il lessico utilizzato da fonti testuali diverse. Tali fonti possono essere testi letterari, articoli di giornale, commenti degli utenti su piattaforme web, o in generale qualsiasi contenuto testuale. L'obiettivo principale è sviluppare un metodo e delle idee di visualizzazione che consentano di isolare le peculiarità lessicali di ciascun corpus testuale in rapporto con altri *corpora* testuali usando la rappresentazione vettoriale delle parole così come la otteniamo da *Word2Vec*.

### Superstar

Il progetto [Pantheon Project: Historical Popularity Index](https://www.kaggle.com/datasets/mit/pantheon-project) fornisce sui dati sulla popolarità di moltissimi personaggi storici basandosi sul numero di visite ricevute dalla corrispondente pagina di Wikipedia. L'obiettivo del progetto è la definizione di una strategia complessiva per utilizzare questi dati a scopi di analisi e visualizzazione, estraendo informazioni di interesse fra essi. Solo per fornire alcuni esempi: si potrebbe comparare fra loro i personaggi aggregandoli sulla base di diverse caratteristiche, provare a scoprire dei *trend* di gradimento, individuare una o più caratteristiche dei personaggi che sembrano essere correlate con le preferenze nei loro confronti, visualizzare mappe tematiche o persino organizzare tornei virtuali in cui i personaggi si scontrano e le loro chance di successo sono proporzionali alla loro popolarità. In una parola, ipotizzare utilizzi creativi per questi dati.

### Raccontami una storia

I due articoli riportati qui sotto affrontano da prospettive diverse il tema dell'uso di AI generativa per la produzione di opere creative. Il progetto mira a applicare alcune di queste idee alla generazione di componimenti letterari, poetici o in prosa, e sottoporli a analisi critica per individuare delle possibili caratteristiche tipiche dello strumento di AI prescelto nella composizione del testo.

*Jing, Y., Yang, Y., Feng, Z., Ye, J., Yu, Y., & Song, M. (2019). Neural style transfer: A review. IEEE transactions on visualization and computer graphics, 26(11), 3365-3385. [link](https://ieeexplore.ieee.org/abstract/document/8732370?casa_token=s0nJ3En9V38AAAAA:odRTMVGIXbKuBNt3ffciJJUsONDkJRrLlJIpA-MTeaJ5ahIkBZDmFXT7ZaDZ3yAt8RPrIiUI)*

*Chakrabarty, T., Laban, P., Agarwal, D., Muresan, S., & Wu, C. S. (2024, May). Art or artifice? large language models and the false promise of creativity. In Proceedings of the CHI Conference on Human Factors in Computing Systems (pp. 1-34). [link](https://dl.acm.org/doi/full/10.1145/3613904.3642731?casa_token=tx-zVbiLE5oAAAAA%3Ajrf6IBIGVw66tY2KihFg3ZVYcYquWZqgAuZlT_nCpDrbTiO0yAXa8E07ZTBLM4dfpoE9OfGuE3KV)*

### Sei sicuro?

L'AI generativa può produrre dati errati o a volte completamente inventati. Il progetto mira a verificare la credibilità e l'accuratezza delle informazioni fornite da uno strumento di AI generativa confrontandone le informazioni con i dati forniti da un *dataset* reale. Solo a titolo d'esempio, si potrebbe utilizzare il *dataset* [Pantheon Project: Historical Popularity Index](https://www.kaggle.com/datasets/mit/pantheon-project) come strumento di verifica dell'accuratezza dell'informazione proposta da uno o più strumenti di AI generativa in merito ai personaggi storici. Oppure ancora, verificare se i personaggi individuati dall'AI generativa per certi periodi storici o certe caratteristiche sono anche quelli più noti e popolari secondo il *dataset*. Altri esempi potrebbero riguardare l'accuratezza circa l'origine geografica dei prodotti alimentari, oppure le caratteristiche tecniche di strumenti elettronici, o la conoscenza letteraria, etc. Il progetto dovrebbe fornire indicatori statistici circa l'accuratezza e appropriati metodi di visualizzazione dei risultati ottenuti.

### Non ci sono più le mezze stagioni

L'AI generativa può essere esposta a pregiudizi e bias culturali di varia natura. Il progetto mira a realizzare un esperimento per indagare il fenomeno, chiedendo a uno o più strumenti di AI generativa di creare dei personaggi letterari fittizi sulla base di alcune caratteristiche che potrebbero ad esempio includere il luogo di ambientazione della presunta opera letteraria, il tema, il genere, l'età, professione e genere del personaggio in questione, il ruolo nell'opera etc. Dopo aver raccolto un numero sufficiente di dati, si procede poi a verificare se i personaggi prodotti rispondono a uno o più stereotipi fornendo una qualche evidenza statistica del fenomeno e una sua corrispondente modalità di visualizzazione.

### Latine loqui

L'articolo sotto riportato indaga la capacità di strumenti di AI generativa di produrre e tradurre testi latini. Il progetto mira a definire diversi esercizi da sottoporre a uno o più strumenti di AI generativa allo scopo di valutarne le qualità come scrittore e traduttore di testi latini. Il progetto può combinare un'analisi ti tipo più qualitativo dei prodotti dell'AI e strumenti di analisi di tipo più quantitativo-statistico.

*Jiao, W., Wang, W., Huang, J. T., Wang, X., & Tu, Z. (2023). Is ChatGPT a good translator? A preliminary study. arXiv preprint arXiv:2301.08745, 1(10). [link](https://wxjiao.github.io/downloads/tech_chatgpt_arxiv.pdf)*
