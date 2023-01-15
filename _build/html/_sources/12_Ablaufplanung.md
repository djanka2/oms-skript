# Ablaufplanung
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


## Ein einfaches zeitkontinuierliches Modell}

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
