(sec:practical-aspects)=
# Praxisaspekte beim Lösen von gemischt-ganzzahligen Programmen


## Marktübersicht MILP-Solver

Es gibt eine größere Anzahl an brauchbaren kommerziellen und nichtkommerziellen Softwaretools zum Lösen von gemischt-ganzzahligen Programmen. 
Die kommerziellen Anwendungen weisen hierbei typischerweise deutlich höhere Lösungsgeschwindigkeiten auf. Dem Dozenten ist kein aktueller unabhängiger umfassender wissenschaftlicher Vergleich zwischen den einzelnen Software\-lösungen bekannt. 

### Übersicht
Bekannte kommerzielle Anwendungen sind etwa CLEX, GUROBI und XPRESS, bekannte Open-Source Lösungen sind etwa CBC, LPSolve und SCIP.
Eine nicht qualitätsgesicherte, aber zum Stand 01.04.2020 brauchbare Auflistung aktueller Softwaretools findet sich in der Wikipedia unter
[List of Optimization Software](https://en.wikipedia.org/wiki/List_of_optimization_software).

### Benchmarks
Zum Stand vom 01.04.2020 erlaubt der 
[NEOS Server](https://neos-server.org/neos/)
Probleme kostenlos durch verschiedenene Solver zu lösen.

Ein etwas älteres Benchmark der Solver CPLEX, GUROBI und XPRESS findet sich in \emph{Josef Jablonsky: Benchmarks for current linear and mixed integer optimization solvers, Acta Universitatis Agriculturae et Silviculturae Mendelianae Brunensis, 2015}.

Weitere Benchmarks werden regelmäßig unter
[http://plato.asu.edu/bench.html](http://plato.asu.edu/bench.html) veröffentlicht.
Diese enthalten seit 2018 keine Resultate für CPLEX, Gurobi und XPRESS (siehe \emph{Hans Mittelmann: Benchmarking Optimization Software - a (Hi)Story, SN Operations Research Forum, 2020}).

Der folgende Auszug stammt aus den Vortragsfolien zu 
*Hans Mittelmann, Latest Benchmarks of Optimization Software, INFORMS Annual Meeting, Houston, 2017*.

```{figure} ./bilder/BenchmarkMittelmann2017.png
:name: BenchmarkMittelmann2017
:height: 300px

```

```{figure} ./bilder/BenchmarkMittelmann2017_2.png
:name: BenchmarkMittelmann2017_2
:height: 300px

```

```{figure} ./bilder/BenchmarkMittelmann2017_3.png
:name: BenchmarkMittelmann2017_3
:height: 300px

```

### Modellierungsumgebungen
Zusätzlich gibt es Modellierungsumgebungen, die es ermöglichen, Modelle unabhängig von einem konkreten Löser zu erzeugen. Dies erlaubt ein einfaches Austauschen des konkreten Lösers. 
Unter Umständen können diese Umgebungen nicht auf alle Eigenheiten oder Features eines speziellen Lösers zugreifen.
Je nach Kombination aus Solver und Modellierungsumgebung erlaubt die Umgebung auch eine komfortablere Erstellung des Modells.
%
Bekannte solche Frameworks sind etwa AIMMS, AMPL, GAMS, JuMP, PuLP, Pyomo.


## Möglichkeiten zur Beschleunigung des Lösungsverfahrens
Ein kritischer Aspekt bei der Arbeit mit gemischt-ganzzahligen Programmen ist die Rechenzeit die zur Lösung eines Modells benötigt wird.
Das effiziente Lösen von gemischt-ganzzahligen Programmen ist ein weites Forschungsfeld, das eine reichhaltige und tiefgehende theoretische Basis entwickelt hat.
%

Moderne Löser arbeiten typischerweise mit einem Branch-And-Bound Verfahren, dass um eine eine große Anzahl an heuristischen Methoden zur Laufzeitverbesserung erweitert wurde. Zusätzlich ist der Einsatz einer Presolve-Methode Standard. 
Die konkret vorliegende Hardwarekonfiguration hat einen zusätzlichen Einfluss auf die Lösungsgeschwindigkeit.
Aus diesem Grund ist das Laufzeitverhalten für ein bestimmtes Modell nicht komplett vorhersagbar.
Im Folgenden skizzieren wir einige allgemeine Gedanken und Ansatzpunkte, mit denen die Rechenzeit in der Praxis verbessert werden kann.

(subsubsec:kriterienBewertung)=
### Allgemeine Kriterien für die Bewertung eines Modells


#### Modellgröße
Ein erstes wichtiges Kriterium für die Bewertung eines Modells ist seine Größe.
Diese kann in der Anzahl der Variablen gemessen werden. 

Wichtig ist eine Unterscheidung in kontinuierliche und ganzzahlige Variablen. 
Kontinuierliche Variablen können effizient durch das Simplex-Verfahren bestimmt werden. 
Diskrete Variablen hingegen verursachen typischerweise den Hauptrechenaufwand, da sie durch ein aufwendigeres Branch-And-Bound Verfahren bestimmt werden müssen.

Bei manchen Modellen macht es zusätzlich Sinn, die Anzahl der Nebenbedingungen zu betrachten.


#### Laufzeit der Modellerzeugung
Der Grund für einen langsamen Gesamtlösungsprozess muss nicht unbedingt in der Laufzeit des mathematischen Lösers selbst liegen.
Bei ineffizienter Programmierung oder langsamer Datenbereitstellung kann der Hauptteil der Rechenzeit durch das Erstellen des Modells anstatt durch das Lösen verursacht werden. 

Als professionelle Diagnosetools stehen für die meisten Programmiersprachen sogenannte *Profiler* bereit, die die Programmlaufzeit nach Einzelroutinen aufschlüsseln können.  Häufig genügt zur Diagnose allerdings auch ein Lauf des Programmcodes, bei dem der finale Aufruf des Lösers auskommentiert ist.


#### Numerische Stabilität
Mathematische Löser für gemischt-ganzzahlige Programme arbeiten nicht mit exakten Zahlen, sondern nutzen die in Computern übliche Fließkommaarithmetik mit beschränkter Genauigkeit. Häufig stellt dies kein Problem dar. 

Wenn die Größenordnungen der Eingabewerte stark unterschiedlich sind, kann es zu numerischen Problemen kommen. 
Ein Vergleich von kleinstem und größtem vorkommenden Eingabewert gibt einen erstes Indiz dafür, ob das Problem numerisch schwierig zu lösen ist.


#### Schärfe der LP-Relaxierung
Wir haben in Abschnitt {ref}`subsec:disjunctiveProgramming` gesehen, dass Modelle die den gleichen zulässigen Lösungsraum beschreiben, sich trotzdem durch die Schärfe ihrer LP-Relaxierung unterscheiden können.
Es gibt tiefgehende Theorie, um den zu einem linearen Programm zugehörigen Lösungspolyeder zu beschreiben.

Einen guten ersten Eindruck zur Güte der LP-Relaxierung kann man durch die *Ganzzahligkeitslücke* (engl: integrality gap) gewinnen.

````{prf:definition} Ganzzahligkeitslücke
Gegeben ist ein gemischt-ganzzahliges Programm MILP mit optimaler Lösung $f^*$ und das zu MILP relaxierte Problem LP mit optimaler Lösung $f^*_{rel}$. Die Ganzzahligkeitslücke von MILP ist
${f^*}/{f^*_{rel}}$ falls MILP ein Minimierungsproblem ist und ${f^*_{rel}}/{f^*}$ sonst.
````

Die Ganzzahligkeitslücke ist mindestens $1$. Kleinere Werte sind im Allgemeinen besser.

````{prf:example}
TO DO
````

### Parametereinstellungen des Lösers

Die heuristischen Vorgehen innerhalb moderner Löser arbeiten mit guten Voreinstellungen, die auf konkrete Instanzen ohne Programmierarbeit angepasst werden können. Die Einstellungs\-möglichkeiten variieren für verschiedene Löser. Beispielhaft folgt eine Übersicht für den kommerziellen Solver Gurobi (Quelle: [www.gurobi.com](https://www.gurobi.com/documentation/9.0/refman/mip_models.html), abgerufen am  31.03.2020). 

```{figure} ./bilder/Gurobi_parameters_chunk1.png
:name: Gurobi_parameters_chunk1
:height: 300px

```

```{figure} ./bilder/Gurobi_parameters_chunk2.png
:name: Gurobi_parameters_chunk2
:height: 300px

```


### Heuristiken und Dekompositionen

Ist es nicht möglich, ein Modell in akzeptabler Zeit optimal zu lösen, liegt eine mögliche Strategie im Einsatz von Heuristiken. Man nimmt dann davon Abstand, beweisbar optimale Lösungen zu finden, sondern hofft auf ausreichend gute Ergebnisse. 

Ein häufiges heuristisches Vorgehen in Zusammenhang mit gemischt-ganzzahligen Programmen ist das der *Problemdekomposition*.
Dabei werden nicht mehr alle Entscheidungsvariablen "gleichzeitig" bestimmt.
Stattdessen wird das Problem in verschiedene Ebenen unterteilt, die nacheinander gelöst werden.
Jede Ebene legt eine bestimme Menge an Entscheidungsvariablen fest, die von den unterliegenden Ebenen nicht mehr revidiert werden können.

Wir betrachten dies am Beispiel des Vehicle-Routing Problems. 
Sogenannte Cluster-First Route-Second Ansätze entscheiden zuerst, welche Orte zu Touren zusammengefasst werden (erste Ebene).
Danach werden die Touren einzeln as Traveling Salesman Instanzen gelöst (zweite Ebene).

````{prf:example}
TO DO
````

### Zeitfenster
Ein spezielles Dekompositionsverfahren für zeitexpandierte Modelle sind die sogenannten *Zeitfenster*. 
Diese heißen im Engischen *time windows*.
Hierbei wird die Zeitachse in mehrere Intervalle zerlegt, die nacheinander gelöst werden. 
Dabei baut jedes Zeitfenster auf der Situation des vorhergehenden Zeitfensters auf.
Entscheidungen, die vor Beginn des aktuellen Zeitfensters liegen, sind fest und können nicht mehr geändert werden. 
Die Situation nach dem aktuellen Zeitfenster wird für dieses nicht berücksichtigt, sondern erst in den folgenden Zeitfenstern.

*Wichtig:* Der Einsatz von Zeitfenstern ist eine Heuristik. Es kann nicht  garantiert werden, dass die optimale Lösung für das ursprüngliche Problem gefunden wird.

#### Rollierende Planung
Es gibt verschiedene Möglichkeiten, Zeitfenster zu realisieren. Eine Möglichkeit sind *rollierende Fenster*, bei denen das Fenster in jedem Schritt nur um wenige Zeitschritte nach vorne bewegt wird.
````{prf:example}
TO DO
````

#### Partitionierung der Zeitachse in Intervalle
Eine Möglichkeit, um weniger Zeitfenster lösen zu müssen ist, die Zeitachse in disjunkte, aneinander angrenzende Intervalle aufzuteilen.
````{prf:example}
TO DO
````
Häufig sind die Ergebnisse dieser Methode nicht zufriedenstellend, da an den Intervallgrenzen unerwünschte Effekte auftreten.
Auf der nächsten Seite findet sich ein solcher Zeitfenster-Ansatz für das Speicheroptimierungsproblem aus Kapitel {ref}`sec:zeitdiskret`. Wir sehen, dass zu Ende jedes Zeitfensters, die Batterie komplett geleert wird. 
Dies macht für das konkrete Zeitfenster Sinn, da so Kosten innerhalb des Fensters gespart werden. 
Es führt allerdings typischerweise zu suboptimalen Lösungen für das Gesamtproblem.

#### Angrenzende Intervalle mit Vorschauperiode
Eine Lösung für das vorangegangene Problem ist der zusätzliche Einsatz einer Vorschauperiode. 
Hierbei enthält jedes Zeitfenster einen zusätzlichen Zeitraum, der an das Ende des Fensters angehängt wird.
Das Optimierungsproblem umfasst das eigentliche Intervall, zusammen mit der Vorschauperiode und optimiert beides. 
Es werden nur die Entscheidungen für das eigentliche Intervall festgehalten. 
Die Entscheidungen der Vorschauperiode werden verworfen. 
Die Vorschauperiode ist dann Teil des nächsten Zeitfensters. Ein Beispiel findet sich hier: {ref}`BatterieZeitfenster_OhneLookAhead`.

````{prf:example}
TO DO
````

```{figure} ./bilder/BatterieZeitfenster_OhneLookAhead.png
:name: BatterieZeitfenster_OhneLookAhead
:height: 300px

Zeitfensteransatz für das Problem aus Kapitel {ref}`sec:zeitdiskret` ohne Vorschauperiode.
```

```{figure} ./bilder/BatterieZeitfenster_MitLookAhead.png
:name: BatterieZeitfenster_MitLookAhead
:height: 300px

Zeitfensteransatz für das Problem aus Kapitel {ref}`sec:zeitdiskret` mit Vorschauperiode.
```

Rollierende Planung für das Beispielmodel aus Kapitel {ref}`sec:zeitdiskret`.

````{prf:example}
TO DO
````

## Interpretation der Solver-Ausgaben

Die Ausgaben des Lösers liefern wichtige diagnostische Informationen. 
Im Folgenden sehen wir die Ausgaben für das Modell aus Abschnitt {ref}`subsub:lazyConstraints`. 


```{figure} ./bilder/Gurobi_SolverOutput2_1.png
:name: Gurobi_SolverOutput2_1


```

Wir sehen, dass das Modell $2550$ Entscheidungsvariablen enthält von denen $0$ kontinuierlich, $1250$ binär und $1250$ ganzzahlig sind. 
Die Matrix $A$ besteht aus 50 Zeilen und 1275 Spalten - es sind aber nur 2500 Einträge ungleich $0$.
Wir vergleichen diese Zahlen mit den von uns erwarteten Werten. 
Dies ist ein erster einfacher Test, ob das Modell richtig implementiert ist.
Wir erkennen zusätzlich, dass Lazy Constraints aktiv sind.

```{figure} ./bilder/Gurobi_SolverOutput2_2.png
:name: Gurobi_SolverOutput2_2


```

Alls vorkommenden Zahlen liegen jeweils in der gleichen Größenordnung. 
Wäre das berichtete Intervall für eine Kategorie sehr groß, wäre dies in Hinweis auf mögliche spätere numerische Probleme beim Lösen des linearen Programms.

```{figure} ./bilder/Gurobi_SolverOutput2_3.png
:name: Gurobi_SolverOutput2_3


```

Der Solver hat über eine Heuristik eine erste zulässge Lösung gefunden bevor mit dem eigentlichen Lösungsprozess gestartet wurde.
Wir wissen also, dass die optimale Lösung einen Zielfunktionswert von höchstens 2775.3416544 hat.
Dieser Wert wird als obere Schranke für den weiteren Lösungsprozess benutzt und kann damit den Lösungsprozess beschleunigen. 

Wird vorab keine zulässige Lösung gefunden, kann der Lösungsprozess möglicherweise beschleunigt werden, indem man durch Kenntnis des konkreten Problems mit wenig Rechenaufwand außerhalb des gemischt-ganzzahligen Modells eine zulässige Lösung findet und dem Solver vorab übermittelt. Dieses Vorgehen ist allerdings nicht immer möglich.

```{figure} ./bilder/Gurobi_SolverOutput2_4.png
:name: Gurobi_SolverOutput2_4


```
Die Presolve-Routine hat das Modell etwas verkleinern können. Die Modellgröße nach der Presolve-Routine ist ein guter Kennwert für die Größe des Modells.

```{figure} ./bilder/Gurobi_SolverOutput2_5.png
:name: Gurobi_SolverOutput2_5


```
Der Löser startet nun mit der eigentlichen Suche. Zu Beginn des Suchbaums wird das relaxierte Problem gelöst (die sogenannte root relaxation).
Diese ergibt in 71 Iterationen die untere Schranke von 598.1996. 
%
Die Lösungsdauer der Root Relaxation ist mit 0.01 Sekunden unkritisch. 
Bei einer deutlich längeren Rechenzeit würden zusätzliche diagnostische Informationen zur Root Relaxation angezeigt werden.

```{figure} ./bilder/Gurobi_SolverOutput2_6.png
:name: Gurobi_SolverOutput2_6


```

Dieser Teil beschreibt den Verlauf des Branch-And-Bound Verfahrens. In festen Zeitabständen wird eine neue Zeile generiert, die Aufschluss über den aktuellen Zustand des aktuellen Suchbaums gibt.
Die Spalten bedeuten im Einzelnen
- Die 1. Spalte enthält ein h oder ein * falls seit der letzten Zeile eine neue zulässige Lösung gefunden wurde.
- Die 2. Spalte enthält die Anzahl der fertig abgearbeiteten Knoten im Suchbaum. 
- Die 3. Spalte enthält die Anzahl der noch zu bearbeitenden Blätter im Suchbaum.
- Die Spalten 4-6 beschreiben den aktuell bearbeiteten Knoten im Suchbaum. 
  - Der Wert der Relaxierung,
  - Die Tiefe im Suchbaum,
  - Die Anzahl der fraktionalen ganzzahligen Variablen.
- Die Spalten 7-9 beschreiben die Güte der bisher gefundenen Lösung.
  - Der Lösungswert der besten bisher gefundenen zulässigen Lösung,
  - Die beste bisher bewiesene Schranke,
  - Der Wert ($|$beste gefundene Lösung - beste gefundene Schranke$|$) / beste gefundene Lösung.
- Die 10. Spalte zeigt die Anzahl der durchschnittlichen Simplex-Operationen pro Knoten.
- Die 11. Spalte zeigt die Laufzeit des Branch-And-Bound Verfahrens bis zum aktuellen Stand.

```{figure} ./bilder/Gurobi_SolverOutput2_7.png
:name: Gurobi_SolverOutput2_7


```
Der Löser hat während des Lösungsprozesses zusätzliche Nebenbedingungen, sogenannte Schnittebenen (\emph{cuts}) hinzugefügt, die die optimale Lösung nicht ändern, aber zu einem schnelleren Lösungsprozess führen sollen. Die Aufschlüsselung dieser folgt nach verschiedenen Klassen von Schnittebenen. 
%
Außerdem wurden insgesamt 8 Lazy-Constraints hinzugefügt. Durch die geringe nötige Anzahl an Lazy-Constraints erkennt man, dass der Einsatz von diesen für die aktuelle Instanz sinnvoll ist.

```{figure} ./bilder/Gurobi_SolverOutput2_8.png
:name: Gurobi_SolverOutput2_8


```
Der fertige Branch-And-Bound Baum besteht aus 22 Knoten. 
Insgesamt wurden 494 Simplex-Schritte an den Knoten ausgeführt. 
Es wurden alle 8 Kerne benutzt.
Die Rechenzeit für das Branch-And-Bound Verfahren war 0.48 Sekunden.
Insgesamt wurden während des Lösungsprozesses 7 zulässige Lösungen im Zahlenbereich von 635 bis 2775 gefunden.

```{figure} ./bilder/Gurobi_SolverOutput2_9.png
:name: Gurobi_SolverOutput2_9


```

Es gilt
\begin{align*}
\frac{|\text{Wert der besten gefundenen Lösung - Wert der schärfsten unteren Schranke}|}{|\text{Wert der besten gefundenen Lösung}|} =0
\end{align*}
Damit wurde die optimale Lösung gefunden.
Als Abbruchtoleranz war $0.0004$ eingestellt, d.h. das Lösungsverfahren bricht ab, wenn dieser Quotient kleiner als $0.0004$ ist. 
Die bis dahin gefundene beste zulässige Lösung wird dann als Ergebnis gemeldet, ist aber möglicherweise nicht optimal.

Die gefundene Lösung hat einen Zielfunktionswert von 635.5025787588. 
Die beste gefundene untere Schranke für den Zielfunktionswert ist 635.5025787588.


Auf der nächsten Seite findet sich die komplette Ausgabe für das Modell.


```{figure} ./bilder/Gurobi_SolverOutput2.png
:name: Gurobi_SolverOutput2


```

# Fortgeschrittene Themen

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
: Eine Menge $C=\{1, 2, \ldots, n\}$ aus $n$ Orten und eine Distanzfunktion $d(c_i,c_j) \in \R^+$ auf $C$.

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


(subsub:lazyConstraints)=
## Lazy Constraints 
In Abschnitt {ref}`subsec:polyeder` ist beschrieben, dass der Raum der zulässigen Lösungen eines linearen Programms ein Polyeder ist, der in der Form
\begin{align*}
P=\{x \in \R^n \mid Ax \leq b\} = \left\{ x \mid \sum_{j=1}^na_{ij}x_j \leq b_i \text{ für } i = 1 \ldots m  \right\}
\end{align*}
ausgedrückt werden kann. Jede der $m$ Nebenbedingungen 
\begin{align*}
\sum_{j=1}^na_{ij}x_j \leq b_i
\end{align*}
verbietet also einen Halbraum von $\R^n$ für die Menge der zulässigen Lösungen. Wir fragen uns, ob immer alle Nebenbedingungen nötig sind, um eine optimale Lösung zu finden. 

````{prf:example}
TO DO
````

````{prf:definition} Bindende Nebenbedingung
Sei $P=\{x \in \R^n \mid Ax \leq b\}$ ein Polyeder und $\overline x=(\overline x_1, \overline x_2, \ldots, \overline x_n)^T \in P$. Dann heißt die Nebenbedingung 
$
\sum_{j=1}^na_{ij}x_j \leq b_i
$ *bindend* für $\overline x$, falls 
\begin{align*}
\sum_{j=1}^na_{ij}\overline x_j = b_i.
\end{align*}	
````

Eine Nebenbedingung ist also nur (lokal) einschränkend für einen Punkt $x$ in Optimierungsrichtung, falls Sie auch bindend ist.


Gemischt-ganzzahlige Programme werden typischerweise über Branch-And-Bound Verfahren gelöst. Es kann sein, dass viele Nebenbedingungen für keine der zulässigen Lösungen, die während des Branch-And-Bound Verfahrens besucht werden, bindend ist. 

````{prf:example}
TO DO
````

Leider kann man diese Nebenbedingungen nicht einfach komplett ignorieren, da vorab unbekannt ist, welche Nebenbedingungen für den Lösungsprozess nicht benötigt werden. 
Wie können wir trotzdem ausnutzen, wenn viele Nebenbedingungen nicht bindend werden?

Wir teilen die Menge $R$ der Nebenbedingungen auf in eine Menge von $R_{\initial}$ von "essentiellen" Nebenbedingungen, sowie eine Menge $R_{\lazy}$ von Nebenbedingungen, bei denen wir davon ausgehen, dass nur ein sehr kleiner Teil tatsächlich im Verlauf des Lösungsverfahrens bindend wird. Wir starten dann ein normales Branch-And-Bound Verfahren auf dem reduzierten Model, das nur die essentiellen Nebenbedingungen enthält. Wann immer eine zulässige Lösung $x$ gefunden wird, müssen wir überprüfen ob $x$  Nebenbedingungen aus $R_{\lazy}$ verletzt. Falls dies so ist, werden diese zum aktuellen Modell hinzugefügt. Danach wird mit dem  Branch-And-Bound Verfahren fortgefahren.
%
Insgesamt ergibt sich folgendes Vorgehen:

````{prf:algorithm} Branch-And-Bound Verfahren mit Lazy Constraints
**Eingabe:**
- Gemischt-ganzzahliges Programm $\ILP$ mit Nebenbedingungen $R=R_{\initial} \cup R_{\lazy}$

**Verfahren:**
- Starte das Branch-And-Bound Verfahren für $\ILP$ mit Nebenbedingungen $R_{\reduced} := R_{\initial}$.
  - Wann immer einer zulässige Lösung $x$ gefunden wurde
	  -	Prüfe ob $x$ eine Nebenbedingung in $R_{\lazy}$ verletzt
	  - Füge jede Nebenbedingung aus $R_{\lazy}$ die durch $x$ verletzt wird zu $R_{\reduced}$ hinzu
	  - Fahre mit dem Branch-And-Bound Verfahren fort
````

Um das Verfahren praktisch umzusetzen muss nicht unbedingt das Branch-And-Bound Verfahren selbst implementiert werden, sondern nur die Prüfroutine für die Verletzung der Nebenbedingungen. Viele Solver unterstützen dies über sogenannte *Callback-Funktionen*.


### Beispiel: Traveling Salesman Problem

Wir betrachten das Vorgehen am Beispiel der Formulierung nach Dantzig, Fulkerson und Johnson für das Traveling Salesman Problem (siehe Abschnitt {ref}`subsubsec:TSP`).		

\begin{alignat*}{5}
\min          & \quad  &   \sum_{i,j=1\ldots, n; i\not=j} & d_{ij}x_{ij}         & & \\[4mm]
\text{s.t. } & &  \sum_{j=1\ldots n, \ i \not=j}x_{ij} & =   1 && \quad\quad & & \forall i= 1, \ldots, n \\[2mm]
 & &  \sum_{i=1\ldots n, \ i \not=j}x_{ij} & =   1 && \quad\quad & & \forall j= 1, \ldots, n \\[2mm]
& & \sum_{i \in C'} \sum_{j \in C'}x_{ij} & \leq   |S|-1 && \quad\quad & & \forall C' \subset \{2, \ldots, n\}, \hspace{0.3cm} |C'| \geq 2 \\[2mm]
& & x_{ij} & \in  \B && && \forall i,j= 1, \ldots, n.
\end{alignat*}
Die ersten beiden Klassen von Nebenbedingungen stellen sicher, dass jeder Ort genau einmal besucht und wieder verlassen wird. Bei $n$ Orten gibt es je $n$ Nebenbedingungen von jeder Klasse. Mit Hinblick auf den Rechenaufwand ist dies unproblematisch. Wir betrachten beide Klassen als essentiell. Diese Nebenbedingungen bilden die Menge $R_{\initial}$.

Die dritte Klasse von Nebenbedingungen verhindert Subtouren. Diese Nebenbedingungen bilden die Menge $R_{\lazy}$. Es gibt eine Nebenbedingung pro möglicher Subtour. Dies sind insgesamt $2^{n-1}$ Nebenbedingungen. Selbst für relativ kleine Werte von $n$ sprengt dies die Möglichkeiten moderner Computer. Wir gehen davon aus, dass nur vergleichsweise wenige Subtouren im Lösungsprozess wirklich relevant werden. Dies Annahme legt die Nutzung als Lazy Constraint nahe.

```{figure} ./bilder/TSP-LoesungMitSubtouren.png
:name: TSP-LoesungMitSubtouren}
:height: 300px

```

Es bleibt noch die Frage zu klären, wie wir für eine gegebene Lösung $x$ effizient überprüfen, ob eine der Subtour-Eliminationsbedingungen verletzt wird. Falls alle $2^{n-1}$ Bedingungen erstellt und einzeln überprüft werden müssten, wird das Verfahren extrem langsam und nicht sinnvoll.

Für eine gegebene Lösung $x$ können wir den Nachfolger eines Ortes $k$ in der Tour oder Subtour bestimmen durch
\begin{align*}
\text{Nachfolger}(k)=l \text{ mit der Eigenschaft } x_{kl}=1
\end{align*}

````{prf:example}
TO DO
````

Wir können die Überprüfung effizient mit folgendem Algorithmus vornehmen:

````{prf:algorithm} Überprüfe auf Subtouren in Lösung $x$
:label: algo:findeSubtour

**Input**: Mögliche Lösung $x$

**Output**: Subtour falls existent

Startort=0

AktuellerOrt = Nachfolger(Startort)

Tour=[Startort, AktuellerOrt]

**while** *AktuellerOrt $\neq=$ Startort* **do**

  AktuellerOrt = Nachfolger(Startort)

  Füge AktuellerOrt an Tour an

**if** *Tour beinhaltet nicht alle Orte* **then**

  Subtour Tour gefunden
````

Der Algorithmus findet auf jeden Fall eine Subtour falls eine solche in $x$ existiert. Eine leicht abgewandelte Version des Vorgehens kann auch alle möglichen vorhandenen Subtouren finden.
````{prf:example}
TO DO
````

```{figure} ./bilder/TSP-lazy-constraints.png
:name: TSP-lazy-constraints
:height: 300px

Eine TSP-Instanz mit 50 Orten. Die Grafik zeigt alle 36 Zwischenlösungen, die bei einem Branch-And-Bound Verfahren mit Lazy-Constraints gefunden werden.
```


## Modellierung von stückweise linearen Funktionen

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

### SOS-Mengen
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
	\delta_i & \in & \B \text{ für } i=0, \ldots, k-1
\end{eqnarray*}

### Das fertige Modell
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
\delta_i & \in & \B \text{ für } i=0, \ldots, k-1
\end{eqnarray*}

````{prf:example}
TO DO
````

### Approximation von beliebigen Funktionen als stückweise lineare Funktion
In der Praxis sind häufig nichtlineare kontinuierliche Funktionen gegeben, die nicht stückweise linear sind.
```{figure} ./bilder/NichtlineareFunktionFuerApproximation.png
:name: NichtlineareFunktionFuerApproximation
:height: 300px

Beispiel einer nichtlinearen Funktion.
```

Wir können solche Funktionen approximativ modellieren, indem wir Stützstellen einfügen und die Funktion zwischen den Stützstellen als stückweise linear ansehen. Je mehr Stützstellen benutzt werden, desto genauer kann der echte Funktionsverlauf nachmodelliert werden. Allerdings steigt mit genauerer Modellierung der Speicherbedarf und wahrscheinlich auch die Komplexität des resultierenden gemischt-ganzzahligen linearen Programms.


	