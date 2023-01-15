# Fortgeschrittene Modellierungstechniken

Viele Echtweltprobleme zeichnen sich durch eine große Anzahl an zu modellierenden Aspekten aus.
Die Standardprobleme aus dem letzten Kapitel bilden bereits einen kleinen Fundus an Bausteinen für die Modellierung. 
Im Folgenden werden einige wiederkehrende Aspekte zusammen mit einer möglichen Lösung präsentiert.

## Maximumsfunktion als Teil der Zielfunktion
Die Zielfunktion linearer Programme besteht aus gewichteten Summen. In manchen Anwendungen benötigen wir eine Zielfunktion der Form
\begin{align*}
\min \max\{f_1(x_1, \ldots, x_n), f_2(x_1, \ldots, x_n), \ldots, f_d(x_1, \ldots, x_n)\}
\end{align*}
mit linearen Ausdrücken $f_1, f_2, \ldots, f_d$. Wie können wir diese Zielfunktion in der Form eines linearen Programms ausdrücken?
Wir führen dazu eine neue Variable $z \in \RR$ ein und modellieren
\begin{align*}
\min z
\end{align*}
unter den Nebenbedingungen
\begin{eqnarray*}
	f_1(x_1, \ldots, x_n) & \leq & z \\
	f_2(x_1, \ldots, x_n) & \leq & z \\
	\ldots \\
	f_d(x_1, \ldots, x_n) & \leq & z.
\end{eqnarray*}
Die Ungleichungen in den Nebenbedingungen übernehmen damit die Funktion des Maximums in der originalen Zielfunktion.


````{prf:example}
Ein Projektplanungsproblem besteht aus vier Arbeitsschritten. Als Entscheidungsvariablen  sind durch $s_1, s_2, s_3, s_4$ die Startzeiten jedes Arbeitsschrittes, durch $d_1, d_2, d_3, d_4$ die Dauer jedes Arbeitsschrittes gegeben. Alle anderen Zusammenhänge vernachlässigen wir in diesem Beispiel. Modellierungsziel ist die möglichst frühe Fertigstellung des Projekts. 

\Karos{33}{16}
````

## Logische Ausdrücke

(subsubsec:logikBeispiel)=
### Einführendes Beispiel
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


### Exkurs: Crash-Kurs Logik
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

#### Darstellung durch Konjunktion, Disjunktion und Negation
Grundsätzlich muss man nicht mit allen Junktoren gleichzeitig arbeiten und kann sich auch auf bestimmte Teilmengen beschränken. So kann man etwa durch Konjunktion, Disjunktion und Negation alle anderen Junktoren ausdrücken:
- Implikation $A \Rightarrow B$ entspricht $\lnot A \lor B$.
- Äquivalenz $A \Leftrightarrow B$ entspricht $(A \Rightarrow B) \land (B \Rightarrow A)$. Dies entspricht 
	$(\lnot A \lor B) \land (\lnot B \lor A)$.
- Exklusiv-Oder $\dot\lor$ entspricht $A \Leftrightarrow \lnot B$. Dies entspricht 
		$(\lnot A \lor \lnot B) \land (A \lor B)$.

````{prf:example}
TO DO
````

#### Rechenregeln für aussagenlogische Formeln
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


#### Die Konjunktive Normalform

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

### Modellierung der Junktoren als arithmetische Ausdrücke
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

### Transformation logischer Zusammenhänge in arithmetische Ausdrücke

Sind mehrere logische Formeln konjunktiv (also durch UND-Verknüpfungen) miteinander verbunden, so können die Formeln  eminzeln behandelt werden.

````{prf:example}
TO DO
````
Sind umfangreichere Formeln gegeben, so können diese über die Rechenregeln für aussagenlogische Formeln in die Konjunktion von bekannten durch arithmetische Ausdrücke modellierbaren Formeln zurückgeführt werden. 
Wir wandeln das einführende Beispiel aus Abschnitt {ref}`subsubsec:logikBeispiel` um:

````{prf:example}
TO DO
````


#### Allgemeines Vorgehen
Die in der Praxis auftretenden Formeln sind typischerweise einfach genug, dass keine komplizierten Umformungen vorgenommen werden müssen. Als allgemeines Verfahren für sehr komplizierte Ausdrücke kann man folgendes Verfahren nutzen: Schritt 1: Umwandlung der Formel in konjunktive Normalform. Schritt 2: Behandlung der einzelnen Klauseln nach der Methode "mindestens $1$ aus $k$".


## Logische Bedingungen für Nebenbedingungen
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

## Endliche Wertemenge für Entscheidungsvariablen
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
## Disjunktive Programmierung
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

### Groß-M Reformulierung
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

### Konvexe-Hülle Reformulierung
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


### Vergleich zwischen beiden Formulierungen
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


## Linearisieren von Nichtlinearitäten
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
