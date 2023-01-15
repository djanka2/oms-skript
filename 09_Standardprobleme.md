# Einige Standardprobleme

## Packprobleme

### Das Rucksackproblem
Das *Rucksackproblem* modelliert Objekte mit Gewicht und Wert. Für ein gegebenes maximales Gesamtgewicht soll eine Auswahl von möglichst großem Wert gefunden werden.

````{prf:definition} Rucksackproblem
Instanz
: Gegeben sind $n$ Objekte mit Werten $v_i$ und Gewichten $w_i$ für $i=1, \ldots, n$ sowie ein maximales Gesamtgewicht $W$.

Aufgabe
: Gesucht ist eine Teilmenge der Objekte mit möglichst großem Gesamtwert, deren Gesamt\-gewicht kleiner oder gleich $W$ ist.
````

Anschaulich kann man sich das Rucksackproblem wie folgt vorstellen.
````{prf:example}
TO DO
````

Als Formulierung durch ein (binäres) Lineares Programm ergibt sich.
````{prf:example}
TO DO
````

#### Eine alternative Lösung

Möglich sind auch Instanzen, bei denen der gleiche Objekttyp (festgelegt durch die Kombination von Wert und Gewicht) mehrfach vorkommt. Unter bestimmten Umständen kann dann auch eine Formulierung als ganzzahliges lineares Programm nützlich sein.
````{prf:example}
TO DO
````


### Bin Packing
Das *Bin Packing-Problem* betrachtet eine Menge an Objekten mit zugehörigen Gewichten. Außerdem sind beliebig viele Behälter mit einer vorgegeben Kapazität vorhanden. Ziel ist, die Objekte so in Behälter zu packen, dass die Kapazitätseinschränkung für jeden Behälter eingehalten wird und insgesamt möglichst wenige Behälter gebraucht werden.

````{prf:definition} Bin Packing Problem 
Instanz
: Gegeben ist eine Menge $U=\{1, 2, \ldots, n\}$ mit Gewichten $w_i$ für $i\in U$ sowie eine (Behälter-)Kapazität $B$.

Aufgabe
: Gesucht ist eine Aufteilung $U=U_1 \cup U_2 \cup \ldots \cup U_k$ in $k$ disjunkte Mengen, so dass die Summe der Elemente in jedem $U_i$ kleiner als $B$ ist und $k$ minimal wird.
````

Für die Modellierung benötigen wir zuerst eine obere Schranke $\overline k$ für die Anzahl der benötigten Behälter. 
Die Anzahl $n$ der Objekte ist offensichtlich eine solche obere Schranke.
Kleinere Werte für $\overline k$ (wir sagen dazu: schärfere obere Schranken) sind nützlich, da sie zu kleineren Modellen führen.
Man kann das Problem wie folgt modellieren.
````{prf:example}
TO DO
````

## Mengenprobleme

### Einführung: Ein einfaches Standortproblem 
Ein Telekommunikationsunternehmen will ein neues Wohngebiet mit Breitband-Internet versorgen. 
Dazu müssen Versorgungsstationen aufgestellt werden.
Das Wohngebiet ist in Häuserblocks $S=\{1, 2, \ldots, s\}$ unterteilt. 
Es gibt $v$ mögliche Positionen $V=\{1, 2, \ldots, v\}$ für die Versorgungsstationen.
Jede Versorgungsstation darf höchstens 200 Meter von den zu versorgenden Häuserblocks entfernt sein. Für jede mögliche Position $i$ sind die Kosten $w_i$ gegeben, eine Versorgungsstation an Position $i$ zu bauen.
Gesucht ist eine kostenoptimale Auswahl an Versorgungsstationen, die alle Blocks versorgt.

````{prf:example}
TO DO
````

Als ILP ergibt sich:

````{prf:example}
TO DO
````

Ist zusätzlich noch einen Teilnehmeranzahl $t_i$ für jeden Block und eine Kapazität $k_i$ für jede Versorgungsposition gegeben, so ergibt sich folgende zusätzliche Nebenbedingung:

````{prf:example}
TO DO
````


### Überdeckungensprobleme auf Mengen

Im Englischen heißt das Überdeckungsproblem auf Mengen *minimum set cover*. Gegeben ist eine Grundmenge $S$ sowie ein Mengensystem $C \subseteq 2^S$. Dabei bezeichnet $2^S$ die Potenmenge von $S$, also die Menge $2^S=\{S' \mid S' \subseteq S \}$ aller möglichen Teilmengen von $S$. 
%Die *Kardinalität* einer Menge ist die Anzahl ihrer Elemente. 
Im gewichteten Fall ist jeweils ein Gewicht $w_c$ für jedes Element aus $C$ gegeben.
\Karos{33}{9}
Das *(ungewichtetet) Überdeckungsproblem* sucht eine Menge von möglichst wenigen Elementen $\{C_1, C_2, \ldots, C_l\} \subseteq C$, die $S$ überdecken, für die also jedes Element aus $S$ in mindestens einer Menge $C_i$ enthalten ist.
\Karos{33}{5}
Die *gewichtete* Variante sucht nicht nach möglichst wenigen Mengen sondern nach einer Lösung mit einem möglichst kleinem Gesamtgewicht:
\Karos{33}{6}

Es ergibt sich folgende formale Definition.
````{prf:definition} Gewichtetes Überdeckungsproblem
Instanz
: Gegeben ist eine endliche Menge $S=\{1, 2, \ldots, |S|\}$, ein Mengensystem $C=\{C_1, C_2, \ldots, C_{|C|}\} \subseteq 2^S$ sowie Gewichte $w_c$ für jedes $c \in C$.

Aufgabe
: Gesucht ist eine Teilmenge $C'= \{C_1, C_2, \ldots, C_l\} \subseteq C$, so dass $S=C_1 \cup C_2 \cup \ldots \cup C_l$ und das  Gesamtgewicht $\sum_{c \in C'}w_c$ minimal ist.
````
Das ungewichtete Überdeckungsproblem kann als Spezialfall des gewichteten Problems angesehen werden, bei dem alle Gewichte $1$ sind.


Um das Problem als binäres Programm zu modellieren, müssen wir die Eingabedaten, also vor allem die Mengen $S$ und $C$, in eine passende Form bringen. Wir konstruieren dafür die sogenannte *Inzidenzmatrix* $A \in \BB^{|S|\times |C|}$ für $C$. Zeilen der Matrix repräsentieren Elemente aus $S$. Spalten repräsentieren Mengen aus $C$. Ein Matrixelement $a_{ij}$ hat den Wert $1$ genau dann, wenn das zugehörige Element in der entsprechenden Menge enthalten ist. Ansonsten besitzt das Element den Wert $0$. Es ist also

\begin{align*}a_{ij}=\begin{cases}
1 & ,i \in C_j \\
0 & , \text{sonst }
\end{cases}
\end{align*}

Wir betrachten wieder das vorherige ungewichtete Beispiel.
````{prf:example}
TO DO
````
Es ergibt sich folgende Inzidenzmatrix:
````{prf:example}
TO DO
````
Das zugehörige binäre Programm löst unsere Instanz:
````{prf:example}
TO DO
````
Allgemein ergibt sich für das gewichtete Überdeckungsproblem das binäre Programm
````{prf:example}
TO DO
````

### Packungsprobleme auf Mengen
Im Englischen heißt das Packungsproblem auf Mengen *set packing*.
Gegeben ist eine Grundmenge $S$ sowie ein Mengensystem $C \subseteq 2^S$. 
Im gewichteten Fall ist jeweils ein Gewicht $w_c$ für jedes Menge aus $C$ gegeben. Zwei Mengen heißen disjunkt, falls sie kein Element gemeinsam besitzen.
````{prf:example}
TO DO
````
Gesucht ist eine Teilmenge $C'=\{C_1, C_2, \ldots, C_l\}$ von paarweise disjunkten Mengen mit maximalem Gesamtgewicht.
````{prf:example}
TO DO
````
In der *ungewichteten* Variante besitzen alle Elemente das Gewicht $1$.
Es ergibt sich folgende formale Definition.
````{prf:definition} Packungsproblem
Instanz
: Gegeben ist eine endliche Menge $S=\{1, 2, \ldots, |S|\}$, ein Mengensystem $C=\{C_1, C_2, \ldots, C_{|C|}\} \subseteq 2^S$ sowie Gewichte $w_c$ für jedes $c \in C$.

Aufgabe
: Gesucht ist eine Teilmenge $C'= \{C_1, C_2, \ldots, C_l\} \subseteq C$, so dass $C_i \cap C_j = \emptyset$ für $C_i, C_j \in C'$ und $C_i \not=C_j$ und so dass das  Gesamtgewicht $\sum_{c \in C'}w_c$ maximal ist.
````
Mit der Definition der Adjazenzmatrix aus dem letzten Abschnitt ergibt sich folgendes binäre Programm zur Lösung des Problems:
````{prf:example}
TO DO
````

### Zerlegungsprobleme auf Mengen
Im Englischen heißt das Zerlegungsproblem *set partitioning*. Gegeben ist eine Grundmenge $S$ sowie ein Mengensystem $C \subseteq 2^S$. Im gewichteten Fall ist jeweils ein Gewicht $w_c$ für jedes Menge aus $C$ gegeben. 
````{prf:example}
TO DO
````
Gesucht ist eine Überdeckung von $S$ durch disjunkte Mengen aus $C$.
````{prf:example}
TO DO
````
In der *ungewichteten* Variante besitzen alle Elemente das Gewicht $1$.
Es ergibt sich folgende formale Definition.
````{prf:definition} Zerlegungsproblem
Instanz
: Gegeben ist eine endliche Menge $S=\{1, 2, \ldots, |S|\}$, ein Mengensystem $C=\{C_1, C_2, \ldots, C_{|C|}\} \subseteq 2^S$ sowie Gewichte $w_c$ für jedes $c \in C$.

Aufgabe
: Gesucht ist eine Teilmenge $C'= \{C_1, C_2, \ldots, C_l\} \subseteq C$, so dass $C_i \cap C_j = \emptyset$ für $C_i, C_j \in C'$ und $C_i \not=C_j$, sowie $S=C_1 \cup C_2 \cup \ldots \cup C_l$  und das  Gesamtgewicht $\sum_{c \in C'}w_c$ maximal ist.
````
Mit der Definition der Adjazenzmatrix aus dem letzten Abschnitt ergibt sich folgendes binäre Programm zur Lösung des Problems:
````{prf:example}
TO DO
````

## Rundreiseprobleme

(subsubsec:TSP)=
### Das Problem des Handelsreisenden

Das Problem des Handelsreisenden heißt im Englischen *traveling salesman problem* oder *traveling salesperson problem*.

Gegeben sind $n$ Orte zusammen mit einer Entfernungs- oder Kostenmatrix $C$, die die paarweise Distanz zwischen den jeweiligen Orten angibt. Alle Entfernungen sind nicht-negativ. Ein Handlungsreisender möchte alle $n$ Orte besuchen und danach wieder zu seinem Startort zurückkehren. Dies bezeichnet man als *geschlossene Rundreise*. 
Gesucht ist eine geschlossene Rundreise von minimaler Gesamtstrecke unter allen geschlossenen Rundreisen.

````{prf:example}
TO DO
````

Eine Permutation $\pi_1, \pi_2, \ldots, \pi_n$ der Zahlen $\{1, 2, \ldots, n\}$ ist eine Umsortierung von $\{1, 2, \ldots, n\}$.[^fn:perm] 

[^fn:perm]: Formal definiert ist eine Permutation von $\{1, 2, \ldots, n\}$ eine umkehrbare Abbildung von $\{1, 2, \ldots, n\}$ auf $\{1, 2, \ldots, n\}$. 

````{prf:example}
TO DO
````

Wir suchen also eine bestimmte Permutation der Orte. 

````{prf:definition} Problem des Handlungsreisenden
Instanz
: Eine Menge $C=\{1, 2, \ldots, n\}$ aus $n$ Orten und eine Distanzfunktion $d(c_i,c_j) \in \RR^+$ auf $C$.

Aufgabe
: Gesucht ist eine kürzeste Rundreise auf $C$, d.h. eine Permutation $\pi_1, \pi_2, \ldots, \pi_n$ von $C$, so dass 

\begin{align*}\left(\sum_{i=1}^{n-1} d(\pi_i,\pi_{i+1}) \right) + d(\pi_n,\pi_1) \end{align*}

minimal ist.  
````

Wir betrachten folgende Probleminstanz
````{prf:example}
TO DO
````
Wir setzen für unsere Modellierung die Entscheidungsvariablen 
````{prf:example}
TO DO
````
ein. 
%Um sicherzustellen, dass jeder Ort genau einmal besucht wird, können wir folgende Nebenbedingungen nutzen.
%\Karos{33}{9}
Als erstes (unvollständiges!) Modell ergibt sich
````{prf:example}
TO DO
````

Wir erkennen, dass die Problemformulierung noch nicht vollständig ist. Es können sich sogenannte *Subtouren* bilden:
````{prf:example}
TO DO
````
Wie verhindern wir Subtouren? Es gibt zwei verschieden Ansätze. 

#### Das Modell nach Dantzig, Fulkerson und Johnson
Das Modell setzt folgende Nebenbedingungen zur Elimination von Subtouren ein:

\begin{align*}\sum_{i \in C'} \sum_{j \in C'}x_{ij} \leq |C'|-1 \hspace{1cm} \forall C' \subset \{2, \ldots, n\}, \hspace{0.3cm} |C'| \geq 2 \end{align*}

````{prf:example}
TO DO
````
Es wird also für jede mögliche Teilmenge $C'$ an Städten sichergestellt, dass "ein Weg in $C'$ führt". Der Ort $1$ wird als Startort der Reise angesehen und benötigt keine Nebenbedingung, da $C'= \{2, \ldots, n\}$ sicherstellt, dass $1$ in der Tour enthalten ist. Insgesamt ergibt sich das folgende Modell:
````{prf:example}
TO DO
````
Es gibt sehr viele Teilmengen von $C$. Damit besitzt dieses Modell sehr viele Nebenbedingungen, wenn die Anzahl der Städte groß ist.

#### Das Modell nach Miller, Tucker und Zemlin
Das Modell setzt zusätzliche reellwertige Variablen $u_i$ ein, die die Orte in der Reihenfolge der Tour durchnummerieren:
%\begin{align*}u_i - u_j + nx_{ij} \leq n-1 \hspace{1cm} i,j \in \{2, \ldots, n\} \hspace{0.3cm} i \not=j \end{align*}
\begin{alignat*}{8}
u_i - u_j + nx_{ij} & \leq &&  \ n-1  \hspace{1cm} && i,j \in \{2, \ldots, n\} \hspace{0.3cm} i \not=j \\
u_1 & = && \ 1 \\
2 \leq u_i & \leq && \ n && i \in \{2, \ldots, n\}
\end{alignat*}
Um die erste Nebenbedingung zu analysieren, machen wir eine Fallunterscheidung nach dem Wert von $x_{ij}$:
````{prf:example}
TO DO
````
Es muss also $u_j$ um mindestens $1$ größer als $u_i$ sein, falls die Route $i-j$ in der Rundreise benutzt wird.

````{prf:example}
TO DO
````
Das Abzählen der Orte verhindert Subtouren. Beispielsweise würde sich im Falle einer Subtour $i-j-k-i$ die Ungleichungskette
````{prf:example}
TO DO
````
ergeben. 

#### Vergleich beider Modelle
Welches Modell ist besser? Das kann von der konreten Instanz abhängen. Wir lernen in den späteren Kapiteln einige Kriterien, um Modelle miteinander vergleichen zu können. Das erste Modell grenzt den Suchraum sehr gut ein, wir sagen es hat eine engere Relaxierung als das zweite Modell. Der Nachteil des ersten Modells ist die sehr große Anzahl an Nebenbedinungen.

### Tourenplanungsprobleme
Tourenplanungsprobleme heißen im Englischen *vehicle routing problems*.
Im Unterschied zum Problem des Handelsreisenden gibt es nicht nur einen Handelsreisenden, sondern $K$ verschiedene Fahrzeuge, die die $n$ Orte besuchen sollen. Wir gehen davon aus, dass alle Fahrzeuge im gleichen zentralen Lager starten. Eine Vorabaufteilung welches Fahrzeug welchen Kunden bedient gibt es nicht. Wir verzichten in diesem Abschnitt auf eine formale Problemdefinition. 

````{prf:example}
TO DO
````

Wir können dieses Problem durch das folgende gemischt-ganzzahlige Programm modellieren.

````{prf:example}
TO DO
````

#### Tourenplanungprobleme in der Praxis
Tourenplanungsprobleme sind eine äußert praxisrelevante Problemklasse. Anwendungen finden sich etwa im Bereich Lieferdienste oder Kundenservice. Über das oben beschriebene Grundproblem hinaus gibt es eine große Vielzahl an Modellierungsaspekten, die in der Praxis auftauchen. Beispiele sind etwa Kapazitätsbeschränkungen für  Fahrzeuge, Zeitfenster für  Kundenbesuche, uhrzeitabhängige Fahrzeiten, oder Restriktionen durch die Fahrt- und Ruhezeitenverordnung. Wegen der hohen Komplexität werden in der Praxis statt gemischt-ganzzahligen Programmen häufig auch heuristische Verfahren eingesetzt.
