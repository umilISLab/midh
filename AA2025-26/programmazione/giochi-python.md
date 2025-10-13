#### Metodologie Informatiche nelle discipline umanistiche - Prof. Alfio Ferrara

# Giochi Python

## Prima lezione (dispensa descrittiva)

Questa dispensa raccoglie 12 giochi semplici che possono essere sviluppati in Python nella primissima fase di apprendimento.  Ogni gioco è accompagnato da una descrizione testuale del suo funzionamento.

---

## 1) Morra cinese (sasso–carta–forbici)  
Un classico gioco a due: il giocatore sceglie fra “sasso”, “carta” o “forbici”, il computer fa una scelta casuale.  
Si confrontano le due mosse secondo le regole note: sasso rompe forbici, forbici tagliano carta, carta avvolge sasso.  
L’esito può essere vittoria, sconfitta o pareggio.

---

## 2) Dadi: il più alto vince  
Il giocatore e il computer lanciano un dado ciascuno, per un certo numero di round (ad esempio tre).  
A ogni round chi ottiene il numero più alto guadagna un punto. Alla fine si dichiara il vincitore in base al punteggio.

---

## 3) Impiccato-lite (Hangman)  
Viene scelta una parola segreta.  
Il giocatore prova a indovinare una lettera alla volta: se la lettera è presente, compare al posto giusto; altrimenti si perde una “vita”.  
Il gioco termina con la parola indovinata (vittoria) o con l’esaurimento delle vite (sconfitta).

---

## 4) Anagrammi (Word scramble)  
Una parola viene mescolata nelle sue lettere e presentata al giocatore.  
L’obiettivo è ricostruire la parola originale indovinando la disposizione corretta.

---

## 5) Timer di riflessi  
Dopo un’attesa casuale, appare il segnale “VIA”.  
Il giocatore deve premere un tasto il più velocemente possibile.  
Si misura il tempo trascorso tra il segnale e la risposta, fornendo così un “tempo di reazione”.

---

## 6) Simon Says (sequenza colori)  
Il computer costruisce una sequenza crescente di colori (per esempio: rosso, verde, blu).  
A ogni turno viene mostrata la sequenza e il giocatore deve ripeterla.  
Se il giocatore sbaglia, la partita termina e viene indicato il livello massimo raggiunto.

---

## 7) Labirinto testuale 3×3  
Un cursore si trova all’inizio di una griglia 3×3 (posizione iniziale in alto a sinistra).  
Il giocatore può muoversi con comandi testuali (w/a/s/d = su/sinistra/giù/destra) fino a raggiungere l’uscita (in basso a destra).  
Se tenta di superare i bordi della griglia, il movimento non è valido.

---

## 8) Battaglia navale 1D  
Una griglia lineare di 10 celle nasconde una nave in una posizione casuale.  
Il giocatore ha un numero limitato di colpi per indovinare la cella corretta.  
Dopo ogni tentativo, si aggiorna la griglia con un segno di colpo mancato o di affondamento.

---

## 9) Tris (Tic-tac-toe) vs PC casuale  
Il classico gioco del tris su una griglia 3×3.  
Il giocatore usa il simbolo “X”, il computer “O”, scegliendo le mosse in modo casuale.  
Vince chi completa una riga, colonna o diagonale; in caso contrario si ha un pareggio.

---

## 10) Blackjack-lite (semplificato)  
Giocatore e banco ricevono due carte da un mazzo semplificato.  
Le figure valgono 10, l’asso può valere 1 o 11.  
Il giocatore può chiedere altre carte per avvicinarsi a 21 punti senza superarlo.  
Il banco prende carte finché non raggiunge almeno 17. Vince chi è più vicino a 21 senza sballare.

---

## 11) Memory 2×4 (trova le coppie)  
Otto carte disposte in fila (due per ciascuna delle lettere A–D).  
All’inizio sono coperte.  
A ogni turno il giocatore sceglie due posizioni: se le carte corrispondono, rimangono scoperte; altrimenti si ricoprono.  
L’obiettivo è trovare tutte le coppie.

---

## 12) Bingo 5×5  
Si genera una cartella 5×5 con numeri unici da 1 a 75.  
Vengono estratti numeri casuali, e quelli presenti sulla cartella vengono marcati.  
Il gioco termina quando il giocatore completa una riga, colonna o diagonale di numeri marcati.

---
