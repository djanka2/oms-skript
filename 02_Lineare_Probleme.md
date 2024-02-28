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

# Lineare Optimierung

Im ersten Teil dieser Vorlesung beschäftigen wird uns mit *linearen Optimierungsproblemen*, auch genannt *lineare Programme (LP)*. Dieses Kapitel bildet die Grundlage für die folgenden Kapitel {ref}`sec:integer-problems`, {ref}`sec:zeitdiskret` und {ref}`sec:practical-aspects`, in denen verschiedene Varianten und Aspekte dieser Probleme vorgestellt werden. 

## Grundbegriffe
Ein *lineares Programm* ist ein Optimierungsproblem, bei dem eine lineare Zielfunktion unter linearen Nebenbedingungen optimiert werden soll. Ein Beispiel für lineares Optimierungsproblem haben wir bereits in Abschnitt {ref}`sec:production-example` gesehen. Es lautete:

\begin{alignat}{5}
\max_{x_1, x_2} & \quad  &   2x_1+2x_2 & & & \\[2mm]
\text{s.t. } & &  5x_1+10x_2&\leq 50\\
             & &  12x_2+8x_2&\leq 72\\
             & &  4x_1+0x_2&\leq 20\\
             & &  x_1+x_2&\leq 30\\
             & & x_1, x_2 &\geq 0
\end{alignat}

Zur Erinnerung: *Linear* bedeutet, dass alle Variablen $x_i$ nur in einfacher Potenz (mit konstanten Koeffizienten) vorkommen dürfen, also Ausdrücke der Form $x_1+2x_2-7x_3$, aber keine Ausdrücke der Form $x_1^2$, $\sin x_2$, $1/x_1$ oder auch $x_1x_2$. Jede lineare Funktion $f:\R^n\rightarrow\R$ lässt sich darstellen als
\begin{align*}
f(\v x)=c_1x_1+\dots +c_nx_n=\sum_{i=1}^nc_ix_i=\v c^T\v x,
\end{align*}
wobei $c_1,\dots,c_n\in\R$ reelle Zahlen sind, die natürlich auch den Wert Null annehmen dürfen. Wir fassen sie im Vektor $\v c\in\R^n$ zusammen.

Als Nebenbedingungen sind Ungleichungen und Gleichungen der Art $\leq, \geq, =$ erlaubt. Nicht erlaubt und typischerweise auch nicht sinnvoll sind Ungleichungen der Art $<$ bzw $>$ (was sollte z.B. die kleinste Zahl $x>0$, also die Lösung des LPs $\min_{x} x\quad \text{s.t. } x>0$ sein?).

Durch die lineare Struktur kann man die Koeffizienten der Variablen in den Ungleichungen in einer Matrix zusammenfassen, deren Spalten der Anzahl der Variablen und deren Zeilen der Anzahl der Nebenbedingungen entspricht.

````{prf:definition} Lineares Programm in allgemeiner Form

Gegeben sei eine $m \times n$-Matrix $\m A=(a_{ij})$, ein $m$-dimensionaler Vektor $\v b$, sowie ein $n$-dimensionaler Vektor $\v c$. Ein *lineares Programm (LP)* ist ein Optimierungsproblem der Form
\begin{alignat*}{5}
\min_{\v x} / \max_{\v x}          & \quad  &   c_1x_1 + \ldots + c_nx_n &          & & \\[2mm]
\text{s.t. } & &  a_{i1}x_1 + \ldots + a_{in}x_n & = & \ b_i & \quad\quad & & \forall i= 1, \ldots, p \\
& &  a_{i1}x_1 + \ldots + a_{in}x_n & \leq & \ b_i & \quad\quad & & \forall i= p+1, \ldots, q \\
& &  a_{i1}x_1 + \ldots + a_{in}x_n & \geq & \ b_i & \quad\quad & & \forall i= q+1, \ldots, m \\
& & x_j & \geq & \ 0 & && \forall j= 1, \ldots, n.
\end{alignat*}
````

Es müssen dabei nicht alle möglichen Arten von Nebenbedingungen ($\leq, =, \geq, \geq 0$) vorkommen. Die genaue Form eines beliebigen LP ergibt sich normalerweise aus der Modellierung der Anwendung wie etwa bei unserem Produktionsbeispiel. Die Form wird dabei meist so gewählt, dass sie möglichst gut verständlich ist. Wenn man Aussagen über beliebige, allgemeine LPs treffen möchte (z.B. bei der Beschreibung von Lösungsverfahren, die für alle möglichen LPs funktionieren sollen), benutzt man gerne lineare Programme in der sogenannten *Standardform*.

````{prf:definition} Lineares Programm in Standardform
:label: def:LP
Gegeben sei eine $m \times n$-Matrix $A$, ein $m$-dimensionaler Vektor $b$, sowie ein $n$-dimensionaler Vektor $c$. Ein *lineares Programm (LP)* ist ein Optimierungsproblem der Form
\begin{alignat*}{5}
\min_{\v x}          & \quad  &   c_1x_1 + \ldots + c_nx_n &          & & \\[2mm]
\text{s.t. } & &  a_{i1}x_1 + \ldots + a_{in}x_n & = & \ b_i & \quad\quad & & \forall i= 1, \ldots, m \\
& & x_j & \geq & \ 0 & && \forall j= 1, \ldots, n.
\end{alignat*}
In Matrixform

\begin{alignat*}{5}
\min_{\v x}          & \quad  &   \v c^T\v x &          & & \\[2mm]
\text{s.t. } & &  \m A\v x & = & \v b & \\
& & \v x & \geq & \ \v 0 & &&
\end{alignat*}
````

## Standardumformungen
Wie bringt man nun ein *beliebiges* Lineares Programm in Standardform? 

<!-- Wir gehen als Zwischenschritt einen etwas umständlichen Weg, der sich später als praktisch und einfacher zu verstehen erweist. Wir bringen dazu das LP erst in eine Form, bei der ein Minimierungsproblem vorliegt, alle Variablen nicht-negativ sind und nur Nebenbedingungen der Form $\leq$ vorliegen: 

\begin{alignat*}{5}
\min_{x_1, \ldots, x_p} &\quad & \sum_{j=1}^{n}c_j x_j \\[2mm]
\text{s.t. } & &\sum_{j=1}^{n} a_{ij} x_j &\leq&  \ b_i & \quad\quad & & \forall i=1,\ldots,m \\
             & & x_j                      &\geq&  0 &  && \forall j =1 ,\ldots ,n
\end{alignat*}

Danach bringen wir es in Standardform. -->

Wir starten mit einem beliebigen linearen Problem, das nicht in Standardform vorliegt.
Es enthält beliebig viele Gleichungen, $\leq$-Ungleichungen und $\geq$-Ungleichungen mit beliebigen Koeffizienten $a_{ij}, i=1,\dots,m, j=1,\dots,n$:
\begin{alignat*}{5}
\max_{x_1, \ldots, x_p} &\quad & \sum_{j=1}^{n}c_j x_j \\[2mm]
\text{s.t. } & &\sum_{j=1}^{n} a_{ij} x_j &\leq&  \ b_i & \quad\quad & & \forall i=1,\ldots,m_1 \\
             & &\sum_{j=1}^{n} a_{ij} x_j &\geq&  \ b_i & \quad\quad & & \forall i=m_1+1,\ldots,m_2 \\
             & &\sum_{j=1}^{n} a_{ij} x_j &=&  \ b_i & \quad\quad & & \forall i=m_2+1,\ldots,m \\
\end{alignat*}

````{prf:example} LP, welches nicht in Standardform vorliegt
\begin{alignat}{5}
\max_{x_1, x_2} & \quad  &  2x_1-3x_2 & & & \\[2mm]
\text{s.t. } & &  3x_1+x_2&\leq 3\\
             & &  -x_1+5x_2&\geq 7\\
             & &  x_1+x_2&= 1\\
             & & x_1&\geq 0
\end{alignat}
````

Wir wandeln das LP nun in vier Schritten in ein neues LP um:
1. Transformation der Zielfunktion
2. Transformation von $\geq$-Ungleichungsnebenbedingungen
3. Transformation auf nichtnegative Variablen
4. Transformation auf Gleichungsbedingungen

Schritt 1
: Falls ein Maximierungsproblem vorliegt, wandeln wir es in ein Minimierungsproblem um, indem wir die Zielfunktion
: \begin{align*}
\max \sum_{j=1}^{n}c_j x_j 
\end{align*}
: durch
: \begin{align*}
\min \sum_{j=1}^{n}-c_j x_j
\end{align*} 
: ersetzen.
````{prf:example} Transformation der Zielfunktion
\begin{alignat*}{5}
\red{\min_{x_1, x_2}} & \quad  &  \red{-2x_1+3x_2} & & & \\[2mm]
\text{s.t. } & &  3x_1+x_2&\leq 3\\
             & &  -x_1+5x_2&\geq 7\\
             & &  x_1+x_2&= 1\\
             & & x_1&\geq 0
\end{alignat*}
````

    
Schritt 2
: Nebenbedingungen der $\geq$-Form 
: \begin{align*}
\sum_{j=1}^{n} a_{ij} x_j \geq b_i
\end{align*}
: multiplizieren wir mit $-1$ durch und erhalten 
\begin{align*}
\sum_{j=1}^{n} -a_{ij} x_j \leq -b_i
\end{align*}
````{prf:example} Transformation der $\geq$-Ungleichungen
\begin{alignat*}{5}
\min_{x_1, x_2} & \quad  &  -2x_1+3x_2 & & & \\[2mm]
\text{s.t. } & &  3x_1+x_2&\leq 3\\
             & &  \red{x_1-5x_2}&\red{\leq -7}\\
             & &  x_1+x_2&= 1\\
             & & x_1&\geq 0
\end{alignat*}
````
    
Schritt 3
: Für jede Variable $x_i$, die negativ werden kann, fügen wir zwei neue Variablen $x_i^+$ und $x_i^-$ mit den Nichtnegativitätsbedingungen 
: \begin{align*}
x_i^+\geq 0\\
x_i^-\geq 0
\end{align*}
: ein. Nun ersetzen wir jedes Vorkommen von $x_i$ durch $(x_i^+-x_i^-)$
````{prf:example} Transformation auf nichtnegative Variablen
\begin{alignat*}{5}
\min_{x_1, \red{x_2^+, x_2^-}} & \quad  &  -2x_1+\red{3x_2^+-3x_2^-} & & & \\[2mm]
\text{s.t. } & &  3x_1+\red{x_2^+-x_2^-}&\leq 3\\
             & &  x_1-\red{5x_2^+-5x_2^-}&\red{\leq -7}\\
             & &  x_1+\red{x_2^+-x_2^-}&= 1\\
             & & x_1,\red{x_2^+,x_2^-}&\geq 0
\end{alignat*}
````

Schritt 4
: Um das Problem in Standardform zu bringen, müssen wir die Nebenbedingungen von der $\leq$-Form in die $=$-Form bringen. Dies lässt sich durch das Hinzufügen von neuen Variablen, sogenannten *Schlupfvariablen* $x_{n+1},\ldots,x_{n+m_2}$  erreichen:
: \begin{align*}
\begin{array}{llllll}
a_{11} x_1+\ldots +a_{1n} x_n	& \red{+x_{n+1}} & &  &   & =b_1\\ 
a_{21} x_1+\ldots +a_{2n} x_n	&  & \red{+x_{n+2}} & &   & =b_2\\
\vdots & & & \ddots & & \vdots\\
a_{m1} x_1+\ldots +a_{mp} x_n	&  & &&  \red{+x_{n+m_2}} & =b_m\\  
\end{array} 
\end{align*}

Auf unser Beispiel übertragen ergibt dies
````{prf:example} Transformation auf Gleichungsnebenbedingung
Transformation auf nichtnegative Variablen
\begin{alignat*}{5}
\min_{x_1, x_2^+, x_2^-, \red{x_3, x_4}} & \quad  &  -2x_1+\red{3x_2^+-3x_2^-} & & & \\[2mm]
\text{s.t. } & &  3x_1+x_2^+-x_2^-\red{+x_3}&\red{=} 3\\
             & &  x_1-5x_2^+-5x_2^-\red{+x_4}&\red{=} -7\\
             & &  x_1+x_2^+-x_2^-&= 1\\
             & & x_1,x_2^+,x_2^-,\red{x_3,x_4}&\geq 0
\end{alignat*}
````

Damit ist das LP in Standardform. In Matrixform schreiben wir
````{prf:example}
\begin{alignat}{5}
\min_{x_1, x_2^+, x_2^-, x_3, x_4} & \quad  &  \bmat -2,&3,&-3,&0,&0 \emat\bmat x_1\\x_2^+\\x_2^-\\x_3\\x_4\emat & & & \\[2mm]
\text{s.t. } & &  \bmat 3&1&-1&1&0\\ 1&-5&5&0&1\\ 1&1&-1&0&0 \emat\bmat x_1\\x_2^+\\x_2^-\\x_3\\x_4\emat&=\bmat 3\\-7\\1\emat\\
             & & (x_1,x_2^+,x_2^-,x_3,x_4)&\geq 0
\end{alignat}
````

## Lösbarkeit von Linearen Programmen

Wir wiederholen nun die Grundbegriffe aus Abschnitt {ref}`sec:grundbegriffe` speziell für den Fall beliebiger linearer Probleme. Streng genommen sind diese natürlich durch die Definitionen im Abschnitt {ref}`sec:grundbegriffe` mit abgedeckt, aber etwas Wiederholung schadet an dieser Stelle nicht.

Wir nennen jedes $x$, das alle Nebenbedingungen erfüllt, eine *zulässige Lösung* des linearen Problems.

````{prf:definition} Zulässige Lösung eines LP
Gegeben ist ein Lineares Programm LP: $\min  c^Tx$ unter den Nebenbedingungen $\m A\v x=\v b$ und $\v x\geq \v 0$. 
Es heißt
\begin{align*}
P=\{\v x \in \R^n \mid Ax=b, \ \v x\geq \v 0\}
\end{align*}
die *Menge aller zulässigen Lösungen* von LP.
````

Eine zulässige Lösung heißt *optimal*, wenn es keine andere zulässige Lösung mit einem besseren Zielfunktionswert gibt.

````{prf:definition} Optimale Lösung eines LP
Gegeben ist ein lineares Programm LP: $\min  c^Tx$ unter den Nebenbedingungen $\m A\v x=\v b$ und $\v x\geq \v 0$. 
Es sei $P$ die Menge der zulässigen Lösungen von LP. Es heißt $x^*\in P$ *optimal* für LP, wenn für alle $\v x' \in P$ gilt, dass $\v c^T\v x^* \leq \v c^T\v x'$.
````

Ein lineares Problem heißt *unbeschränkt*, wenn es für jeden Wert $k$ eine zulässige Lösung mit Zielfunktionswert gibt, der besser als $k$ ist. Man kann also "beliebig gut werden".

````{prf:definition} Unbeschränktes Lineares Programm
Gegeben ist ein lineares Programm LP: $\min  \v c^T\v x$ unter den Nebenbedingungen $\m A\v x=\v b$ und $\v x\geq \v 0$. 
Es sei $P$ die Menge der zulässigen Lösungen von LP. LP heißt *unbeschränkt*, wenn es für alle $k \in \R$ ein $\v x \in P$ gibt, so dass $\v c^T\v x \leq k$.
````

Für jedes lineare Programm LP trifft genau eine der folgenden Möglichkeiten zu:
1. LP besitzt (mindestens) eine optimale Lösung.
2. LP besitzt keine zulässige Lösung.
3. LP ist unbeschränkt.


## Grafisches Lösen
Wir betrachten noch einmal das Produktionsbeispiel {eq}`eq:prodopt`:
\begin{alignat}{5}
\max_{x_1, x_2} & \quad  &   2x_1+2x_2 & & & \\[2mm]
\text{s.t. } & &  5x_1+10x_2&\leq 50\\
             & &  12x_2+8x_2&\leq 72\\
             & &  4x_1+0x_2&\leq 20\\
             & &  x_1+x_2&\leq 30\\
             & & x_1, x_2 &\geq 0
\end{alignat}
Im vorigen Kapitel haben wir die Lösung angegeben: $x_1^{\star}=4, x_2^{\star}=3$. Wir wollen uns nun anschauen, wie man auf diese Lösung kommt. Dazu stellen wir uns den Variablenvektor $\v x=\bmat x_1\\x_2\emat$ als Punkt im zweidimensionalen Raum, also der Ebene, vor. Jede der Nebenbedingungen teilt den $\R^2$ in zwei Bereiche: einen Bereich, in dem alle Punkte liegen, die diese Nebenbedingung erfüllen und einen Bereich, in dem alle Punkte liegen, die sie nicht erfüllen. Die Trennlinie dieser Bereiche -- man nennt sie auch *Halbräume* -- ist die Gerade, die durch Gleichsetzen der linken und rechten Seite der Ungleichung entsteht. Dies kann man nun für jede der Ungleichungen machen. Dort, wo sich die Bereiche überlagern, liegen die zulässigen Punkte des Problems.

```{figure} ./bilder/prodopt-feasible.png
:name: fig:feasible-set
:width: 400px

Nebenbedingungen (orange Linien) und die resultierende zulässige Menge (in blau) des Produktionsoptimierungsbeispiel {eq:prodopt}. Die Nebenbedingung $x_1+x_2\leq 30$ ist hier nicht eingezeichnet, da sie auf die zulässige Menge keinen Einfluss hat.
```
Doch welcher der zulässigen Punkte ist ein optimaler Punkt? Dazu betrachten wir eine sog. *Höhenlinie* der Zielfunktion. Die Höhenlinie zu einem Wert $\beta\in\R$ ist eine Gerade entlang derer die Zielfunktion den konstanten Wert $\beta$ annimmt. Im Bild ist z.B. die Höhenlinie zum Niveau $\beta=8$ eingezeichnet, was bedeutet, dass alle Punkte auf der Linie den Zielfunktionswert 8 haben. Wenn wir die Höhenlinie parallel in Pfeilrichtung verschieben -- das ist übrigens die Richtung $\v c=\bmat 2\\2\emat$, der Vektor, der die Zielfunktion definiert! -- verbessert sich die Zielfunktion. Dies tun wir nun so lange, bis wir die zulässige Menge gerade so noch berühren. Dieser letzte Berührungspunkt zwischen Höhenlinie und zulässiger Menge ist ein Optimalpunkt des Problems. 

```{figure} ./bilder/prodopt-feasible-opt.png
:name: fig:feasible-opt
:width: 450px

Höhenlinie und Verschiebung der Höhenlinie bis zum optimalen Punkt.
```

Wir beobachten, dass der Optimalpunkt in diesem Beispiel in einer Ecke der zulässigen Menge liegt. 
Dies ist tatsächlich nicht nur in diesem Beispiel so, sondern immer, d.h. für jedes beliebige LP. Diese Tatsache ist sehr wichtig, da sie die Grundlage für Lösungsverfahren von LPs bildet. Im nächsten Abschnitt beschreiben wir diese Eigenschaft von LPs etwas formaler.

(subsec:polyeder)=
## Der Polyeder der zulässigen Lösungen
Jede Gleichung der Form 
\begin{align*} \sum_{j=1}^{n} a_{ij} x_j = b_i \end{align*}
unterteilt den Raum $\R^n$ in zwei *Halbräume*
$\sum_{j=1}^{n} a_{ij} x_j \leq b_i$ und
$\sum_{j=1}^{n} a_{ij} x_j \geq  b_i$.


```{figure} ./bilder/halbraeume.png
:name: fig:halbraeume
:width: 400px

Zwei Halbräume, die durch die Gleichung $x_2=\frac{1}{2}x_1+1$ definiert sind.
```

Die Schnittmenge von (endlich vielen) Halbräumen nennt man einen *Polyeder*.

````{prf:definition} Polyeder
Ein *Polyeder* $P \subseteq \R^n$ ist eine Punktmenge, die eine endliche Zahl an linearen Ungleichungen erfüllt, d.h. die durch die Form 

\begin{align*}
P=\{\v x \in \R^n \mid \m A\v x \leq \v b\}
\end{align*}

darstellbar ist für eine $m \times n$ Matrix $\m A$ und einen $m$-dimensionalen Vektor $\v b$.
````

Polyeder und lineare Optimierungsprobleme haben eine enge Verbindung, da die zulässige Menge eines linearen Programms immer als ein Polyeder aufgefasst werden kann. Das liegt daran, dass man die Menge der zulässigen Punkte auch ausschließlich durch *Un*gleichungen beschreiben kann (womit sie die Polyeder-Definition erfüllen). In unserer Standardformulierung {prf:ref}`def:LP` haben wir eigentlich festgehalten, dass ein LP beliebig viele Gleichungen der Form
\begin{align*}
\sum_{j=1}^{n} a_{ij} x_j  =  b_i
\end{align*}
enthalten kann. Nun kann man aber offenbar jede solche Gleichung durch die beiden Ungleichungen
\begin{align*}
\sum_{j=1}^{n} a_{ij} x_j  &\leq  b_i
\sum_{j=1}^{n} a_{ij} x_j  &\geq  b_i
\end{align*}
ersetzen und erhält damit ein äquivalentes LP, welches ausschließlich Ungleichungen als Nebenbedingung hat. Die Menge der Punkte, die alle Ungleichungen erfüllen, bilden den *Polyeder der zulässigen Lösungen*.

Ein Punkt $\v x \in P$ in einem Polyeder $P$ heißt *Ecke*, wenn er nicht in der Mitte von zwei anderen Punkten aus $P$ liegt. Mathematisch exakt drückt man das wie folgt aus

```{figure} ./bilder/ecken.png
:name: fig:ecken
:width: 400px

Ein Polyeder mit fünf Ecken $e_1,e_2,e_3,e_4,e_5$.
```

````{prf:definition} Ecke
Ein Punkt $\v x \in P$ in einem Polyeder $P$ heißt *Ecke* von $P$, falls es keine zwei Punkte $\v x^1, \v x^2 \in P$ gibt mit $\v x^1\not=\v x^2$, so dass $\v x=\frac{1}{2}\v x^1+\frac{1}{2}\v x^2$ gilt.
````

Eine Menge $T \subseteq \R^n$ heißt *konvex*, wenn für jedes Punktepaar $\v x^1, \v x^2 \in T$ auch die komplette Verbindungslinie zwischen $\v x^1$ und $\v x^2$ in der Menge $T$ liegt. Polyeder sind konvexe Mengen (Umgekehrt kann eine nichtkonvexe Menge kein Polyeder sein).

```{figure} ./bilder/konvexe_menge.png
:name: fig:konvexe-mengen
:width: 400px

Beispiele konvexer und nicht konvexer Mengen.
```

````{prf:definition} Konvexität
Eine Menge $T \subseteq \R^n$ heißt *konvex*, falls aus $\v x^1 \in T$ und $\v x^2 \in T$ folgt, dass $\lambda \v x^1 + (1-\lambda) \v x^2 \in T$ gilt.
````
Konvexität ist in der Optimierung eine sehr starke und wünschenswerte Eigenschaft und wird uns im Laufe der Vorlesung noch öfter begegnen.

````{prf:theorem}
:label: thm:ecken
Besitzt ein lineares Programm eine optimale Lösung, so besitzt es auch mindestens eine optimale Lösung, die eine Ecke im zugehörigen Lösungspolyeder ist.
````

```{figure} ./bilder/ecke-loesung.png
:name: fig:ecke-loesung
:width: 500px

Optimallösungen im Polyeder.
```

## Lösungsmethoden für LPs
Zur Lösung allgemeiner LPs der Form {prf:ref}`def:LP` gibt es im wesentlichen zwei Ansätze, die in der Praxis verwendet werden. In diesem Abschnitt erklären wir kurz die Ideen dieser beiden Ansätze. Auf Details verzichten wir an dieser Stelle, da mittlerweile für beide Ansätze sehr gute Software verfügbar ist, die in (zumindest für viele Probleme) als black box verwendet kann.

### Simplex-Verfahren
Das Simplex Verfahren wurde 1947 von George Dantzig entwickelt, einem der wichtigsten Menschen im Bereich der mathematischen Optimierung (er entwickelte es im Rahmen einer Planungsaufgabe für das US Militär). In dem Verfahrens wird ausgenutzt, dass sich eine Lösung des LPs stets in einer Ecke des Polyeders der zulässigen Punkte befindet (siehe {prf:ref}`thm:ecken`). Das Verfahren iteriert über die Ecken des Polyeders und prüft an jeder Ecke, ob es sich um eine optimale Lösung handelt. Wichtig: Man muss für dieses "Prüfen" auf Optimalität nicht *alle* Ecken besuchen, sondern man kann es einer Ecke "ansehen", ob es sich um eine optimale handelt (durch Überprüfung gewisser mathematischer Bedingungen).
Warum ist das wichtig? Die Anzahl der Ecken des Polyeders der zulässigen Lösungen kann überraschend groß sein. So hat ein $n$-dimensionaler Einheitswürfel, also die Menge $C=\{\v x\in\R^n \mid 0\leq x_i\leq 1, i=1,\dots,n\}$ $2^n$ Ecken. Ein Quadrat im $\R^2$ hat $2^2=4$ Ecken, ein Würfel im $\R^3$ hat $2^3=8$ Ecken. Wenn man ein LP auf 500 Variablen betrachtet, beträgt die Anzahl der Ecken $2^{500}\approx 3\cdot 10^{150}$. Zum Vergleich: man geht davon aus, dass es im gesamten Universum etwa $10^{80}$ Atome gibt.
Um so erstaunlicher ist es, dass moderne Varianten des Simplex-Verfahrens Probleminstanzen mit hunderttausenden Variablen und Constraints oft innerhalb Sekunden auf einem Standardlaptop lösen können.

Die exakte Laufzeit vorherzusehen, ist allerdings schwierig und in der Tat hat das Simplex-Verfahren im worst-case exponentielle Laufzeit. So wurde in den 1970er Jahren ein Beispiel konstruiert, der sogenannte Klee-Minty-Würfel, bei denen Simplex-Verfahren eben doch alle Ecken besuchen würden. 

Um eine Vorstellung von der Komplexität zu bekommen: Hätte Dantzig 1947 sein Simplex-Verfahren für ein Klee-Minty-Würfel mit 500 Variablen auf einem Rechner gestartet, der pro Sekunde eine Billiarde ($10^15$) Ecken überprüft und bis heute ununterbrochen läuft, so hätte er heute nicht einmal $10^{25}$ Ecken überprüft, also gerade mal etwa $10^{-123}=0.00000\dots001\%$ der Ecken des Polytops.

In der Praxis treten solche Worst-Case Probleme allerdings eher nicht auf und das Simplex-Verfahren ist ein robustes und schnelles Verfahren für lineare Programme.  


### Innere-Punkte-Verfahren
Neben Simplex-Verfahren gibt es eine weiter Klasse von Verfahren, die eine andere Lösungsstrategie verfolgt, sogenannte *Innere-Punkte-Verfahren*. Wie der Name schon sagt, besteht die Idee darin, im Inneren des Polyeders zu starten und iterativ zu versuchen, sich der optimalen Ecken approximativ zu nähern. Aktuelle Löser starten in der Regel beide Typen von Verfahren gleichzeitig (auf unterschiedlichen Kernen), da keines der Verfahren dem anderen auf allen Probleminstanzen überlegen ist. Der Lösungslauf endet, sobald eines der Verfahren das LP gelöst hat.


## Software
Für allgemeines lineare Programme existieren heutzutage ausgereifte Softwarepakete, die Instanzen mit hundertausenden Variablen und Nebenbedingungen innerhalb von Sekunden auf Standardlaptops lösen können (dies hängt natürlich von der konkreten Probleminstanz ab). Der schnellste Löser ist [Gurobi](https://www.gurobi.com/) (nach den Erfindern Gu, Rothberg und Bixby). Dieser ist proprietär, aber für den akademischen Gebrauch ist die Lizenz immerhin kostenlos. Weitere kommerzielle Löser sind CPLEX, Mosek und FICO Xpress.

Daneben gibt es frei erhältliche Software wie [CLP](https://github.com/coin-or/Clp) oder [SoPlex](https://soplex.zib.de/) (bzw. [CBC](https://github.com/coin-or/Cbc) und [SCIP](https://scipopt.org/), falls auch Ganzzahligkeitsbedingungen betrachtet werden sollen). Besonders für große und schwierige Instanzen mit Ganzzahligkeitsbedingungen sind die kommerziellen Löser den freien allerdings z.T. deutlich überlegen.

Gurobi z.B. bietet eine eigene Python Schnittstelle zur einfachen Modellierung von Problemen. Des weiteren existieren Modellierungsbibliotheken wie [PuLP](https://coin-or.github.io/pulp/) oder [Python-MIP](https://www.python-mip.com/), mit denen ein Problem formuliert werden kann, welches dann an einen Löser nach Wahl (u.a. Gurobi, CLP) übergeben wird.

Wir benutzen in dieser Vorlesung das Python-Interface von Gurobi. Der folgende Code erstellt zuerst das Modell, ruft dann Gurobi auf und gibt schließlich die berechnete Lösung aus.

```{code-cell} ipython3
:tags: []

import gurobipy as gp
from gurobipy import GRB
import numpy as np
```

Formulierung in mathematischer Form

\begin{alignat}{5}
\max_{x_1, x_2} & \quad  &   2x_1+2x_2 & & & \\[2mm]
\text{s.t. } & &  5x_1+10x_2&\leq 50\\
             & &  12x_1+8x_2&\leq 72\\
             & &  4x_1+0x_2&\leq 20\\
             & &  x_1+x_2&\leq 30\\
             & & x_1, x_2 &\geq 0
\end{alignat}

Zuerst erzeugen wir ein leeres Modell:

```{code-cell} ipython3
:tags: []
m = gp.Model("Production Optimization")
```

Danach können wir einzelne Variablen anlegen. Als Parameter geben wir an
* Den Namen mit "name="
* Den Variablentyp mit "vtype=". Es gibt folgende Möglichkeiten
  * GRB.CONTINUOUS 
  * GRB.BINARY
  * GRB.INTEGER
* Die untere Schranke für die Variable mit "lb=". Falls nichts angegeben wird, ist die Variable automatisch nichtnegativ. Falls die Variable nach unten unbeschränkt sein soll, können wir "lb=-np.infty" spezifizieren.

```{code-cell} ipython3
:tags: []

x1 = m.addVar(name="x1", vtype=GRB.CONTINUOUS, lb=0)
x2 = m.addVar(name="x2", vtype=GRB.CONTINUOUS, lb=0)
```

Einzelne Nebenbedinungen können wir dann direkt mit dem Befehl addConstr angeben.

```{code-cell} ipython3
:tags: []
m.addConstr(5*x1+10*x2 <= 50)
m.addConstr(12*x1+8*x2 <= 72)
m.addConstr(4*x1 <= 20)
m.addConstr(x1+x2 <= 30)
#m.addConstr(x1 >= 0) # nicht nötig, da bereits über den Parameter lb=0 beim Anlegen der Variable spezifiziert
#m.addConstr(x2 >= 0)
```

Danach folgt die Zielfunktion:

```{code-cell} ipython3
m.setObjective(2*x1+2*x2, GRB.MAXIMIZE)
```

Nun starten wir den Solver.

```{code-cell} ipython3
:tags: []
m.optimize()
```

Die Lösung können wir wie folgt auslesen:

```{code-cell} ipython3
print(f"x1={x1.x}, x2={x2.x}")
```
(subsubsec:tricks1)=
## Modellierungstricks I

(subsubsec:minmax)=
### Maximumsfunktion als Teil der Zielfunktion

````{prf:example} Min Max
Ein Projektplanungsproblem besteht aus vier Arbeitsschritten. Als Entscheidungsvariablen sind durch $s_1, s_2, s_3, s_4$ die Startzeiten jedes Arbeitsschrittes, durch $d_1, d_2, d_3, d_4$ die Dauer jedes Arbeitsschrittes gegeben. Alle anderen Zusammenhänge vernachlässigen wir in diesem Beispiel. Modellierungsziel ist die möglichst frühe Fertigstellung des Projekts. 

Die Endzeiten der einzelnen Arbeitsschritte sind gegeben durch $s_1+d_1, s_2+d_2, s_3+d_3, s_4+d_4$. Die letzte (größte) dieser Zeiten soll möglichst klein werden. Mathematisch drückt man das so aus:

```{math}
:label: eq:minmax
\begin{align*}
\min \max \{s_1+d_1, s_2+d_2, s_3+d_3, s_4+d_4\}
\end{align*}
```

```{figure} ./bilder/minmax.png
:width: 400px
```
Löser für lineare Programme können mit diesen $\min\max$ meist nicht direkt umgehen. Wie kann man das $\min\max$-Problem in ein reines Minimierungsproblem von der Form {prf:ref}`def:LP` überführen?
````

Die Zielfunktion linearer Programme besteht immer aus einer gewichteten Summen der Variablen. In manchen Anwendungen benötigen wir eine Zielfunktion der Form
\begin{align*}
\min \max\{f_1(x_1, \ldots, x_n), f_2(x_1, \ldots, x_n), \ldots, f_d(x_1, \ldots, x_n)\}
\end{align*}
mit linearen Ausdrücken $f_1, f_2, \ldots, f_d$. Wie können wir diese Zielfunktion in der Form eines linearen Programms ausdrücken?
Wir führen dazu eine neue Variable $z \in \R$ ein und modellieren
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
Sie garantieren, dass $z$ größer oder gleich *jeder* der Funktionen $f_i$ ist. Gleichzeitig soll $z$ aber minimiert werden, dadurch wird es auf das Maximum der $f_i$ "gedrückt". Ähnlich können übrigens auch $\max \min$ Probleme reformuliert werden. Bei Problemen der Form $\max \max$ oder $\min \min$ gestaltet sich die Sache schwieriger (mehr dazu im nächsten Kapitel).

%max min als Übung?
  
````{prf:example} Min Max (Forsetzung)
Wir führen eine neue Variable $y$ und 4 Nebenbedingungen ein. Der zur $\min\max$-Formulierung {eq}`eq:minmax` äquivalente Teile eines linearen Programms lautet:

\begin{alignat}{5}
\min_{s_1,d_1,s_2,d_2,s_3,d_3,s_4,d_4,y} & \quad  &   y & & & \\[2mm]
\text{s.t. } & &  s_1+d_1&\leq y\\
             & &  s_2+d_2&\leq y\\
             & &  s_3+d_3&\leq y\\
             & &  s_4+d_4&\leq y
\end{alignat}
````

(subsubsec:betraege)=
### Beträge
Die Betragsfunktion ist definiert als
\begin{align*}
f(x)=|x|=\left\{ \begin{array}{lr} 
                x, & \text{ falls }x\geq0\\
                -x, & \text{ falls }x<0
                \end{array}
\right.
\end{align*}
Beträge sind bei vielen Modellen hilfreich, wenn z.B. der Abstand zwischen zwei Variablen betrachtet werden soll, aber nicht klar ist, welche von beiden Variablen die größere ist. Ähnlich wie bei $\min \max$-Problemen muss man auch die Betragsfunktion umformulieren, so dass das Problem von der Form {prf:ref}`def:LP` ist und an einen Löser übergeben werden kann.

Eine erste Beobachtung ist die Tatsache, dass der Betrag einer Zahl gerade dem Maximum der Zahl und ihres negativen Wertes entspricht, in Formeln:
\begin{align*}
f(x)=|x|=\max\{x,-x\}
\end{align*}

Damit können wir ähnlich vorgehen wie im vorherigen Abschnitt. Folgende Bedingungen sind äquivalent:
\begin{align*}
|x|\leq 2 \Leftrightarrow \max\{x,-x\}\leq 2 \Leftrightarrow x\leq 2, -x\leq 2
\end{align*}

Funktioniert das auch bei Ungleichungen der Form $|x|\geq2$? Leider nicht, da $|x|\geq 2$ bedeutet, dass entweder $x\leq -2$ oder $x\geq 2$ gelten muss. Die zulässige Menge dieser "Entweder-Oder-Aussage" ist nicht konvex; sie hat ein Loch zwischen $-2$ und $2$. Wir hatten aber im vorherigen Abschnitt festgestellt, dass sich die zulässige Menge eines LP als Polyeder darstellen lässt und Polyeder konvex sind. Daher kann die Menge $|x|\geq2$ nicht die zulässige Menge eines LP sein. Wie man Bedingungen dieser Art mit Hilfe binärer Variablen modellieren kann, erfahren Sie im nächsten Kapitel.

Wir halten fest:
````{prf:remark}
Die Bedingung $|x|\leq \alpha$ ist äquivalent zu den beiden Bedingungen $x\leq\alpha$ und $-x\leq \alpha$.
````

Falls Beträge in der Zielfunktion eines *Minimierungs*problems auftauchen, so kann man sie ebenfalls umformulieren. Beispiel:
\begin{align*}
\min_{x\in\R} |x+2|
\end{align*}
lässt sich über folgende Schritte in ein äquivalentes LP umwandeln:
\begin{align*}
\min_{x\in\R} |x+2| &\Leftrightarrow \min_{(x,\alpha)\in\R^2} \alpha \quad \text{s.t. } |x+2|\leq \alpha\\
&\Leftrightarrow \min_{(x,\alpha)\in\R^2} \alpha \quad \text{s.t. } x+2\leq \alpha, -(x+2)\leq \alpha
\end{align*}

Das lässt sich verallgemeinern, wenn die Summe von mehreren Beträgen minimiert werden soll. In diesem Fall muss jeder Summand durch zwei Ungleichungsnebenbedingungen aufgelöst werden. Beispiel: Das Problem
\begin{align*}
\min_{(x_1,x_2)\in\R} |x_1+2|+|2x_2|
\end{align*}
wird zunächst umformuliert zu
\begin{align*}
\min_{(x_1,x_2,\alpha_1,\alpha_2)\in\R^4} \alpha_1+\alpha_2 \quad \text{s.t. } |x_1+2|\leq \alpha_1, |2x_2|\leq\alpha_2
\end{align*}
und im nächsten Schritt zu
\begin{align*}
\min_{(x_1,x_2,\alpha_1,\alpha_2)\in\R^4} \alpha_1+\alpha_2 \quad \text{s.t. } \quad &x_1+2\leq \alpha_1,\quad -(x_1+2)\leq \alpha_1\\ 
                                                              &2x_2\leq\alpha_2,\quad -2x_2\leq \alpha_2
\end{align*}
Achtung: Das funktioniert nur, wenn die Koeffizienten der Beträge in der Zielfunktion nicht negativ sind. Formal:
````{prf:theorem}
Das Optimierungsproblem 
\begin{align*}
\min_{\v x\in\R^n}\sum_{i=1}^N\lambda_i |f_i(\v x)|
\end{align*}
ist äquivalent zum Problem
\begin{align*}
\min_{\v x\in\R^n, \v \alpha \in\R^N}\sum_{i=1}^N\lambda_i \alpha_i \quad \text{s.t. }\quad f_i(\v x)&\leq\alpha_i,\quad -f_i(\v x)\leq\alpha_i, i\in\{1,\dots,N\}
\end{align*}
für Funktionen $f_1,\dots,f_N$ und *nichtnegative* Zahlen $\lambda_1,\dots,\lambda_N$.
````