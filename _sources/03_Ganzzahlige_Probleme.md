---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.4
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

(sec:integer-problems)=
# Ganzzahlige Probleme

## Ganzzahligkeitsbedingungen und weitere Modellarten

In vielen Problemstellungen dürfen manche oder alle Entscheidungsvariablen nicht beliebige reelle Werte, sondern nur einen eingeschränkten Wertebereich, etwa den der ganzen Zahlen annehmen. Beispiele sind etwa der Kauf eines Investitionsgutes oder das An- und Ausschalten einer Maschine. Man unterscheidet unter anderem die folgende Problemarten, die wir der Einfachheit halber nur in Standardform darstellen.

Lineare Programme (LP)
: Die Entscheidungsvariablen dürfen beliebige reelle Werte annehmen.
: \begin{alignat*}{5}
\min          & \quad  &   \v c^T\v x &          & & \\[2mm]
\text{s.t. } & &  \m A\v x & = & \v b & \\
& & \v x & \geq & \ \v 0 & &&
\end{alignat*}

Ganzzahlige lineare Programme (Integer Linear Programs / ILP)
: Alle Entscheidungsvariablen dürfen nur ganzzahlige Werte annehmen.
: \begin{alignat*}{5}
\min_{\v x}         & \quad  &   \v c^T\v x &          & & \\[2mm]
\text{s.t. } & & \m A\v x & = & \v b & \\
& & \v x & \geq & \ \v 0 & &&\\
& & \v x & \in & \Z
\end{alignat*}



Binäre lineare Programme
: Alle Entscheidungsvariablen dürfen nur die Werte $0$ und $1$ annehmen.
: \begin{alignat*}{5}
\min_{\v x}          & \quad  &   \v c^T\v x &          & & \\[2mm]
\text{s.t. } & &  \m A\v x & = && \ \v b & \\
& & \v x & \geq && \ \v 0 &\\
& & \v x & \in && \{0,1\}^n 
\end{alignat*}


Gemischt-ganzzahlige lineare Programme (Mixed Integer Linear Programs / MILP)
: Manche Entscheidungsvariablen dürfen nur ganzzahlige Werte annehmen.
: \begin{alignat*}{5}
\min_{\v x,\v y}         & \quad  &   \v c^T\v x+\v h^T\v y &          & & \\[2mm]
\text{s.t. } & &  \m A\v x +\m G\v y& = & \v b & \\
& & \v x & \geq & \ \v 0 & &&\\
& & \v y & \geq & \ \v 0 & &&\\
& & \v y & \in & \Z
\end{alignat*}


## Relaxierung von Problemen mit Ganzzahligkeitsbedingungen

Für alle Problemtypen, die Ganzzahligkeitsbedingungen enthalten, bezeichnet das zugehörige *relaxierte Problem* das Problem, bei dem die Ganzzahligkeitsbedingungen entfernt wurden. Für jede Binärvariable $x_i$ fordern wir im zugehörigen relaxierten Problem zusätzlich, dass $0 \leq x_i \leq 1$ gilt.

Das relaxierte Problem des ILP
\begin{alignat*}{5}
\min_{\v x}         & \quad  &   \v c^T\v x &          & & \\[2mm]
\text{s.t. } & &  \m A\v x & = & \v b & \\
& & \v x & \geq & \ \v 0 & &&\\
& & \v x & \in & \Z
\end{alignat*}
ist das LP
\begin{alignat*}{5}
\min_x         & \quad  &   \v c^T\v x &          & & \\[2mm]
\text{s.t. } & &  \m A\v x & = & \v b & \\
& & \v x & \geq & \ \v 0 & &&
\end{alignat*}

An folgenden Beispiel sehen wir den Zusammenhang der Lösungsräume zwischen einem ganzzahligen linearen Problem und seiner relaxierten Version:
```{figure} ./bilder/relaxierung.png
:name: fig:relaxierung
:width: 400px

Zulässige Menge eines ILP und des zugehörigen relaxierten Problems.
```

Beobachtung: Eine Lösung des ganzzahligen Problems ist zwar zulässig für das relaxierte Problem, aber möglicherweise nicht optimal. Ein zulässiger Punkt des relaxierten Problems ist für das ganzzahlige Problem möglicherweise unzulässig (da evtl. die Ganzzahligkeitsbedingungen nicht erfüllt sind). Das gilt insbesondere für die optimale Lösung des relaxierten Problems. Allerdings gilt für die optimale Lösung des relaxierten Problems, das sie mindestens so gut ist wie die optimale Lösung des ganzzahligen Problems. Diesen Umstand machen sich viele Lösungsverfahren für ganzzahlige Probleme zu Nutze. 


## Lösungsverfahren

### Branch and bound
Es gibt verschiedene Verfahren, um gemischt-ganzzahlige Programme zu lösen. 
Der Kern aktueller Softwaresysteme sind *Branch-And-Bound* Verfahren. 
Hierbei wird zuerst das relaxierte Problem gelöst (die sogenannte Root-Relaxation).
Danach wird nach ganzzahligen Variablen, für die eine fraktionale (nicht ganzzahlige) Lösung vorliegt, verzweigt. Das bedeutet, diese Variablen werden probehalber auf verschiedene ganzzahlige Werte fixiert und es wird eine neue Relaxierung gelöst.  Sobald eine *zulässige* ganzzahlige Lösung gefunden wurde, kann man deren Zielfunktionswert mit dem Zielfunktionswert der Relaxierung vergleichen. Daraus kann man dann die Güte der gefundenen zulässigen Lösung abschätzen. 
Eine gute Einführung in Branch-And-Bound Verfahren für gemischt-ganzzahlige Programme findet sich in [Bradley, Hax, Magnanti: Applied Mathematical Programming, Addison-Wesley, 1977](http://web.mit.edu/15.053/www/AMP.htm).

Im schlechtesten Fall werden beim reinen Branch-and-Bound alle Kombinationen von ganzzahligen Variablen betrachtet (also sehr sehr viele). Deshalb wird dieser algorithmische Kern wird häufig durch zahlreiche heuristische Zusätze erweitert. 
Beispielsweise werden Heuristiken benutzt, um schnell zulässige Lösungen zu finden oder gute Branching-Regeln zu lernen.
Bedingt durch das Branch-And-Bound Verfahren selbst, sowie die Zusatzheuristiken ist eine genaue Vorhersage der nötigen Rechenzeit normalerweise nicht möglich. 
Es gibt allerdings Anhaltspunkte, von denen einige in Abschnitt {ref}`subsubsec:kriterienBewertung` geschildert werden.


### Schnittebenen
Eine Möglichkeit, um den Lösungsprozess zu beschleunigen, ist das Zufügen von zusätzlichen Nebenbedingungen, die den zulässigen Lösungsraum nicht verändern, aber in einer schärferen Relaxierung resultieren. Solche Nebenbedinungen heißen *Schnittebenen* (eng: cutting planes). 
Bei tiefer Problemkenntnis können Schnittebenen manuell zugefügt werden. 
Einige Löser erzeugen und nutzen automatisiert Schnittebenen.


### Preprocessing
Leistungsstarke Löser setzen *Presolve-Routinen* ein.
Diese stellen einen Vorberechnungsschritt dar, der das Ziel hat, das zu lösende Problem zu verkleinern, sowie zu vereinfachen. 
Der ursprüngliche zulässige Bereich soll dabei voll rekonstruierbar bleiben.

Eine detaillierte Beschreibung solcher Presolve-Routinen findet sich in *Achterberg, Bixby, Gu, Rothberg, Weninger: Presolve Reductions in Mixed Integer Programming, INFORMS Journal On Computing, 2019*.


## Einige Standardprobleme 
Wir schauen uns in diesem Abschnitt einige Standardprobleme an, mit denen das typische Vorgehen bei der ganzzahligen Programmierung verdeutlicht werden soll. Diese Probleme tauchen in der Praxis oft auch als Teil von umfangreicheren Modellen auf. 


### Das Rucksackproblem
Das *Rucksackproblem* sind verschiedene Gegenstände mit einem bestimmten Gewicht und einem Nutzwert gegeben. Aus diesen Gegenständen soll nun eine Auswahl getroffen werden, die in einen Rucksack mit einer vorgegebenen Gewichtsschranke mitgenommen werden können.

```{figure} ./bilder/rucksack.png
:name: fig:rucksack
:width: 400px

Beispiel Rucksackproblem.
```

Um das Beispiel aus {numref}`fig:rucksack` zu modellieren, orientieren wir uns an den vier Elementen eines Optimierungsproblems (Problemdaten, Entscheidungen, Zielfunktion, Nebenbedingungen):

Problemdaten
: 5 Gegenstände mit Gewichten (2kg, 1kg, 4kg, 1kg, 12kg) und Werten ($2, $1, $10, $2, $4).
: Maximales Rucksackgewicht von 15kg.

Entscheidungen (Optimierungsvariablen)
: Für jeden Gegenstand $i, i=1,\dots,5$ wird entschieden, ob er mitgenommen wird ($x_i=1$) oder nicht ($x_i=0$).

Zielfunktion
: Der Gesamtwert des Rucksacks soll maximiert werden:
: \begin{align*}
	\max_{x_1,x_2,x_3,x_4,x_5} 2x_1+1x_2+10x_3+2x_4+4x_5
  \end{align*}

Nebenbedingungen
: Das maximale Gewicht darf nicht überschritten werden:
: \begin{align*}
	2x_1+1x_2+4x_3+1x_4+12x_5\leq 15
  \end{align*}
: Die Entscheidungen sind binär:
: \begin{align*}
	x_1,x_2,x_3,x_4,x_5\in \{0,1\}
  \end{align*}

Die allgemeine Definition lautet:
````{prf:definition} Rucksackproblem
Instanz
: Gegeben sind $n$ Objekte mit Werten $v_i$ und Gewichten $w_i$ für $i=1, \ldots, n$ sowie ein maximales Gesamtgewicht $W$.

Aufgabe
: Gesucht ist eine Teilmenge der Objekte mit möglichst großem Gesamtwert, deren Gesamt\-gewicht kleiner oder gleich $W$ ist.
````

Die allgemeine Formulierung als (binäres) lineares Programm lautet:
%````{topic} 
\begin{alignat*}{5}
\min_{\v x}          & \quad  &   \sum_{i=1}^n v_ix_i &          & & \\[2mm]
\text{s.t. } & &  \sum_{i=1}^n w_ix_i & \leq && \ W & \\
& & x_i & \in && \{0,1\},\quad i=1,\dots,n
\end{alignat*}
oder in Matrixform
\begin{alignat*}{5}
\min_{\v x}          & \quad  &   \v v^T\v x &          & & \\[2mm]
\text{s.t. } & &  \v w^T\v x & \leq && \ W & \\
& & \v x &\in && \{0,1\}^n
\end{alignat*}
%````

Möglich sind auch Instanzen, bei denen der gleiche Objekttyp (festgelegt durch die Kombination von Wert und Gewicht) mehrfach vorkommen darf. In diesem Fall werden die Nebenbedingungen $x_i\in\{0,1\}$ ersetzt durch $0\leq x_i\leq h_i,\quad x_i\in\N$, wobei jeder Gegenstand $i$ maximal $h_i$ Mal mitgenommen werden darf.


### Bin Packing
Beim *Bin Packing-Problem* betrachtet man eine Menge an Objekten mit zugehörigen Gewichten. Außerdem sind beliebig viele Behälter ("bins") mit einer vorgegeben Kapazität vorhanden. Ziel ist es, die Objekte so in Behälter zu packen, dass die Kapazitätseinschränkung für jeden Behälter eingehalten wird und insgesamt möglichst wenige Behälter gebraucht werden.

```{figure} ./bilder/binpacking.png
:name: fig:binpacking
:width: 400px

Beispiel Bin Packing Problem.
```
Um das Beispiel aus {numref}`fig:binpacking` zu modellieren, formulieren wir wieder Problemdaten, Entscheidungen, Zielfunktion und Nebenbedingungen:

Problemdaten
: 5 Gegenstände mit Gewichten $\v w=(2,2,2,3,3)$
: Maximale Behälterkapazität $B=4$.

Entscheidungen (Optimierungsvariablen)
: Man braucht zunächst eine obere Schranke $k_{max}$ für die Anzahl der benötigten Behälter. Die Anzahl der Objekte ist eine solche obere Schranke. Mehr als 5 Behälter werden wir sicher nicht brauchen. 
: Wir führen folgende Binärvariablen ein:
: \begin{align*}
	x_{ij}&=\left\{\begin{array}{lr}1 &\text{Objekt }i\text{ ist in Behälter }j.\\
									0& \text{sonst} \end{array}\right.,\quad i=1,\dots,5, j=1,\dots,k_{max}\\
	y_j&=\left\{\begin{array}{lr}1 &\text{Behälter }j\text{ wird benutzt.}\\
									0& \text{sonst} \end{array}\right.,\quad j=1,\dots,k_{max}
	\end{align*}

Zielfunktion
: Minimiere die Anzahl der benutzten Behälter:
: \begin{align*}
	\min_{\v x, \v y} y_1+y_2+y_3+y_4+y_5
  \end{align*}

Nebenbedingungen
: 1. Bei jedem benutzten Behälter muss das zulässige Gesamtgewicht beachtet werden. Wenn der Behälter nicht benutzt wird ($y_j=0$), dann dürfen auch keine Gegenstände darin sein (alle $x_{ij}=0$ für dieses $j$)
:   \begin{align*}
		2x_{1,1}+2x_{2,1}+2x_{3,1}+3x_{4,1}+3x_{5,1}&\leq 6\cdot y_1\\
		2x_{1,2}+2x_{2,2}+2x_{3,2}+3x_{4,2}+3x_{5,2}&\leq 6\cdot y_2\\
		2x_{1,3}+2x_{2,3}+2x_{3,3}+3x_{4,3}+3x_{5,3}&\leq 6\cdot y_3\\
		2x_{1,4}+2x_{2,4}+2x_{3,4}+3x_{4,4}+3x_{5,4}&\leq 6\cdot y_4\\
		2x_{1,5}+2x_{2,5}+2x_{3,5}+3x_{4,5}+3x_{5,5}&\leq 6\cdot y_5
	\end{align*}
: 2. Jeder Gegenstand muss in genau einem Behälter sein (nicht mehr und nicht weniger):
:   \begin{align*}
		x_{1,1}+x_{1,2}+x_{1,3}+x_{1,4}+x_{1,5}&=1\\
		x_{2,1}+x_{2,2}+x_{2,3}+x_{2,4}+x_{2,5}&=1\\
		x_{3,1}+x_{3,2}+x_{3,3}+x_{3,4}+x_{3,5}&=1\\
		x_{4,1}+x_{4,2}+x_{4,3}+x_{4,4}+x_{4,5}&=1\\
		x_{5,1}+x_{5,2}+x_{5,3}+x_{5,4}+x_{5,5}&=1
	\end{align*}
: 3. Alle Variablen sind binär:
:   \begin{align*}
		x_{ij}, y_{j}\in \{0,1\},\quad i,j=1,\dots,5
	\end{align*}

````{note}
Kleinere Werte für $k_{max}$ (wir sagen dazu: schärfere obere Schranken) sind nützlich, da sie zu kleineren Modellen und damit zu einer kürzeren Rechenzeit führen.
````

Die allgemeine mathematische Definition lautet:
````{prf:definition} Bin Packing Problem 
Instanz
: Gegeben ist eine Menge $U=\{1, 2, \ldots, n\}$ mit Gewichten $w_i$ für $i\in U$ sowie eine (Behälter-)Kapazität $B$.

Aufgabe
: Gesucht ist eine Aufteilung $U=U_1 \cup U_2 \cup \ldots \cup U_k$ in $k$ disjunkte Mengen, so dass die Summe der Elemente in jedem $U_i$ kleiner als $B$ ist und $k$ minimal wird.
````

Die allgemeine Formulierung als (binäres) lineares Programm lautet:
\begin{alignat*}{5}
\min_{\v x, \v y}          & \quad  &   \sum_{j=1}^{k_{max}} y_j &          & & \\[2mm]
\text{s.t. } & &  \sum_{i=1}^n w_ix_{ij} & \leq && \ B\cdot y_j,\quad &&j=1,\dots,k_{max} \\
& & \sum_{j=1}^{k_{max}} x_{ij} & = && \ 1,\quad &&i=1,\dots,n\\
& & x_{ij},y_j &\in && \{0,1\},\quad &&i=1,\dots,n\quad j=1,\dots,k_{max}
\end{alignat*}
 

### Einführung Mengenprobleme: Ein einfaches Standortproblem 
% Siehe auch Gurobi Cell Tower
Ein Telekommunikationsunternehmen will ein neues Wohngebiet mit Breitband-Internet versorgen. 
Dazu müssen Versorgungsstationen aufgestellt werden.
Das Wohngebiet ist in Häuserblocks $S=\{1, 2, \ldots, s\}$ unterteilt. 
Es gibt $v$ mögliche Positionen $V=\{1, 2, \ldots, v\}$ für die Versorgungsstationen.
Jede Versorgungsstation darf höchstens 200 Meter von den zu versorgenden Häuserblocks entfernt sein. Für jede mögliche Position $i$ sind die Kosten $w_i$ gegeben, eine Versorgungsstation an Position $i$ zu bauen. Gesucht ist eine kostenoptimale Auswahl an Versorgungsstationen, die alle Blocks versorgt.

```{figure} ./bilder/standortproblem.png
:name: fig:standortproblem
:width: 400px

Beispiel Standortproblem mit Häuserblocks $1,\dots,6$ und möglichen Standorten für Versorgungsstationen $v_1,\dots,v_5$. Orange Linien bedeuten, dass der jeweilige Häuserblock von dem Standort $v_i$ abgedeckt ist.
```

Problemdaten
: Es ist gegeben, welche Standorte welche Häuserblocks abdecken. Im Beispiel {numref}`fig:standortproblem` sind das:
: \begin{align*}
	v_1=\{1,2,4\},\quad v_2=\{1,4,5\},\quad v_3=\{2,4,5,6\},\\
	v_4=\{3,5,6\},\quad v_5=\{1,2,3,5\}
  \end{align*}
: Dies können wir in der folgenden *Abdeckungsmatrix* zusammenfassen:
: \begin{align*}
	\begin{array}{r|cccccc}
	 & 1 & 2 & 3 & 4 & 5 & 6\\
	 \hline
	 v_1 & x & x &   & x &  & \\
	 v_2 & x &   &   & x & x & \\
	 v_3 &   & x &   & x & x & x\\
	 v_4 &   &   & x &   & x & x\\
	 v_5 & x & x & x &   & x & \\
	\end{array}
	\end{align*}
: Weiterhin sind die Kosten $w_1,w_2,w_3,w_4,w_5$ für die Errichtung einer Station gegeben.

Entscheidungen (Optimierungsvariablen)
: \begin{align*}
	x_{i}&=\left\{\begin{array}{lr}1 &\text{Station am Standort }v_i\text{ wird gebaut}.\\
									0& \text{sonst} \end{array}\right.,\quad i=1,\dots,5.
	\end{align*}

Zielfunktion
: Die Gesamtkosten sollen minimiert werden:
: \begin{align*}
	\min_{\v x} w_1x_1+w_2x_2+w_3x_3+w_4x_4+w_5x_5
  \end{align*}

Nebenbedingungen
: Jeder Block soll versorgt werden. Dies ergibt eine Nebenbedingung pro Block:
: \begin{align*}
	x_1+x_2+x_5&\geq 1\\
	x_1+x_3+x_5&\geq 1\\
	x_4+x_5&\geq 1\\
	x_1+x_2+x_3&\geq 1\\
	x_2+x_3+x_4+x_5&\geq 1\\
	x_3+x_4&\geq 1
  \end{align*}
: Ganzzahligkeitsbedingungen:
: \begin{align*}
	x_1,\dots,x_5\in\{0,1\}
  \end{align*}

<!-- Ist zusätzlich noch einen Teilnehmeranzahl $t_i$ für jeden Block und eine Kapazität $k_i$ für jede Versorgungsposition gegeben, so ergibt sich folgende zusätzliche Nebenbedingung: -->



### Überdeckungensprobleme auf Mengen

Das obige Standortproblem ist ein Beispiel für ein *minimum set cover* Problem. Wir führen diese Problemklasse nun formell ein. Gegeben ist eine Grundmenge $S$ sowie ein Mengensystem $C \subseteq 2^S$. Dabei bezeichnet $2^S$ die Potenzmenge von $S$, also die Menge $2^S=\{S' \mid S' \subseteq S \}$ aller möglichen Teilmengen von $S$. 

Im gewichteten Fall ist jeweils ein Gewicht $w_c$ für jedes Element aus $C$ gegeben.

````{prf:example}
```{figure} ./bilder/setcover.png
:name: fig:setcover
:width: 400px
```
````

Das *(ungewichtetet) Überdeckungsproblem* sucht eine Menge von möglichst wenigen Elementen $\{C_1, C_2, \ldots, C_l\} \subseteq C$, die $S$ überdecken, für die also jedes Element aus $S$ in mindestens einer Menge $C_i$ enthalten ist.
```{prf:example}
$C_1\cup C_2 \cup C_4$ überdeckt $S$ mit Kosten $3$, denn $\{1,2\}\cup\{3,4\}\cup\{4,5\}=\{1,2,3,4,5\}=S$.
```

Die *gewichtete* Variante sucht nicht nach möglichst wenigen Mengen sondern nach einer Lösung mit einem möglichst kleinem Gesamtgewicht:
```{prf:example}
$C_1\cup C_2 \cup C_4$ überdeckt $S$ mit Kosten $2+2+1=5$, denn $\{1,2\}\cup\{3,4\}\cup\{4,5\}=\{1,2,3,4,5\}=S$.
```

%Die *Kardinalität* einer Menge ist die Anzahl ihrer Elemente.
Es ergibt sich folgende formale Definition.
````{prf:definition} Gewichtetes Überdeckungsproblem
Instanz
: Gegeben ist eine endliche Menge $S=\{1, 2, \ldots, |S|\}$, ein Mengensystem $C=\{C_1, C_2, \ldots, C_{|C|}\} \subseteq 2^S$ sowie Gewichte $w_c$ für jedes $c \in C$.

Aufgabe
: Gesucht ist eine Teilmenge $C'= \{C_1, C_2, \ldots, C_l\} \subseteq C$, so dass $S=C_1 \cup C_2 \cup \ldots \cup C_l$ und das  Gesamtgewicht $\sum_{c \in C'}w_c$ minimal ist.
````
Das ungewichtete Überdeckungsproblem kann als Spezialfall des gewichteten Problems angesehen werden, bei dem alle Gewichte $1$ sind.


Um das Problem als binäres Programm zu modellieren, müssen wir die Eingabedaten, also vor allem die Mengen $S$ und $C$, in eine passende Form bringen. Wir konstruieren dafür die sogenannte *Inzidenzmatrix* $A \in \B^{|S|\times |C|}$ für $C$. Zeilen der Matrix repräsentieren Elemente aus $S$. Spalten repräsentieren Mengen aus $C$. Ein Matrixelement $a_{ij}$ hat den Wert $1$ genau dann, wenn das zugehörige Element in der entsprechenden Menge enthalten ist. Ansonsten besitzt das Element den Wert $0$. Es ist also

\begin{align*}a_{ij}=\begin{cases}
1 & ,i \in C_j \\
0 & , \text{sonst }
\end{cases}
\end{align*}

Wir betrachten wieder das vorherige ungewichtete Beispiel.
\begin{align*}
C=\{\{1,2\},\{2,3,4\},\{3,4\},\{4,5\}\}
\end{align*}

Es ergibt sich folgende Inzidenzmatrix:
\begin{align*}
\m A=\bmat 1 & 0 & 0 & 0\\
			1 & 1 & 0 & 0\\
			0 & 1 & 1 & 0\\
			0 & 1 & 1 & 1\\
			0 & 0 & 0 & 1\emat
\end{align*}
Jede Zeile steht dabei für ein Element der Grundmenge $S$, und jede Spalte für eine Element des Mengensystems $C$.

Das zugehörige binäre Programm löst unsere Instanz:
\begin{alignat*}{5}
\min_{\v x}         & \quad  &   x_1+x_2+x_3+x_4 &          & & \\[2mm]
\text{s.t. } & & \bmat 1 & 0 & 0 & 0\\
			1 & 1 & 0 & 0\\
			0 & 1 & 1 & 0\\
			0 & 1 & 1 & 1\\
			0 & 0 & 0 & 1\emat \bmat x_1\\x_2\\x_3\\x_4\emat & \geq && \bmat 1\\1\\1\\1\emat & \\
& & x_1,x_2,x_3,x_4 & \in && \{0,1\}
\end{alignat*}

Allgemein ergibt sich für das gewichtete Überdeckungsproblem das binäre Programm
\begin{alignat*}{5}
\min_{\v x}         & \quad  &   \v w^T\v x &          & & \\[2mm]
\text{s.t. } & & \m A\v x & \geq &\ \v 1 & \\
& & \v x & \in & \{0,1\}^n
\end{alignat*}
mit dem Gewichtsvektor $\v w\in\R^{|C|}$ und der Inzidenzmatrix $\m A\in\R^{|S|\times|C|}$.

### Packungsprobleme auf Mengen
Im Englischen heißt das Packungsproblem auf Mengen *set packing*.
Gegeben ist eine Grundmenge $S$ sowie ein Mengensystem $C \subseteq 2^S$. 
Im gewichteten Fall ist jeweils ein Gewicht $w_c$ für jedes Menge aus $C$ gegeben. Zwei Mengen heißen disjunkt, falls sie kein Element gemeinsam besitzen.
````{prf:example}
```{figure} ./bilder/setpacking.png
:name: fig:setpacking
:width: 400px
```
````

Gesucht ist eine Teilmenge $C'=\{C_1, C_2, \ldots, C_l\}$ von paarweise disjunkten Mengen mit maximalem Gesamtgewicht.
````{prf:example}
- $\{1,2\},\{3,4\}$ ist Packung und hat Gewicht $4$.
- $\{1,2\},\{4,5\}$ ist Packung und hat Gewicht $3$.
- $\{2,3,4\},\{4,5\}$ ist keine Packung.
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
\begin{alignat*}{5}
\max_{\v x}         & \quad  &   \v w^T\v x &          & & \\[2mm]
\text{s.t. } & & \m A\v x & \leq &&\ \v 1 & \\
& & \v x & \in && \{0,1\}^n
\end{alignat*}
mit dem Gewichtsvektor $\v w\in\R^{|C|}$ und der Inzidenzmatrix $\m A\in\R^{|S|\times|C|}$.


### Zerlegungsprobleme auf Mengen
Im Englischen heißt das Zerlegungsproblem *set partitioning*. Gegeben ist eine Grundmenge $S$ sowie ein Mengensystem $C \subseteq 2^S$. Im gewichteten Fall ist jeweils ein Gewicht $w_c$ für jedes Menge aus $C$ gegeben. 
````{prf:example}
```{figure} ./bilder/setpartition.png
:name: fig:setpartition
:width: 400px
```
````

Gesucht ist eine Überdeckung von $S$ durch *disjunkte* Mengen aus $C$.
````{prf:example}
Die Beispielinstanz besitzt keine zulässige Lösung.
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
\begin{alignat*}{5}
\max_{\v x}         & \quad  &   \v w^T\v x &          & & \\[2mm]
\text{s.t. } & & \m A\v x & = &&\ \v 1 & \\
& & \v x & \in && \{0,1\}^n
\end{alignat*}


## Modellierungstricks II

Viele Echtweltprobleme zeichnen sich durch eine große Anzahl an zu modellierenden Aspekten aus.
Die Standardprobleme aus dem letzten Kapitel bilden bereits einen kleinen Fundus an Bausteinen für die Modellierung. 
Im Folgenden werden einige wiederkehrende Aspekte zusammen mit einer möglichen Lösung präsentiert. Dies knüpft an {ref}`subsubsec:tricks1` an mit dem Unterschied, dass für die nächsten Tricks immer ganzzahlige (binäre) Variablen benötigt werden.


### Logische Bedingungen an Variablen

(subsubsec:logikBeispiel)=
#### Junktoren
Viele Echtweltprobleme beinhalten auch logische Zusammenhänge. Wir betrachten ein Beispiel aus der Produktion.

````{prf:example}
Es gibt $5$ Maschinen $A,B,C,D, E$, die jeweils ein- oder ausgeschaltet sein können.
1. Ist  $A$ eingeschaltet, so darf $B$ nicht eingeschaltet sein. 
2. Ist  $D$ eingeschaltet, so ist immer auch mindestens  $B$ oder  $C$ eingeschaltet.
3. Ist  $D$ ausgeschaltet, so sind immer auch  $B$ und  $C$ ausgeschaltet.
4. Es ist immer genau eine der beiden Maschinen $D$ und $E$ eingeschaltet.
````

Wir übersetzen dies in einen logischen Ausdruck mit den logischen Variablen $A,B,C,D,E$, die die Werte *wahr* und *falsch* annehmen können.

````{prf:example}
Variablen $A,B,C,D,E$ mit der Bedeutung
  \begin{align*}
	\text{Variable }X\text{ ist wahr}\Leftrightarrow \text{Maschine }X\text{ ist angeschaltet.}
	\end{align*}
1. $A\Rightarrow \neg B$
2. $D\Rightarrow (B\vee C)$
3. $\neg D \Rightarrow (\neg B \wedge \neg C)$
4. $D\dot{\vee}E$
````

````{note}
Aussagenlogische Variablen können durch sogenannte *Junktoren* miteinander verknüpft werden. Die wichtigsten Junktoren sind 
- Konjunktion (UND-Verknüpfung), Symbol: $\wedge$
- Disjunktion (ODER-Verknüpfung), Symbol: $\vee$	
- Negation (Verneinung), Symbol: $\neg$	
- Implikation (logischer Schluss), Symbol: $\Rightarrow$	
- Äquivalenz (Gleichheit), Symbol: $\Leftrightarrow$	
- Exklusiv-Oder (Entweder-Oder), Symbol: $\dot\vee$	
````

<!-- #### Exkurs: Crash-Kurs Logik
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
-->

#### Modellierung der Junktoren als arithmetische Ausdrücke
Logische Variablen werden durch Binärvariablen modelliert. Für jede logische Variable $V$ führen wir eine Binärvariable $x_V$ ein, mit der Bedeutung
\begin{align*}
x_V=\left\{\begin{array}{rl}
1 & \text{, V ist wahr} \\
0 & \text{, V ist falsch}
\end{array}\right.
\end{align*}

````{prf:theorem}
Die logischen Operationen Negation, Und, Oder, Implikation und Äquivalenz lassen sich wie folgt modellieren:
  
|           	| Logische Formel 		| 	Arithmetischer Ausdruck 		|
|---------- 	|-------------   		| -------------:					|
|				| $A$					| $x_A=1$							|
| Negation 		| $\neg A$          	| $1-x_A=1$							|
| Konjunktion 	| $A\wedge B$       	| $x_A+x_B=2$ oder $x_A=1, x_B=1$	|
| Diskunktion 	| $A\vee B$         	| $x_A+x_B\geq 1$					|
| Implikation 	| $A\Rightarrow B$		| $x_A\leq x_B$						|
| Exklusiv-Oder | $A\dot\vee B$			| $x_A+x_B=1$						|
| Äquivalenz	| $A\Leftrightarrow B$	| $x_A=x_B$							|

Sind Literale $L_1, L_2, \ldots, L_n$ gegeben, so können wir die Situation "\{mindestens, genau, höchstens\} $k$ aus $n$ Literalen sind wahr" modellieren: 

- Mindestens $k$ aus $n$ sind wahr:
  \begin{align*}
  \sum_{i=1}^n x_{L_i} \geq k
  \end{align*}
- Höchsten $k$ aus $n$ sind wahr:
  \begin{align*}
  \sum_{i=1}^n x_{L_i} \leq k
  \end{align*}
- Genau $k$ aus $n$ sind wahr:
  \begin{align*}
  \sum_{i=1}^n x_{L_i} = k
  \end{align*}
````

#### Transformation logischer Zusammenhänge in arithmetische Ausdrücke

Sind mehrere logische Formeln konjunktiv (also durch UND-Verknüpfungen) miteinander verbunden, so können die Formeln  einzeln behandelt werden.

````{prf:example}
Die logische Formel
\begin{align*}
	(A\vee B \vee C) \wedge (\neg B \Leftrightarrow C)\wedge D \wedge (A\Rightarrow C)
\end{align*}
ergibt
\begin{align*}
	x_A+x_B+x_C&\geq 1\\
	1-x_B&=x_C\\
	x_D&=1\\
	x_A&\leq x_C
\end{align*}
````
Sind umfangreichere Formeln gegeben, so können diese über die Rechenregeln für aussagenlogische Formeln in die Konjunktion (d.h. mit UND verknüpfte) von bekannten durch arithmetische Ausdrücke modellierbaren Formeln zurückgeführt werden. 

Wir wandeln das einführende Beispiel aus Abschnitt {ref}`subsubsec:logikBeispiel` um:

````{prf:example}
1. $A\Rightarrow \neg B: \quad x_A\leq 1-x_B$
2. $D\Rightarrow (B\vee C):\quad x_D\leq x_B+x_C$
3. $\neg D \Rightarrow (\neg B \wedge \neg C):\quad 1-x_D\leq 1-x_B, 1-x_D\leq 1-x_C$
4. $D\dot{\vee}E: x_D+x_E=1$
````


<!-- ##### Allgemeines Vorgehen
Die in der Praxis auftretenden Formeln sind typischerweise einfach genug, dass keine komplizierten Umformungen vorgenommen werden müssen. Als allgemeines Verfahren für sehr komplizierte Ausdrücke kann man folgendes Verfahren nutzen: Schritt 1: Umwandlung der Formel in konjunktive Normalform. Schritt 2: Behandlung der einzelnen Klauseln nach der Methode "mindestens $1$ aus $k$". -->


### Logische Bedingungen für Nebenbedingungen

<!-- In manchen Fällen sollen Nebenbedingungen nicht durchgehend gelten, sondern nur, wenn eine logische Variable wahr ist. Wir betrachten dazu ein Beispiel:

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
```` -->

<!-- ### Endliche Wertemenge für Entscheidungsvariablen
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
-->


%(subsec:disjunctiveProgramming)=
%### Logische Bedingungen an Nebenbedingungen (Disjunktive Programmierung)

In manchen Anwendungen liegen mehrere Mengen von Nebenbedingungen vor, die durch eine logische Oder-Verknüpfung miteinander verbunden sind. Man gibt die Menge der zulässigen Lösungen manchmal auch in der Form
\begin{align*}
\bigcup_{i=1\ldots k}\left\{\v x \mid \m A_i\v x \leq \v b_i, \ \v x \geq 0 \right\}
\end{align*} 
an. Diese Darstellung kann sich etwa ergeben, wenn die Menge der zulässigen Lösungen nicht zusammenhängend oder nicht konvex ist. Ein Beispiel dafür haben wir schon in {ref}`subsubsec:betraege` gesehen: Soll z.B. für eine Variable $x$ die Nebenbedingung $|x|\geq 2$ gelten, so ist dies gleichbedeutend damit, dass entweder $x\geq 2$ oder aber $x\leq -2$ ist.
Allgemein kann dies auch für eine größere Anzahl von Ungleichungen gelten.

````{prf:example}
Für zwei Variablen $x_1,x_2$ eines MILP soll entweder gelten
\begin{align*}
 2&\leq x_1\leq 4\\
 3&\leq x_2\leq 4
\end{align*}
oder
\begin{align*}
 1&\leq x_1\leq 3\\
 0&\leq x_2\leq 2
\end{align*}
Grafisch lässt sich die zulässige Menge wie folgt darstellen:
```{figure} ./bilder/DisjunctiveProgramm_Instance.png
:name: fig:disjunktiv
:width: 400px
```
````

Für das weitere Vorgehen benötigen wir den Begriff des "großen $M$": In der Optimierung bezeichnet der Buchstabe $M$ typischerweise einen sehr großen Wert. Dabei ist nicht von Bedeutung wie groß der Wert von $M$ genau ist, solange er "groß genug" ist. Das große $M$ kann im Zusammenspiel mit einer Binärvariable $y$ dazu verwendet werden, einzelne Ungleichungen an- oder abzuschalten. Das "Abschalten" einer Ungleichung geschieht, indem die Grenzen bei Bedarf auf einen so großen Wert (das große $M$) gesetzt werden, dass die Ungleichung für das Problem irrelevant wird.

````{prf:example}
Für ein MILP soll die Ungleichung 
\begin{align*}
1\leq x_1\leq 3
\end{align*} 
gelten, falls $y_1=1$ ist, wobei $y_1\in\{0,1\}$. 
Die Nebenbedingung wird nun wie folgt formuliert:
\begin{align*}
-M(1-y_1)+1\leq x_1\leq 3+M(1-y_1)
\end{align*} 
Es ergibt sich z.B. für $M=1000$:
\begin{align*}
y_1=0 \Rightarrow -999\leq x_1\leq 1003\\
y_1=1 \Rightarrow 1\leq x_1\leq 3\\
\end{align*} 
Klar ist: Wenn $M$ groß genug ist, wird die erste Ungleichung immer erfüllt sein und so die Lösung nicht einschränken. Ein passender Wert für $M$ ist dabei noch zu bestimmen. 
````

Wir versuchen unser Beispiel mit Hilfe von zusätzlichen Binärvariablen $y_1$ und $y_2$ sowie einem großen $M$ zu formulieren. $y_1$ bezeichnet dabei das erste Paar von Ungleichungen, $y_2$ das zweite.

````{prf:example}
Auswahl der beiden Varianten:
\begin{align*}
y_1+y_2&=1\\
y_1,y_2&\in \{0,1\}
\end{align*}
Nebenbedingungen für $x_1$ und $x_2$:
\begin{align*}
-M(1-y_1)+1&\leq x_1 \leq 3+M(1-y_1)\\
-M(1-y_1)+0&\leq x_2 \leq 3+M(1-y_1)\\
-M(1-y_2)+2&\leq x_1 \leq 3+M(1-y_2)\\
-M(1-y_2)+3&\leq x_2 \leq 3+M(1-y_2)\\
\end{align*}
Wie groß muss dann $M$ mindestens sein? Es gilt auf jeden Fall
\begin{align*}
1&\leq x_1\leq 4\\
0&\leq x_2\leq 4
\end{align*}
Damit ist $M=4$ groß genug.
````

````{note}
Möglichst kleine Werte für $M$ können unter Umständen die Lösungsgeschwindigkeit des Modells verbessern.
````

Allgemein ergibt sich als Groß-M Reformulierung

````{prf:definition} Groß-M Reformulierung
Gegeben sind durch "Oder" verknüpfte Mengen von Nebenbedingungen
\begin{align*}
\left[
\begin{array}{rcl}
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
l_{1k} & \leq x_1 \leq & u_{1k} \\
l_{2k} & \leq x_2 \leq & u_{2k} \\
& \ldots & \\
l_{nk} & \leq x_n \leq & u_{nk} 
\end{array}
\right]
\end{align*}
sowie Zahlen $M_i\in\R$, so dass 
\begin{align*}x_i \in [-M_i+\min\{l_{ij} \mid k=1,\ldots, k\},\max\{u_{ij} \mid k=1,\ldots, k\}+M_i]\end{align*}
für alle $i=1\ldots n$ in jeder zulässigen Lösung $x$ gilt. 

Die *Groß-M Reformulierung* für die Nebenbedingungen ist

\begin{eqnarray*}
y_1 + y_2 + \ldots + y_k & = & 1 \\
y_1, y_2, \ldots, y_k & \in & \B
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

<!-- #### Konvexe-Hülle Reformulierung
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
		y_1, y_2, \ldots, y_k & \in & \B \\[6mm]
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
 -->

### Min min Probleme
In {ref}`subsubsec:minmax` hatten wir das Problem betrachtet, die maximale Endzeit eines Projektes zu minimieren -- ein $\min \max$ Problem. Wir greifen das Beispiel wieder auf, um das Prinzip eines $\min \min$ Problems zu illustrieren.
````{prf:example}
Ein Projektplanungsproblem besteht aus vier Arbeitspaketen. Die Startzeiten jedes Arbeitspakets $s_1,s_2,s_3,s_4$ sind die Entscheidungsvariablen. Ziel des Optimierungsproblems ist es, so früh wie möglich mit dem Projekt zu beginnen. Das Optimierungsproblem lautet also:
\begin{align*}
\min_{s_1,s_2,s_3,s_4} \min\{s_1,s_2,s_3,s_4\}
\end{align*}

```{figure} ./bilder/minmin.png
:width: 400px
```
Die Reformulierung als MILP ist etwas komplizierter als im $\min \max$ Fall. Wir führen für jedes $s_i$ eine binäre Variable $z_i$ ein, die den Wert $1$ annimmt, wenn es sich bei $s_i$ um das Minimum der Menge $\{s_1,s_2,s_3,s_4\}$ handelt und $0$ sonst. Des weiteren führen wir ein großes $M$ ein. Das gibt uns die Möglichkeit, die Konstruktion aus {ref}`subsubsec:minmax` so zu erweitern, dass alle Nebenbedingungen bis auf eine (die, für die $y_i=1$ ist) durch das große $M$ "abgeschaltet" werden.

Das folgende MILP ist äquivalent zum obigen $\min \min$ Problem:
\begin{alignat}{5}
\min_{s_1,s_2,s_3,s_4,z_1,z_2,z_3,z_4,y} & \quad  &   y & & & \\[2mm]
\text{s.t. } & &  s_1&\leq y-M(1-z_1)\\
             & &  s_2&\leq y-M(1-z_2)\\
             & &  s_3&\leq y-M(1-z_3)\\
             & &  s_4&\leq y-M(1-z_4)\\
			 & &  1 & = z_1+z_2+z_3+z_4\\
			 & & z_i&\in \{0,1\},\quad i=1,\dots,4
\end{alignat}
Als Wert für $M$ kommt z.B. die größtmögliche Startzeit, die in dem Problem vorkommen kann, in Frage.
````

### Beträge revisited
In {ref}`subsubsec:betraege` haben wir festgestellt, dass Nebenbedingungen der Art 
\begin{align*}
|x|\geq \alpha
\end{align*}
zu einer nicht konvexen zulässigen Menge führen. Ebenso lässt sich die Zielfunktion
\begin{align*}
\min_x -|x|
\end{align*}
nicht mit den dort vorgestellten Techniken reformulieren. Der Grund dafür ist, dass der Betrag eine versteckte Maximumsbildung ist. Wenn wir die in obige Formel einsetzen, erhalten wir
\begin{align*}
 \min_x -|x| = \min_x (-\max\{x,-x\}) = \min_x \min\{x,-x\}
\end{align*} 
Nicht konvexe Menge und $\min \min$ Probleme... dahinter verbirgt sich doch wieder ein großes $M$!

Konkret geht man so vor, dass man $x$ durch die *Different zweier* positiver Variablen $x_p-x_n$ ersetzt, wobei garantiert wird, dass eine von den beiden gleich Null ist. Welche das ist, kommt darauf an, ob $x$ positiv (dann ist $x_n=0$) oder negativ ist (dann ist $x_p=0$). Den Betrag wiederum kann man dan als *Summe* dieser beiden Variablen schreiben, diese ist dann immer positiv. Das Konstrukt wird mit Hilfe einer Binärvariable und einem großen $M$ umgesetzt und sieht wie folgt aus: Das Optimierungsproblem
\begin{align*}
\min_x -|x|
\end{align*}
ist äquivalent zu
\begin{alignat}{5}
\min_{x,x_p,x_n,y}   \quad &   -(x_p+x_n) & & & \\[2mm]
\text{s.t. }\quad  &   x=x_p-x_n\\
             &   0\leq x_p \leq My\\
             &   0\leq x_n \leq M(1-y)\\
			 &   y\in \{0,1\}
\end{alignat}
Ähnlich ist die Nebenbedingung
\begin{align*}
|x|\geq \alpha
\end{align*}
äquivalent zu
\begin{alignat}{5}
			 & &  x_p+x_n&\geq \alpha\\
			 & &  x&=x_p-x_n\\
             & &  0&\leq x_p \leq My\\
             & &  0&\leq x_n \leq M(1-y)\\
			 & &  y&\in \{0,1\}
\end{alignat}
Dieses Vorgehen ist rechentechnisch aufwendiger als das in {ref}`subsubsec:betraege` vorgestellte, da man eine zusätzliche Binärvariable, zwei kontinuierliche Variablen und zwei zusätzliche Ungleichungen einführt. Dafür ist es allgemeiner, da es für beide Richtungen der Ungleichung funktioniert.


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

Es gilt
\begin{align*}
b_1^3 = \left\{\begin{array}{rl}1, & \quad \text{wenn } b_1=1\\
								0, & \quad \text{wenn } b_1=0\end{array}\right. = b_1
\end{align*}
für $b_1\in\{0,1\}$. Damit können wir $b_1^3$ ersetzen.

Um $b_1\cdot b_2$ zu reformulieren, führen wir eine neue Variable $b_{12}$ ein, für die gelten soll $b_{12}=b_1\cdot b_2$. Das erreichen wir durch folgende zusätzliche Nebenbedingungen:
\begin{align*}
b_{12}&\leq b_1\\
b_{12}&\leq b_2\\
b_{12}&\geq b_1+b_2-1
\end{align*}

Insgesamt ist das Problem damit äquivalent zu folgendem MILP:
\begin{alignat*}{5}
\min & \quad  &   4b_1-7b_{12}+b_3 &          & & \\[2mm]
\text{s.t. } & &  b_1 + b_2+b_3 & \leq  2 & \quad\quad & &  \\
 & &  b_{12}&\leq b_1 & \quad\quad & &  \\
 & &  b_{12}&\leq b_2 & \quad\quad & &  \\
 & &  b_{12}&\geq b_1+b_2-1 & \quad\quad & &  \\
 & &  b_1,  b_2, b_3 & \in   \{0,1\} & \quad\quad & &  \\
 & & b_{12} & \in   \{0,1\}
\end{alignat*}
````

#### Produkt von Binärvariablen
Es seien $b_1, b_2, \ldots b_k \in \B$ binäre Variablen. Das Produkt
\begin{align*}
y=\prod_{i=1}^kb_i
\end{align*}
kann durch folgende Bedingungen an die Variable $y$ linearisiert werden:
1. \begin{align*}
  y\leq b_i,\quad i=1,\dots, k
  \end{align*}
  Damit ist sichergestellt, dass $y=0$, sobald (mindestens) eines der $b_i=0$.
2. \begin{align*}
  y\geq \sum_{i=1}^k b_i-k+1,\quad i=1,\dots, k
  \end{align*}
  Damit ist sichergestellt, dass $y=1$, wenn alle $b_i=1$.
Danach kann man jedes Auftreten des nichtlinearen Terms $\prod_{i=1}^kb_i$ durch (den linearen Term) $y$ ersetzen.

#### Produkt von einer Binärvariablen und einer kontinuierlichen Variable
Es sei $x \in \R^+$ eine kontinuierliche und $b\in \B$ eine binäre Variable. Das Produkt 
\begin{align*}
y=x\cdot b
\end{align*}
kann wie folgt linearisiert werden. Wir benötigen zunächst eine obere Schranke $M$ für $x$ (diese sollte sich aus dem Probleme ergeben). Wir fügen dem Problem nun folgende Nebenbedingungen hinzu:
1. \begin{align*}
  y&\leq Mb
  \end{align*}
  Damit ist sichergestellt, dass wenn $b=0$ auch $y=0$ ist.
2.  \begin{align*}
  y&\leq x
  y&\geq x-M(1-b)
  \end{align*}
  Damit ist sichergestellt, dass wenn $b=1$ ist, sowohl $y\leq x$ als auch $y\geq x$ gilt. Mit anderen Worten $y=x$, wie gewünscht.

Danach kann man jedes Auftreten des nichtlinearen Terms $x\cdot b$ durch (den linearen Term) $y$ ersetzen.

## Allgemeines Vorgehen bei der Modellierung
In {ref}`sec:intro` und in den Beispielmodellen in diesem Kapitel haben wir bereits gesehen, dass die Optimierungsmodelle in dieser Vorlesung aus den vier Komponenten Problemdaten, Entscheidungsvariablen, Zielfunktion und Nebenbedingungen bestehen. 

In diesem Abschnitt möchten wir noch auf einige Punkte eingehen, die besonders beim Erstellen von größeren Modellen mit Gurobi oder einem anderen Framework hilfreich, um Modellierungsfehler zu vermeiden und den Code nachvollziehbarer zu machen.

Konkret empfiehlt es sich, bei der Erstellung eines Modells nach den folgenden fünf Schritten vorzugehen.

**Schritt 1: Indexmengen decklarieren**

Gerade wenn es mehrere Mengen gibt, über die iteriert wird, ist es hilfreich auch Indexvariablen festzulegen, die durchgängig verwendet werden. Die Indexmengen werden wir in allen folgenden Schritten (2.-5.) benutzt, daher empfiehlt es sich, diese als erstes anzulegen. Die Indexmengen können und sollten dabei möglichst nah an der Problemformulierung gewählt werden.

Beispiel: Für ein Standortproblem möchten Sie als mögliche Standorte für ein Warenlager die Städte Karlsruhe, Berlin und Heidelberg modellieren. Statt $x_1,x_2,x_3$ können Sie die zugehörigen Entscheidungsvariablen auch $x_{Karlsruhe}, x_{Berlin}, x_{Heidelberg}$ nennen. In Gurobi können Sie die Indexmenge dann direkt beim Erstellen der Variablen übergeben, d.h. anstatt

```{code-cell} ipython3
:tags: ["remove-output","remove-stderr"]

x = m.addVars(3, name="x", vtype=GRB.BINARY)
```
schreiben Sie
```{code-cell} ipython3
:tags: ["remove-output","remove-stderr"]

staedte = ["Karlsruhe", "Berlin", "Heidelberg"]
x = m.addVars(staedte, vtype=GRB.BINARY)
```

Sie können dann auf die Variablen z.B. mit ``x["Karlsruhe"]`` zugreifen. Das funktioniert auch, wenn der Index aus Paaren besteht. Wollen Sie z.B. eine Variable für die Transportkosten von Karlsruhe nach Berlin anlegen und diese mit $y_{Karlsruhe, Berlin}$ bezeichnen, so können Sie das in Gurobi wie folgt tun:
```{code-cell} ipython3
:tags: ["remove-output","remove-stderr"]

transport = [("Karlsruhe", "Berlin"), ("Heidelberg", "Karlsruhe")]
y = m.addVars(staedte, vtype=GRB.BINARY)
```
Dadurch werden zwei Variablen erzeugt, auf die Sie dann einfach mit ``y["Karlsruhe","Berlin"]`` und ``y["Heidelberg","Karlsruhe"]`` zugreifen können.

Indexmengen sind ein wichtiges Werkzeug, um kurzen, lesbaren Code zu erzeugen.


**Schritt 2: Problemdaten identifizieren und Bezeichner festlegen**

Im Kontext der Optimierung sind Problemdaten zwar feste Zahlen, es empfiehlt sich aber trotzdem, ihnen Bezeichner zu geben. Dadurch ist man näher an der mathematischen Formulierung, die Nachvollziehbarkeit des Programms wird erhöht und Änderungen am Code sowie Rechnen von verschiedenen Szenarien werden enorm erleichtert. 

**Schritt 3: Entscheidungsvariablen definieren**

Auch genannt Optimierungsvariablen, also das, was der Löser berechnen soll. Zu einer Variable gehören ein Datentyp (stetig, ganzzahlig, binär) und evtl. Grenzen (z.B. $0\leq x\leq 20$). Wir sprechen oft von Entscheidungsvariablen, auch wenn manche der Variablen keine "Entscheidungen" im umgangssprachlichen Sinne sind. Sämtliche unbekannten Werte, von denen Sie möchten, dass der Löser für sie einen Wert berechnet, gehören zu den Entscheidungs- bwz. Optimierungsvariablen.

**Schritt 4: Zielfunktion formulieren**

Was soll optimiert werden? Das muss ein (linearer) Ausdruck in den Entscheidungsvariablen und den Problemdaten sein. Evtl. empfiehlt es sich, schrittweise vorzugehen: wenn z.B. die Gesamtkosten minimiert werden sollen, sollte man zunächst die einzelnen Beiträge zu den Gesamtkosten identifizieren und Terme für diese aufstellen.

**Schritt 5: Nebenbedingungen formulieren**

Schließlich formulieren Sie die Nebenbedingungen an die Variablen, die sich aus der Problemstellung ergeben oder aus der Definition der Optimierungsvariablen. Wenn das Problem unzulässig oder unbeschränkt ist, sind die Nebenbedingungen oft die Fehlerquelle. Etwa, wenn bestimmte Nebenbedingungen vergessen wurden oder versehentlich sich widersprechende Nebenbedingungen formuliert wurden. 



## Anwendung: Ablaufplanung (Scheduling)
Ablaufplanung wird im Englischen *scheduling* genannt. 
Es gibt sehr viele verschiedene Probleme der Ablaufplanung. Eine Übersicht über akademische Arbeiten findet sich etwa in 
*Michael L. Pinedo: Scheduling. Theory, Algorithms and Systems, Springer, 2016*.

Allen Problemvarianten gemeinsam ist, dass es um die *Zuteilung von Resourcen zu Aufgaben über die Zeit* geht, sowie um das *Erstellen eines zugehörigen Zeitplans*. Wir betrachten zuerst ein Beispiel aus der Produktion:

````{prf:example}
Farbe wird in drei Schritten produziert: Zuerst werden die Rohmaterialien gemahlen, dann wird gemixt und am Ende verpackt. Wir erstellen den Produktionsplan für eine Fabrik, die weiße und blaue Farbe produzieren kann. Der Mixer muss 10 Minuten gesäubert werden, wenn von blauer auf weißer Farbe gewechselt wird. In umgekehrter Reihenfolge muss nicht gesäubert werden. Wir besitzen zwei Mühlen (eine langsame und eine schnelle), einen Mixer sowie eine Packstation. Alle Maschinen können Batches zu je 1000 Litern bewältigen. Unsere Aufgabe ist, 2000 Liter weiße Farbe und 2000 Liter blaue Farbe zu produzieren.
````

Ein Produktionsplan wird typischerweise über ein *Gantt-Chart* visualisiert:

```{figure} ./bilder/gantt.png
:name: fig:gantt
:width: 400px
```

In der Produktionsplanung sind häufig für die einzelnen Aufgaben zusätzlich individuelle, gewünschte Fertigstellungszeitpunkte gegeben.
Typische Zielfunktionen sind die Minimierung einer der folgenden Terme
- Die Summe der Fertigstellungszeitpunkte aller Aufgaben (engl: total completion time). 
- Der Fertigstellungszeitpunkt der letzten Aufgabe(n) (engl: makespan)
- Die Anzahl der zu spät fertiggestellten Aufgaben (engl: total number of tardy/late jobs)
- Die längste Verzögerung für eine Aufgabe (engl: maximum lateness).
In Realweltproblemen gibt es typischerweise eine hohe Anzahl an zusätzlichen Arten von Nebenbedingungen die in ihrer Kombination meistens sehr individuell auf ein spezifisches Problem angepasst sind.

Bei der Modellierung von Ablaufplanungsproblemen durch gemischt-ganzzahlige Programme gibt es zwei grundsätzliche Modelltypen: *zeitdiskretisierte Modelle* sowie *zeitkontinuierliche Modelle*. Mit allgemeinen zeitdiskretisierten Modellen beschäftigen wir uns im nächsten Kapitel. Im folgenden werden wir ein zeitkontinuierliches Modell für ein einfaches Problem aus der Projektplanung entwickeln.


### Ein einfaches zeitkontinuierliches Modell

Ein Projektleiter erstellt einen Zeitplan für sein Projekt. Er nutzt dafür folgende Informationen.  
- Eine Menge an Aufgaben $A=\{1, 2, \ldots, n\}$.
- Für jede Aufgabe $i$ ist ihre Dauer $d_i$ gegeben. $D=\{d_1, d_2, \ldots, d_n\}$
- Es ist eine Menge $L=\{(p_1,s_1), \ldots, (p_n,s_n)\} \subset A\times A$ von Abhängigkeiten gegeben mit der Bedeutung: Aufgabe $p_i$ muss abgeschlossen sein, bevor Aufgabe $s_i$ starten kann.
- Es ist eine Menge $B=\{(a_1,b_1), \ldots, (a_n,b_n)\} \subset A\times A$ von Blockierungen gegeben mit der Bedeutung: Aufgabe $a_i$ und $b_i$ können nicht zeitgleich ausgeführt werden.	

Gesucht ist
- die Startzeit $x_i$ für jede Aufgabe $i \in A$, so dass das Projekt möglichst schnell abgeschlossen ist (d.h. alle Aufgaben sind beendet).

Wir betrachten die Beispielinstanz $A=\{1, 2, \ldots, 6\}$ und $L=\{(1,4),(2,4),(3,6), (4,5),(4,6)\}$ und $D=(1,2,1,2,2,1)$ und $B=\{(1,2),(2,3),(1,3)\}$.

```{figure} ./bilder/scheduling_beispiel.png
:name: fig:scheduling_beispiel
:width: 400px
```
Wir führen folgende Optimierungsvariablen ein:
- Den Anfangszeitpunkt $x_1,\dots,x_6$ für jede Aufgabe
- Den spätesten Endzeitpunkt $y$ (siehe die $\min \max$ Konstruktion {ref}`subsubsec:minmax`)
- Um die Blockierungsbedingungen zu modellieren, führen wir für jede der Blockierungen in $B$ eine binäre Entscheidungsvariable $z_{ij}$, die angibt, welcher der beiden Aufgaben $i$ bzw. $j$ zuerst ausgeführt wird.

Für jede Vorgängerbedingung führen wir eine Nebenbedingung ein. Die Blockierungsbedingungen sind etwas komplizierter: Hier brauchen wir zwei Bedingungen für jede Blockierungsbedingung, von denen jeweils eine mittels eines großen $M$ "abgeschaltet" wird. Wir können $M$ z.B. $M=d_1+d_2+d_3+d_4+d_5+d_6$ setzen. Dies ist offenbar eine obere Schranke für die Endzeit, wenn nämlich alle Aufgaben einfach sequentiell abgearbeitet werden.

Es ergibt sich als Modell für diese Instanz:

\begin{alignat*}{5}
\min_{\v x, y, \v z}         & \quad  &   y &          & & \\[2mm]
\text{s.t. } & & & && & \\
\text{Makespan}\quad && \text{Vorgänger}\quad && \text{Blockierungen}\quad &&\\
x_1+d_1 &\leq y \quad & x_1+d_1&\leq x_4 \quad & x_1+d_1&\leq x_2+Mz_{12}\\
x_2+d_2 &\leq y \quad & x_2+d_2&\leq x_4 \quad & x_2+d_2&\leq x_1+M(1-z_{12})\\
x_3+d_3 &\leq y \quad & x_3+d_3&\leq x_6 \quad & x_1+d_1&\leq x_3+Mz_{13}\\
x_4+d_4 &\leq y \quad & x_4+d_4&\leq x_5 \quad & x_3+d_3&\leq x_1+M(1-z_{13})\\
x_5+d_5 &\leq y \quad & x_4+d_4&\leq x_6 \quad & x_2+d_2&\leq x_3+Mz_{23}\\
x_6+d_6 &\leq y \quad & &				 \quad & x_3+d_3&\leq x_2+M(1-z_{23})\\
x_1,x_2,\dots,x_6 & \geq 0 \quad & &		 \quad & z_{12},z_{13},z_{23}&\in \{0,1\}
\end{alignat*}

Als allgemeines Modell für diese Problemklasse ergibt sich
\begin{alignat*}{5}
\min_{\v x, y, \v z} & \quad  &   y &          & & \\[4mm]
\text{s.t. } & & x_i + d_i  & \leq   \ y & \quad\quad & & \forall i \in A \\
& & x_i + d_i  & \leq   \ x_j & \quad\quad & & \forall (i,j) \in L \\[4mm]
& & x_i + d_i  & \leq   \ x_j + (1-z_{ij})d_{max} & \quad\quad & & \forall (i,j) \in B \\
& & x_j + d_j  & \leq   \ x_i + z_{ij}d_{max} & \quad\quad & & \forall (i,j) \in B \\[4mm]
& & x_i & \geq  \ 0 & && \forall i \in A \\
& & z_{ij} & \in \ \B & && \forall (i,j) \in B
\end{alignat*}

mit den Entscheidungsvariablen
- $y$: Endzeitpunkt der letzten Aufgabe
- $x_i$: Startzeitpunkt von Aufgabe $i$
- $z_{ij}=\left\{\begin{array}{rl} 1, &\text{ wenn Aufgabe }i\text{ vor Aufgabe }j\text{ ausgeführt wird}\\ 0, & \text{ sonst}. \end{array}\right.$ 

und dem Wert
\begin{align*}
d_{max}=\sum_{i \in A}d_i.
\end{align*}


%## Anwendung: Sudoku
% TODO
%In Vorlesung zusammen entwickeln, als Übung coden lassen (Notebook vervollständigen).

%## Anwendung: Studierende auf Projekte verteilen
% TODO
%AWP Notebook, enthält BigM
% Aufgabe dazu: https://colab.research.google.com/github/Gurobi/modeling-examples/blob/master/milp_tutorial/introduction_to_modeling.ipynb

%## Anwendung: EV Charger Placement
% TODO
%Musterlösung, enthält BigM
% Aufgabe dazu: https://colab.research.google.com/github/Gurobi/modeling-examples/blob/master/facility_location/facility_location.ipynb#scrollTo=8RUukodHFOMf

%## Anwendung: Payments
% als Hausaufgabe