(sec:practical-aspects)=
# Praxisaspekte beim Lösen von gemischt-ganzzahligen Programmen

## Lösungsverfahren

### Preprocessing
Leistungsstarke Löser setzen *Presolve-Routinen* ein.
Diese stellen einen  Vorberechnungsschritt dar, der das Ziel hat, das zu lösende Problem zu verkleinern, sowie zu vereinfachen. 
Der ursprüngliche zulässige Bereich soll dabei voll rekonstruierbar bleiben.

Eine detaillierte Beschreibung solcher Presolve-Routinen findet sich in *Achterberg, Bixby, Gu, Rothberg, Weninger: Presolve Reductions in Mixed Integer Programming, INFORMS Journal On Computing, 2019*.


### Branch and bound
Es gibt verschiedene Verfahren, um gemischt-ganzzahlige Programme zu lösen. 
Der Kern aktueller Softwaresysteme sind Branch-And-Bound Verfahren. 
Hierbei wird zuerst das relaxierte Problem gelöst (die sogenannte Root-Relaxation).
Danach wird nach ganzzahligen Variablen, für die eine fraktionale (nicht ganzzahlige) Lösung vorliegt verzweigt. 
Eine gute Einführung in Branch-And-Bound Verfahren für gemischt-ganzzahlige Programme findet sich in [Bradley, Hax, Magnanti: Applied Mathematical Programming, Addison-Wesley, 1977](http://web.mit.edu/15.053/www/AMP.htm).

Dieser algorithmische Kern wird häufig durch zahlreiche heuristische Zusätze erweitert. 
Beispielsweise werden Heuristiken benutzt, um schnell zulässige Lösungen zu finden oder gute Branching-Regeln zu lernen.
Bedingt durch das Branch-And-Bound Verfahren selbst, sowie die Zusatz\-heuristiken ist eine genaue Vorhersage der nötigen Rechenzeit normalerweise nicht möglich. 
Es gibt allerdings Anhaltspunkte, von denen einige in Abschnitt {ref}`subsubsec:kriterienBewertung` geschildert werden.



### Schnittebenen
Eine Möglichkeit, um den Lösungsprozess zu beschleunigen, ist das Zufügen von zusätzlichen Nebenbedingungen, die den zulässigen Lösungsraum nicht verändern, aber in einer schärferen Relaxierung resultieren. Solche Nebenbedinungen heißen *Schnittebenen* (eng: cutting planes). 
Bei tiefer Problemkenntnis können Schnittebenen manuell zugefügt werden. 
Einige Löser erzeugen und nutzen automatisiert Schnittebenen.


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

(subsub:lazyConstraints)=
### Lazy Constraints 
In Abschnitt {ref}`subsec:polyeder` ist beschrieben, dass der Raum der zulässigen Lösungen eines linearen Programms ein Polyeder ist, der in der Form
\begin{align*}
P=\{x \in \RR^n \mid Ax \leq b\} = \left\{ x \mid \sum_{j=1}^na_{ij}x_j \leq b_i \text{ für } i = 1 \ldots m  \right\}
\end{align*}
ausgedrückt werden kann. Jede der $m$ Nebenbedingungen 
\begin{align*}
\sum_{j=1}^na_{ij}x_j \leq b_i
\end{align*}
verbietet also einen Halbraum von $\RR^n$ für die Menge der zulässigen Lösungen. Wir fragen uns, ob immer alle Nebenbedingungen nötig sind, um eine optimale Lösung zu finden. 

````{prf:example}
TO DO
````

````{prf:definition} Bindende Nebenbedingung
Sei $P=\{x \in \RR^n \mid Ax \leq b\}$ ein Polyeder und $\overline x=(\overline x_1, \overline x_2, \ldots, \overline x_n)^T \in P$. Dann heißt die Nebenbedingung 
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


#### Beispiel: Traveling Salesman Problem
Wir betrachten das Vorgehen am Beispiel der Formulierung nach Dantzig, Fulkerson und Johnson für das Traveling Salesman Problem (siehe Abschnitt {ref}`subsubsec:TSP`).		

\begin{alignat*}{5}
\min          & \quad  &   \sum_{i,j=1\ldots, n; i\not=j} & d_{ij}x_{ij}         & & \\[4mm]
\text{s.t. } & &  \sum_{j=1\ldots n, \ i \not=j}x_{ij} & =   1 && \quad\quad & & \forall i= 1, \ldots, n \\[2mm]
 & &  \sum_{i=1\ldots n, \ i \not=j}x_{ij} & =   1 && \quad\quad & & \forall j= 1, \ldots, n \\[2mm]
& & \sum_{i \in C'} \sum_{j \in C'}x_{ij} & \leq   |S|-1 && \quad\quad & & \forall C' \subset \{2, \ldots, n\}, \hspace{0.3cm} |C'| \geq 2 \\[2mm]
& & x_{ij} & \in  \BB && && \forall i,j= 1, \ldots, n.
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
	