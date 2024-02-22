# Ganzzahlige Probleme

## Ganzzahligkeitsbedingungen und weitere Modellarten

In vielen Problemstellungen dürfen manche oder alle Entscheidungsvariablen nicht beliebige reelle Werte, sondern nur einen eingeschränkten Wertebereich, etwa den der ganzen Zahlen annehmen. Beispiele sind etwa der Kauf eines Investitionsgutes oder das An- und Ausschalten einer Maschine. Man unterscheidet unter anderem die folgende Problemarten, die wir der Einfachheit halber nur in Standardform darstellen.

Lineare Programme 
: Die Entscheidungsvariablen dürfen beliebige reelle Werte annehmen.

````{prf:example}
TO DO
````

Ganzzahlige lineare Programme
: Alle Entscheidungsvariablen dürfen nur ganzzahlige Werte annehmen.

````{prf:example}
TO DO
````


Binäre lineare Programme
: Alle Entscheidungsvariablen dürfen nur die Werte $0$ und $1$ annehmen.

````{prf:example}
TO DO
````

Gemischt-ganzzahlige lineare Programme
: Manche Entscheidungsvariablen dürfen nur ganzzahlige Werte annehmen.

````{prf:example}
TO DO
````


## Relaxierung von Problemen mit Ganzzahligkeitsbedingungen

Für alle Problemtypen, die Ganzzahligkeitsbedingungen enthalten, bezeichnet das zugehörige *relaxierte Problem* das Problem, bei dem die Ganzzahligkeitsbedingungen entfernt wurden. Für jede Binärvariable $x_i$ fordern wir im zugehörigen relaxierten Problem zusätzlich, dass $0 \leq x_i \leq 1$ gilt.
````{prf:example}
TO DO
````

An folgenden Beispiel sehen wir den Zusammenhang der Lösungsräume zwischen einem ganzzahligen linearen Problem und seiner relaxierten Version:
````{prf:example}
TO DO
````

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

## Zuordnungsprobleme

## Mengenprobleme (Facility Location)

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


## Ablaufplanung
Ablaufplanung wird im Englischen *scheduling* genannt. 
Es gibt sehr viele verschiedene Probleme der Ablaufplanung. Eine Übersicht über akademische Arbeiten findet sich etwa in 
*Michael L. Pinedo: Scheduling. Theory, Algorithms and Systems, Springer, 2016*.

Allen Problemvarianten gemeinsam ist, dass es um die *Zuteilung von Resourcen zu Aufgaben über die Zeit* geht, sowie um das *Erstellen eines zugehörigen Zeitplans*. Wir betrachten zuerst ein Beispiel aus der Produktion:

````{prf:example}
Farbe wird in drei Schritten produziert: Zuerst werden die Rohmaterialien gemahlen, dann wird gemixt und am Ende verpackt. Wir erstellen den Produktionsplan für eine Fabrik, die weiße und blaue Farbe produzieren kann. Der Mixer muss 10 Minuten gesäubert werden, wenn von blauer auf weißer Farbe gewechselt wird. In umgekehrter Reihenfolge muss nicht gesäubert werden. Wir besitzen zwei Mühlen (eine langsame und eine schnelle), einen Mixer sowie eine Packstation. Alle Maschinen können Batches zu je 1000 Litern bewältigen. Unsere Aufgabe ist, 2000 Liter weiße Farbe und 2000 Liter blaue Farbe zu produzieren.
````

Ein Produktionsplan wird typischerweise über ein *Gantt-Chart* visualisiert:

````{prf:example}
TO DO
````

In der Produktionsplanung sind häufig für die einzelnen Aufgaben zusätzlich individuelle, gewünschte Fertigstellungszeitpunkte gegeben.
Typische Zielfunktionen sind die Minimierung einer der folgenden Terme
- Die Summe der Fertigstellungszeitpunkte aller Aufgaben (engl: total completion time). 
- Der Fertigstellungszeitpunkt der letzten Aufgabe(n) (engl: makespan)
- Die Anzahl der zu spät fertiggestellten Aufgaben (engl: total number of tardy/late jobs)
- Die längste Verzögerung für eine Aufgabe (engl: maximum lateness).
In Realweltproblemen gibt es typischerweise eine hohe Anzahl an zusätzlichen Arten von Nebenbedingungen die in ihrer Kombination meistens sehr individuell auf ein spezifisches Problem angepasst sind.

Bei der Modellierung von Ablaufplanungsproblemen durch gemischt-ganzzahlige Programme gibt es zwei grundsätzliche Modelltypen: *zeitdiskretisierte Modelle* sowie *zeitkontinuierliche Modelle*. Zeitdiskretisierte Modelle haben wir im letzten Kapitel kennengelernt. Im folgenden werden wir ein zeitkontinuierliches Modell für ein einfaches Problem aus der Projektplanung entwickeln.


### Ein einfaches zeitkontinuierliches Modell

Ein Projektleiter erstellt einen Zeitplan für sein Projekt. Er nutzt dafür folgende Informationen.  
- Eine Menge an Aufgaben $A=\{1, 2, \ldots, n\}$.
- Für jede Aufgabe $i$ ist ihre Dauer $d_i$ gegeben. $D=\{d_1, d_2, \ldots, d_n\}$
- Es ist eine Menge $L=\{(p_1,s_1), \ldots, (p_n,s_n)\} \subset A\times A$ von Abhängigkeiten gegeben mit der Bedeutung: Aufgabe $p_i$ muss abgeschlossen sein, bevor Aufgabe $s_i$ starten kann.
- Es ist eine Menge $B=\{(a_1,b_1), \ldots, (a_n,b_n)\} \subset A\times A$ von Blockierungen gegeben mit der Bedeutung: Aufgabe $a_i$ und $b_i$ können nicht zeitgleich ausgeführt werden.	

Gesucht ist
- die Startzeit $x_i$ für jede Aufgabe $i \in A$, so dass das Projekt möglichst schnell abgeschlossen ist (d.h. alle Aufgaben sind beendet).

Wir betrachten die Beispielinstanz $A=\{1, 2, \ldots, 6\}$ und $L=\{(1,4),(2,4),(3,6), (4,5),(4,6)\}$ und $D=(1,2,1,2,2,1)$ und $B=\{(1,2),(2,3),(1,3)\}$.

````{prf:example}
TO DO
````

Es ergibt sich als Modell für diese Instanz:

````{prf:example}
TO DO
````

Es ergibt sich als allgemeines Modell für diese Problemklasse
\begin{alignat*}{5}
\min & \quad  &   y &          & & \\[4mm]
\text{s.t. } & & x_i + d_i  & \leq   \ y & \quad\quad & & \forall i \in A \\
& & x_i + d_i  & \leq   \ x_j & \quad\quad & & \forall (i,j) \in L \\[4mm]
& & x_i + d_i  & \leq   \ x_j + (1-h_{ij})d_{max} & \quad\quad & & \forall (i,j) \in B \\
& & x_j + d_j  & \leq   \ x_i + h_{ij}d_{max} & \quad\quad & & \forall (i,j) \in B \\[4mm]
& & x_i & \geq  \ 0 & && \forall i \in A \\
& & h_{ij} & \in \ \BB & && \forall (i,j) \in B
\end{alignat*}

mit den Entscheidungsvariablen
- $y$: Endzeitpunkt der letzten Aufgabe
- $x_i$: Startzeitpunkt von Aufgabe $i$
- $h_{ij}=\begin{cases} 1 &\text{ , wenn Aufgabe }i\text{ vor Aufgabe }j\text{ ausgeführt wird}\\ 0 & \text{, sonst}. \end{cases}$ 

und dem Wert
\begin{align*}
d_{max}=\sum_{i \in A}d_i.
\end{align*}

## Modellierungstricks II

Viele Echtweltprobleme zeichnen sich durch eine große Anzahl an zu modellierenden Aspekten aus.
Die Standardprobleme aus dem letzten Kapitel bilden bereits einen kleinen Fundus an Bausteinen für die Modellierung. 
Im Folgenden werden einige wiederkehrende Aspekte zusammen mit einer möglichen Lösung präsentiert.



### Logische Bedingungen an Variablen

(subsubsec:logikBeispiel)=
#### Einführendes Beispiel
Viele Echtweltprobleme beinhalten in einer Form auch logische Zusammenhänge. Wir betrachten ein Beispiel aus der Produktion.

````{prf:example}
1. Es gibt $5$ Maschinen $A,B,C,D, E$, die jeweils ein- oder ausgeschaltet sein können.
2. Ist  $A$ eingeschaltet, so darf $B$ nicht eingeschaltet sein. 
3. Ist  $D$ eingeschaltet, so ist immer auch mindestens  $B$ oder  $C$ eingeschaltet.
4. Ist  $D$ ausgeschaltet, so sind immer auch  $B$ und  $C$ ausgeschaltet.
5. Es ist immer genau eine der beiden Maschinen $D$ und $E$ eingeschaltet.
````

Wir übersetzen dies in einen logischen Ausdruck mit den logischen Variablen $A,B,C,D,E$, die die Werte *wahr* und *falsch* annehmen können.

````{prf:example}
TO DO
````


#### Exkurs: Crash-Kurs Logik
Wir wiederholen einige wichtige Ergebnisse aus der Logik. 
Eine aussagenlogische Variable kann die Werte *wahr* oder *falsch* annehmen. 
Wir schreiben dafür kurz auch $1$ (wahr) und $0$ (falsch).

Aussagenlogische Variablen können durch sogenannte *Junktoren miteinander verknüpft werden. Die wichtigsten Junktoren sind 
- Konjunktion (UND-Verknüpfung), Symbol: $\land$
- Disjunktion (ODER-Verknüpfung), Symbol: $\lor$	
- Negation (Verneinung), Symbol: $\lnot$	
- Implikation (logischer Schluss), Symbol: $\Rightarrow$	
- Äquivalenz (Gleichheit), Symbol: $\Leftrightarrow$	
- Exklusiv-Oder (Entweder-Oder), Symbol: $\dot\lor$	

Die Bedeutung der einzelnen Junktoren ergibt sich aus folgender **Wahrheitstabelle**

| $A$ | $B$ | $A \land B$ | $A\lor B$ | $\lnot A$ | $A \Rightarrow B$ | $A \Leftrightarrow B$ | $ A \dot\lor B$ | 
|--:|--:|------------:|----------:|----------:|------------------:|----------------------:|----------------:| 
| 0 | 0 | 0           | 0         | 1         | 1                 | 1                     | 0 |
| 0 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 
| 1 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 
| 1 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 

##### Darstellung durch Konjunktion, Disjunktion und Negation
Grundsätzlich muss man nicht mit allen Junktoren gleichzeitig arbeiten und kann sich auch auf bestimmte Teilmengen beschränken. So kann man etwa durch Konjunktion, Disjunktion und Negation alle anderen Junktoren ausdrücken:
- Implikation $A \Rightarrow B$ entspricht $\lnot A \lor B$.
- Äquivalenz $A \Leftrightarrow B$ entspricht $(A \Rightarrow B) \land (B \Rightarrow A)$. Dies entspricht 
	$(\lnot A \lor B) \land (\lnot B \lor A)$.
- Exklusiv-Oder $\dot\lor$ entspricht $A \Leftrightarrow \lnot B$. Dies entspricht 
		$(\lnot A \lor \lnot B) \land (A \lor B)$.

````{prf:example}
TO DO
````

##### Rechenregeln für aussagenlogische Formeln
Idempotenz 
: $ A \lor A = A$ 
: $A \land A = A$ 

Neutralität:
: $A \lor 0 = A $ 
: $A \land 1=A$ 

Negation
: $\lnot\lnot A = A$  
: $A \lor \lnot A = 1$ 
: $A \land \lnot A =0$ 

Kommutativität
: $A \land B = B \land A $ 
: $A \lor B = B \lor A $ 

Assoziativität
: $A \land (B \land C) = (A \land B) \land C$ 
: $A \lor (B \lor C) = (A \lor B) \lor C$ 

Distributivität
: $A \land (B \lor C) = (A \land B) \lor (A \land C)$ 
: $A \lor (B \land C) = (A \lor B) \land (A \lor C)$ 

De Morgansche Regeln
: $\lnot (A \land B) = \lnot A \lor \lnot B$  
: $\lnot (A \lor B) = \lnot A \land \lnot B$  	


##### Die Konjunktive Normalform

Ein *Literal* ist eine aussagenlogische Variable oder die Negation einer aussagenlogischen Variable. Beispiel: $A$ bzw $\lnot B$.
Eine *Klausel* ist eine Disjunktion vom Literalen. Beispiel: $(A \lor B \lor \lnot C)$.

Eine aussagenlogische Formel ist in *konjunktiver Normalform*, wenn Sie eine Konjunktion von Klauseln ist.
Beispiel: 
\begin{align*}
(A \lor B \lor \lnot C) \land (A \lor C \lor  D) \land (\lnot D \lor \lnot E \lor  F).
\end{align*} 

````{prf:example}
TO DO
````

#### Modellierung der Junktoren als arithmetische Ausdrücke
Logische Variablen werden durch Binärvariablen modelliert. Für jede logische Variable $V$ führen wir eine Binärvariable $x_V$ ein, mit der Bedeutung
\begin{align*}
x_V=\begin{cases}
1 & \text{,V ist *wahr*} \\
0 & \text{,V ist *falsch*}
\end{cases}
\end{align*} 
Die logischen Operationen Negation, Und, Oder, Implikation und Äquivalenz lassen sich wie folgt modellieren:

````{prf:example}
TO DO
````

Sind Literale $L_1, L_2, \ldots, L_n$ gegeben, so können wir die Situation "\{mindestens, genau, höchstens\} $k$ aus $n$ Literalen sind wahr" modellieren: 

````{prf:example}
TO DO
````

#### Transformation logischer Zusammenhänge in arithmetische Ausdrücke

Sind mehrere logische Formeln konjunktiv (also durch UND-Verknüpfungen) miteinander verbunden, so können die Formeln  einzeln behandelt werden.

````{prf:example}
TO DO
````
Sind umfangreichere Formeln gegeben, so können diese über die Rechenregeln für aussagenlogische Formeln in die Konjunktion von bekannten durch arithmetische Ausdrücke modellierbaren Formeln zurückgeführt werden. 
Wir wandeln das einführende Beispiel aus Abschnitt {ref}`subsubsec:logikBeispiel` um:

````{prf:example}
TO DO
````


##### Allgemeines Vorgehen
Die in der Praxis auftretenden Formeln sind typischerweise einfach genug, dass keine komplizierten Umformungen vorgenommen werden müssen. Als allgemeines Verfahren für sehr komplizierte Ausdrücke kann man folgendes Verfahren nutzen: Schritt 1: Umwandlung der Formel in konjunktive Normalform. Schritt 2: Behandlung der einzelnen Klauseln nach der Methode "mindestens $1$ aus $k$".


### Logische Bedingungen für Nebenbedingungen
In manchen Fällen sollen Nebenbedingungen nicht durchgehend gelten, sondern nur, wenn eine logische Variable wahr ist. Wir betrachten dazu ein Beispiel:

````{prf:example}
Ein Kraftwerk hat eine maximale Kapazität von 570 MW, sowie einen minimalen stabilen Produktionslevel von 290 MW. Ist das Kraftwerk ausgeschaltet, so produziert es 0 MW. Ist das Kraftwerk angeschaltet, so produziert es zwischen 290 und 570 MW.
````

Zur Modellierung benutzen wir folgende Entscheidungsvariablen
\begin{align*}
z=&\begin{cases}
	1 & \text{ Kraftwerk ist eingeschaltet}  \\
	0 & \text{ Kraftwerk ist ausgeschaltet}
	\end{cases}
p =& \text{Produktionslevel des Kraftwerks}
\end{align*}

Es gelten immer die Nebenbedingungen
\begin{align*}0 \leq p \leq 570 \end{align*}
Ist das Kraftwerk eingeschaltet, soll zusätzlich die Nebenbedingung
\begin{align*}290 \geq p \end{align*}
gelten. Falls das Kraftwerk ausgeschaltet ist, soll zusätzlich die Nebenbedingung
\begin{align*}p \leq 0 \end{align*}
gelten. Wie können wir dies modellieren?

````{prf:example}
TO DO
````

#### Allgemeines Vorgehen zu logischen Bedingungen für Nebenbedingungen
Wir betrachten nun den allgemeinen Fall, dass eine Nebenbedingung 
\begin{align*}a_{1}x_1 + a_{2}x_1 + \ldots + a_{n}x_n  \leq  b \end{align*}
nur abhängig von dem Wert einer binären Variable $v$ wirklich aktiv sein soll. Wir müssen dazu erst eine 
%untere Schranke $L$ sowie eine 
obere Schranke $U$ für den Wert
\begin{align*}a_{1}x_1 + a_{2}x_1 + \ldots + a_{n}x_n - b \end{align*}
bestimmen. Hierfür gibt es keine allgemeine Vorgehensweise. Die Möglichkeit der Berechnung solcher Schranken ist abhängig vom konkreten Modell. Es ergibt sich dann die Nebenbedingung
\begin{align*}
a_{1}x_1 + a_{2}x_1 + \ldots + a_{n}x_n - b \leq U (1-v)
\end{align*}
Für $v=1$ ergibt sich die ursprüngliche Bedingung. Für $v=0$ ist die neue Bedingung immer erfüllt.
Für den Fall 
\begin{align*}a_{1}x_1 + a_{2}x_1 + \ldots + a_{n}x_n  \geq  b \end{align*}
bestimmen wir eine untere Schranke $L$ für 
\begin{align*}a_{1}x_1 + a_{2}x_1 + \ldots + a_{n}x_n - b \end{align*}
und erhalten die Bedingung 
\begin{align*}
a_{1}x_1 + a_{2}x_1 + \ldots + a_{n}x_n - b \geq L (1-v).
\end{align*}
Nebenbedingung der Form
\begin{align*}a_{1}x_1 + a_{2}x_1 + \ldots + a_{n}x_n  = b \end{align*}
ersetzen wir durch eine $\leq-$ und eine $\geq-$Ungleichung und verfahren wie in den ersten beiden Fällen.

````{prf:example}
TO DO
````

### Endliche Wertemenge für Entscheidungsvariablen
Wir betrachten noch einen interessanten Spezialfall. Wir haben eine Nebenbedingung gegeben, für die nicht nur ein fester $b$-Wert sondern eine Menge von $b$-Werten möglich ist. Es soll also gelten
\begin{eqnarray*}
	a_{1}x_1 + a_{2}x_1 + \ldots + a_{n}x_n  & =  & b_1 \text{ oder} \\
	a_{1}x_1 + a_{2}x_1 + \ldots + a_{n}x_n  & =  & b_2 \text{ oder} \\
	\ldots \\
	a_{1}x_1 + a_{2}x_1 + \ldots + a_{n}x_n  & =  & b_k. 
\end{eqnarray*}
Wir können dies wie folgt modellieren: Wir führen neue Binärvariablen $z_1, z_2, \ldots, z_n$ ein, sowie die Nebenbedingungen
\begin{align*}
a_{1}x_1 + a_{2}x_1 + \ldots + a_{n}x_n   =   b_1z_1+b_2z_2+ \ldots + b_nz_n
\end{align*}
und
\begin{align*}
z_1 + z_2 + \ldots + z_n = 1. 
\end{align*} 
Dies löst unsere Aufgabenstellung.

````{prf:example}
TO DO
````


(subsec:disjunctiveProgramming)=
### Logische Bedingungen an Nebenbedingungen (Disjunktive Programmierung)

In manchen Anwendungen liegen mehrere Mengen von Nebenbedingungen vor, die durch eine logische Oder-Verknüpfung miteinander verbunden sind. Die Menge der zulässigen Lösungen kann also in der Form
\begin{align*}
\bigcup_{i=1\ldots k}\left\{x \mid A_ix \leq b_i, \ x \geq 0 \right\}
\end{align*} 
angegeben werden. Diese Darstellung kann sich etwa ergeben, wenn die Menge der zulässigen Lösungen nicht zusammen\-hängend oder nicht konvex ist.
````{prf:example}
TO DO
````
Man nutzt dafür folgende Schreibweise
````{prf:example}
TO DO
````

Für das weitere Vorgehen benötigen wir den Begriff des "großen M": In der Optimierung bezeichnet der Buchstabe $M$ typischerweise einen sehr großen Wert. Dabei ist nicht von Bedeutung wie groß der Wert von $M$ genau ist, solange er "groß genug" ist.

````{prf:example}
TO DO
````

\includegraphics[width=0.3\linewidth]{bilder/DisjunctiveProgramm_Instance.png}

#### Groß-M Reformulierung
Wir versuchen unser Beispiel mit Hilfe von zusätzlichen Binärvariablen $y_1$ und $y_2$ sowie einem großen $M$ zu formulieren:

````{prf:example}
TO DO
````

Wie groß muss $M$ dann mindestens sein?

````{prf:example}
TO DO
````
Allgemein ergibt sich als Groß-M Reformulierung

````{prf:definition} Groß-M Reformulierung
Gegeben ist ein Disjunktives Programm DP
\begin{align*}
\left[
\begin{array}{rcl}
& y_1 & \\
l_{11} & \leq x_1 \leq & u_{11} \\
l_{21} & \leq x_2 \leq & u_{21} \\
& \ldots & \\
l_{n1} & \leq x_n \leq & u_{n1} 
\end{array}
\right]
\vee
\ldots
\vee
\left[
\begin{array}{rcl}
& y_k & \\
l_{1k} & \leq x_1 \leq & u_{1k} \\
l_{2k} & \leq x_2 \leq & u_{2k} \\
& \ldots & \\
l_{nk} & \leq x_n \leq & u_{nk} 
\end{array}
\right]
\end{align*}
sowie ein $M_i$, so dass 
\begin{align*}x_i \in [-M_i+\min\{l_{ij} \mid k=1,\ldots, k\},\max\{u_{ij} \mid k=1,\ldots, k\}+M_i]\end{align*}
für alle $i=1\ldots n$ in jeder zulässigen Lösung $x$ gilt. 
Die *Groß-M Reformulierung* von DP ist

\begin{eqnarray*}
y_1 + y_2 + \ldots + y_k & = & 1 \\
y_1, y_2, \ldots, y_k & \in & \BB
\end{eqnarray*}


\begin{align*}
\begin{array}{rcl}
-M(1-y_1) + l_{11}  & \leq x_1 \leq & u_{11} + M(1-y_1) \\
-M(1-y_1) + l_{21}  & \leq x_2 \leq & u_{21} + M(1-y_1) \\
& \ldots & \\
-M(1-y_1) + l_{n1}  & \leq x_n \leq & u_{n1} + M(1-y_1) \\[8mm]
& \ldots & \\[8mm]
-M(1-y_k) + l_{1k}  & \leq x_1 \leq & u_{1k} + M(1-y_k) \\
-M(1-y_k) + l_{2k}  & \leq x_2 \leq & u_{2k} + M(1-y_k) \\
& \ldots & \\
-M(1-y_k) + l_{nk}  & \leq x_n \leq & u_{nk} + M(1-y_k).
\end{array}
\end{align*}
````

```{note}
Die Definition kann für beliebige Nebenbedingungen der Form
\begin{align*}
l \leq a_1x_1 + a_2x_2 + \ldots + a_nx_n \leq u
\end{align*}
erweitert werden.
```

#### Konvexe-Hülle Reformulierung
```{figure} ./bilder/DisjunctiveProgramm_Instance.png
:name: dp_example
:height: 300px

Beispiel: Zulässige Menge für ein disjunktives Programm.
```
Die Idee der Konvexe-Hülle Reformulierung ist, zusätzliche Entscheidungsvariablen für jede Oder-Variante zu erzeugen. Wir benötigen dann immer noch ein großes M, können dies aber für jede Oder-Variante einzeln wählen. Für unser Beispiel ergibt sich.

````{prf:example}
TO DO
````

Allgemein ergibt sich als Konvexe-Hülle Reformulierung:

````{prf:definition} Konvexe-Hülle Reformulierung
Gegeben ist ein Disjunktives Programm DP
\begin{align*}
	\left[
	\begin{array}{rcl}
	& y_1 & \\
	l_{11} & \leq x_1 \leq & u_{11} \\
	l_{21} & \leq x_2 \leq & u_{21} \\
	& \ldots & \\
	l_{n1} & \leq x_n \leq & u_{n1} 
	\end{array}
	\right]
	\vee
	\ldots
	\vee
	\left[
	\begin{array}{rcl}
	& y_k & \\
	l_{1k} & \leq x_1 \leq & u_{1k} \\
	l_{2k} & \leq x_2 \leq & u_{2k} \\
	& \ldots & \\
	l_{nk} & \leq x_n \leq & u_{nk} 
	\end{array}
	\right] .
\end{align*}
		
Die *Konvexe-Hülle Reformulierung* von DP ist
\begin{eqnarray*}
		y_1 + y_2 + \ldots + y_k & = & 1 \\
		y_1, y_2, \ldots, y_k & \in & \BB \\[6mm]
		x_{11} + x_{12} + \ldots + x_{1k} & = & x_1 \\
		& \vdots &  \\
  	    x_{n1} + x_{n2} + \ldots + x_{nk} & = & x_n \\
\end{eqnarray*}

\begin{align*}
\begin{array}{ccc}
l_{11}y_1   \leq x_{11} \leq  u_{11}y_1 & \hspace{1cm} \ldots \hspace{1cm} \ & l_{1k}y_k   \leq x_{1k} \leq  u_{1k}y_k \\
l_{21}y_1   \leq x_{21} \leq  u_{21}y_1 & \hspace{1cm} \ldots \hspace{1cm} \ & l_{2k}y_k   \leq x_{2k} \leq  u_{2k}y_k \\
\vdots &  & \vdots \\
l_{n1}y_1   \leq x_{n1} \leq  u_{n1}y_1 & \hspace{1cm} \ldots \hspace{1cm} \ & l_{nk}y_k   \leq x_{nk} \leq  u_{nk}y_k \\
\end{array}
\end{align*}
````

```{note} Die Definition kann für beliebige Nebenbedingungen der Form
\begin{align*}
l \leq a_1x_1 + a_2x_2 + \ldots + a_nx_n \leq u
\end{align*}
erweitert werden.
```


#### Vergleich zwischen beiden Formulierungen
Der Lösungsraum beider Formulierungen stimmt überein. 
Die Groß-M Formulierung benötigt weniger Entscheidungsvariablen als die Konvexe-Hülle-Formulierung.
Wird das Modell durch ein typisches Branch-And-Bound Verfahren gelöst, dient die Relaxierung des Models zur Berechnung von oberen Schranken (bei Maximierungsproblemen) bzw. unteren Schranken (bei Minimierungsproblemen) als ein Anhaltspunkt für die Güte der Formulierung. Die Konvexe-Hülle Reformulierung besitzt eine engere Relaxierung und resultiert damit in schärferen Schranken. 

```{figure} ./bilder/DisjunctiveProgramm_BigM_Reformulation.png
:name: dp_example_bigm
:height: 300px

Relaxierung der Groß-M Reformulierung.
```

```{figure} ./bilder/DisjunctiveProgramm_ConvexHull.png
:name: dp_example_convhull
:height: 300px

Relaxierung der Konvexe-Hülle Reformulierung.
```


### Linearisieren von Nichtlinearitäten
(Gemischt-ganzzahlige) lineare Programme sind in der Anwendung populär, da sie sich vergleichsweise gut lösen lassen.
Es ist deswegen wünschenswert, Modelleinschränkungen möglichst als lineare Nebenbedingungen modellieren zu können. 
In manchen Fällen lassen sich nichtlineare Nebenbedingungen durch äquivalente lineare Ausdrücke beschreiben. 
Wir lernen im Folgenden drei solche Beispiele kennen.

````{prf:example}
Wir linearisieren das Problem
\begin{alignat*}{5}
\min & \quad  &   4b_1^3-7b_1b_2+b_3 &          & & \\[2mm]
\text{s.t. } & &  b_1 + b_2+b_3 & \leq  2 & \quad\quad & &  \\
 & &  b_1,  b_2, b_3 & \in   \{0,1\} & \quad\quad & &  \\
\end{alignat*}

\Karos{33}{29}

````

#### Produkt von Binärvariablen
Es seien $b_1, b_2, \ldots b_k \in \BB$ binäre Variablen. Das Produkt
\begin{align*}
y=\prod_{i=1}^kb_i
\end{align*}
kann wie folgt linearisiert werden:
````{prf:example}
TO DO
````

#### Produkt von einer Binärvariablen und einer kontinuierlichen Variable
Es sei $x \in \RR^+$ eine kontinuierliche und $b\in \BB$ eine binäre Variable. Das Produkt 
\begin{align*}
y=x\cdot b
\end{align*}
kann wie folgt linearisiert werden:
````{prf:example}
TO DO
````


### Modellierung von stückweise linearen Funktionen

In der Realität sind Zielfunktionen nicht immer linear. Wir betrachten dazu folgendes Beispiel:

````{prf:example}
:label: fabrik

Eine Fabrik kann ein bestimmtes Produkt produzieren. Die Rüstkosten betragen 1000€ falls das Produkt überhaupt produziert wird. Die ersten 3000 produzierten Einheiten haben zusätzliche Produktionsstückkosten von 3€, die nächsten 2000 produzierten Einheiten haben zusätzliche Produktionsstückkosten von 2€, die nächsten 2000 produzierten Einheiten haben zusätzliche Produktionsstückkosten von 1€. Insgesamt hat die Fabrik einen maximale Kapazität von 7000 Stück.
````

```{figure} ./bilder/StueckweiseLineareFunktion.png
:name: StueckweiseLineareFunktion
:height: 300px

Stückweise lineare Kostenfunktion aus Beispiel {prf:ref}`fabrik`.
```

Es liegt also eine stückweise lineare Funktion vor.
Wie können wir die Produktionskosten $y$ abhängig von der Produktionsmenge $x$ modellieren? Wir betrachten zuerst den Produktionsbereich von 3000-5000 Stück:

````{prf:example}
TO DO
````

Wir führen also neue Variablen $\lambda_0, \ldots, \lambda_3 \geq 0$ ein.

````{prf:example}
TO DO
````

Wir betrachten einen konkreten Punkt $x \in [0,7000]$. 
Falls wir sicherstellen können, dass die $\lambda$-Werte abhängig vom konkreten Segment wie oben gewählt werden, können wir schreiben:

\begin{eqnarray*}
	x & = & \sum_{i=0}^k\lambda_is_i \\[2mm]
	y & = & \sum_{i=0}^k\lambda_if_i \\[2mm]
	1 & = & \sum_{i=0}^k\lambda_i 
\end{eqnarray*}

#### SOS-Mengen
Wir müssen noch sicherstellen, dass die $\lambda$-Werte in der richtigen Form sind. Es müssen also 
- alle bis auf 2 der Variablen $\lambda_0, \ldots, \lambda_k$  den Wert $0$ annehmen,
- die beiden von Null unterschiedlichen Variablen direkt aufeinanderfolgen.
Eine solche Variablenmenge nennt man SOS-2 Menge. Der Vollständigkeit halber definieren wir zuerst SOS1-Mengen.

````{prf:definition} SOS1-Menge
Eine *Special Ordered Set vom Typ 1* ist eine Menge an Entscheidungsvariablen $\lambda_0, \ldots, \lambda_k$, für die gilt, dass in einer zulässigen Lösung höchstens eine Variable gleichzeitig ungleich $0$ ist.
````

````{prf:definition} SOS2-Menge]
Eine *Special Ordered Set vom Typ 2* ist eine geordnete Menge an Entscheidungsvariablen $\lambda_0, \ldots, \lambda_k$, für die gilt, dass in einer zulässigen Lösung höchstens zwei Variablen $\lambda_i, \lambda_{i+1}$ gleichzeitig ungleich $0$ sind und diese direkt aufeinanderfolgen.
````

Wie können wir garantieren, dass eine Menge $\lambda_0, \ldots, \lambda_k$ eine SOS2-Menge ist? Wir benötigen zusätzliche Binärvariablen $\delta_0, \ldots, \delta_{k-1}$. Wir modellieren wie folgt:
````{prf:example}
TO DO
````

Dies ergibt:
\begin{eqnarray*}
	\sum_{i=0}^{k-1} \delta_i & = & 1  \\[2mm]
	\lambda_1 & \leq & \delta_1 \\[2mm]
	\lambda_i & \leq & \delta_{i-1} + \delta_i \hspace{0.5cm} \text{ für } i=0, \ldots, k-1	\\[2mm]
	\lambda_k & \leq & \delta_{k-1} \\[2mm]
	\delta_i & \in & \BB \text{ für } i=0, \ldots, k-1
\end{eqnarray*}

#### Das fertige Modell
Gegeben ist eine stückweise lineare Funktion $f(x)$ mit Stützstellen $s_0, \ldots, s_k$ und deren Funktions\-werten $f_0, \ldots, f_k$. Wir möchten den Ausdruck $y=f(x)$ innerhalb eines linearen Programms modellieren. Wir nutzen dazu folgendes Modell

\begin{eqnarray*}
x & = & \sum_{i=0}^k\lambda_is_i \\[2mm]
y & = & \sum_{i=0}^k\lambda_if_i \\[2mm]
1 & = & \sum_{i=0}^k\lambda_i \\[3mm]	
\lambda_i & \geq & 0 \hspace{0.5cm} \text{ für } i=0, \ldots, k
\end{eqnarray*}

und den Bedingungen, dass $\lambda_0, \ldots, \lambda_k$ eine SOT2-Menge ist:

\begin{eqnarray*}
\sum_{i=0}^{k-1} \delta_i & = & 1  \\[2mm]
\lambda_1 & \leq & \delta_1 \\[2mm]
\lambda_i & \leq & \delta_{i-1} + \delta_i \hspace{0.5cm} \text{ für } i=0, \ldots, k-1	\\[2mm]
\lambda_k & \leq & \delta_{k-1} \\[2mm]
\delta_i & \in & \BB \text{ für } i=0, \ldots, k-1
\end{eqnarray*}

````{prf:example}
TO DO
````

#### Approximation von beliebigen Funktionen als stückweise lineare Funktion
In der Praxis sind häufig nichtlineare kontinuierliche Funktionen gegeben, die nicht stückweise linear sind.
```{figure} ./bilder/NichtlineareFunktionFuerApproximation.png
:name: NichtlineareFunktionFuerApproximation
:height: 300px

Beispiel einer nichtlinearen Funktion.
```

Wir können solche Funktionen approximativ modellieren, indem wir Stützstellen einfügen und die Funktion zwischen den Stützstellen als stückweise linear ansehen. Je mehr Stützstellen benutzt werden, desto genauer kann der echte Funktionsverlauf nachmodelliert werden. Allerdings steigt mit genauerer Modellierung der Speicherbedarf und wahrscheinlich auch die Komplexität des resultierenden gemischt-ganzzahligen linearen Programms.
