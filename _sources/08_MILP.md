Das Thema dieses Vorlesungsteils ist das Modellieren und Lösen von Problemen aus der Unternehmenspraxis durch *gemischt-ganzzahlige lineare Programme*. Ziel ist gleichermaßen die Vermittlung der theoretischen Grundlagen als auch der nötigen Praxisaspekte. Dieser Teil des Skriptes wurde größtenteils übernommen von Prof. Dr. Reinhard Bauer (Fakultät W).

Die Vorlesung orientiert sich an den Büchern
- J. Kallrath: *Gemischt-ganzzahlige Optimierung in der Praxis*, Springer Spektrum, 2013.
- H. P. Williams: *Model Building in Mathematical Programming, 5th Edition*, Wiley, 2013.
- K. G. Murty: *Case Studies in Operations Research*, Springer, 2015.
- H. Hamacher, K. Klamroth: *Lineare Optimierung und Netzwerkoptimierung*, Vieweg, 2006.
- S. Bradley, A. Hax, T. Magnanti: *Applied Mathematical Programming*, Addison-Wesley, 1977.

auf denen es teilweise auch basiert. 

# Gemischt-ganzzahlige lineare Programmierung

## Ein Beispiel

Ein chemisches Unternehmen handelt mit drei verschiedenen Substanzen, die in verschiedenen Mengen simultan durch den gleichen Produktionsprozess erzeugt werden. 
Das Unternehmen kann pro Monat (maximal) die folgenden Mengen verkaufen:

Substanz A: 50t, Substanz B: 72t, Substanz C: 20t 

Zur Produktion der Substanzen besitzt das Unternehmen zwei verschiedene Anlagen, die nach leicht verschiedenen Verfahren arbeiten. Dadurch ergeben sich unterschiedliche Produktionsmengen pro Tag. Der Betrieb der Anlagen erbringt pro Tag einen Profit von je 2 Millionen Euro.
An Tagen an denen die Anlagen nicht produzieren, fällt kein Profit, aber auch keine Kosten an.

Darüber hinaus ist Folgendes über die Tagesproduktion der Anlagen bekannt:

|           | Anlage 1  | Anlage 2  |
|:----------|-----------|----------:|    
|Substanz A | 5t / Tag  | 10t / Tag |
|Substanz B | 12t / Tag | 8t / Tag  | 
|Substanz C | 4t / Tag  | 0t / Tag  | 

Die Firma hat keine Lagermöglichkeit und kann pro Monat nicht mehr produzieren, als sie verkaufen kann. Wie viele Tage pro Monat muss die Firma in den jeweiligen Anlagen produzieren, um ihren Profit zu optimieren? Anmerkung: Die Firma kann auch für den Bruchteil eines Tages produzieren (anstatt den ganzen Tag) und erhält dann auch nur den entsprechenden Bruchteil des Profits.

````{prf:example}
TO DO
````

## Definition
Ein *lineares Programm* ist ein Optimierungsproblem, bei dem eine lineare Zielfunktion unter linearen Nebenbedingungen optimiert werden soll.

````{prf:example}
TO DO
````

Als Nebenbedingungen sind Ungleichungen und Gleichungen der Art $\leq, \geq, =$ erlaubt. Nicht erlaubt und typischerweise auch nicht sinnvoll sind Ungleichungen der Art $<$ bzw $>$. 

````{prf:definition} Lineares Programm in allgemeiner Form

Gegeben sei eine $m \times n$-Matrix $A=(a_{ij})$, ein $m$-dimensionaler Vektor $b$, sowie ein $n$-dimensionaler Vektor $c$. Ein *lineares Programm* ist ein Optimierungsproblem der Form
\begin{alignat*}{5}
\min / \max          & \quad  &   c_1x_1 + \ldots + c_nx_n &          & & \\[2mm]
\text{s.t. } & &  a_{i1}x_1 + \ldots + a_{in}x_n & = & \ b_i & \quad\quad & & \forall i= 1, \ldots, p \\
& &  a_{i1}x_1 + \ldots + a_{in}x_n & \leq & \ b_i & \quad\quad & & \forall i= p+1, \ldots, q \\
& &  a_{i1}x_1 + \ldots + a_{in}x_n & \geq & \ b_i & \quad\quad & & \forall i= q+1, \ldots, m \\
& & x_j & \geq & \ 0 & && \forall j= 1, \ldots, n.
\end{alignat*}
````

Es müssen dabei nicht alle möglichen Arten von Nebenbedingungen ($\leq, =, \geq, \geq 0$) vorkommen.
Um mit einer einheitlichen Darstellung arbeiten zu können, benutzt man gerne lineare Programme in der sogenannten *Standardform*.

````{prf:definition} Lineares Programm in Standardform

Gegeben sei eine $m \times n$-Matrix $A$, ein $m$-dimensionaler Vektor $b$, sowie ein $n$-dimensionaler Vektor $c$. Ein *lineares Programm* ist ein Optimierungsproblem der Form
\begin{alignat*}{5}
\min          & \quad  &   c_1x_1 + \ldots + c_nx_n &          & & \\[2mm]
\text{s.t. } & &  a_{i1}x_1 + \ldots + a_{in}x_n & = & \ b_i & \quad\quad & & \forall i= 1, \ldots, m \\
& & x_j & \geq & \ 0 & && \forall j= 1, \ldots, n.
\end{alignat*}
In Matrixform

\begin{alignat*}{5}
\min          & \quad  &   c^Tx &          & & \\[2mm]
\text{s.t. } & &  Ax & = & b & \\
& & x & \geq & \ 0 & &&
\end{alignat*}
````

## Standardumformungen

Wie bringt man ein beliebiges Lineares Programm in Standardform? Wir gehen als Zwischenschritt einen etwas umständlichen Weg, der sich später als praktisch und einfacher zu verstehen erweist. Wir bringen dazu das LP erst in eine Form, bei der ein Minimierungsproblem vorliegt, alle Variablen nicht-negativ sind und nur Nebenbedingungen der Form $\leq$ vorliegen:

\begin{alignat*}{5}
\min_{x_1, \ldots, x_p} &\quad & \sum_{j=1}^{n}c_j x_j \\[2mm]
\text{s.t. } & &\sum_{j=1}^{n} a_{ij} x_j &\leq&  \ b_i & \quad\quad & & \forall i=1,\ldots,m \\
             & & x_j                      &\geq&  0 &  && \forall j =1 ,\ldots ,n
\end{alignat*}

Danach bringen wir es in Standardform. Wir starten mit einem beliebigen linearen Problem
\begin{alignat*}{5}
\max_{x_1, \ldots, x_p} &\quad & \sum_{j=1}^{n}c_j x_j \\[2mm]
\text{s.t. } & &\sum_{j=1}^{n} a_{ij} x_j &\leq&  \ b_i & \quad\quad & & \forall i=1,\ldots,m_1 \\
             & &\sum_{j=1}^{n} a_{ij} x_j &\geq&  \ b_i & \quad\quad & & \forall i=m_1+1,\ldots,m_2 \\
             & &\sum_{j=1}^{n} a_{ij} x_j &=&  \ b_i & \quad\quad & & \forall i=m_2+1,\ldots,m \\
\end{alignat*}
````{prf:example}
TO DO
````

Wir wandeln das LP nun wie folgt in ein neues LP um: 

**(1)** Falls ein Maximierungsproblem vorliegt, wandeln wir es in ein Minimierungsproblem um, indem wir die Zielfunktion
\begin{align*}
\max \sum_{j=1}^{n}c_j x_j 
\end{align*}
durch
\begin{align*}
\min \sum_{j=1}^{n}-c_j x_j
\end{align*} 
ersetzen.
````{prf:example}
TO DO
````

**(2)** Nebenbedingungen der $=$-Form 
\begin{align*}
\sum_{j=1}^{n} a_{ij} x_j = b_i 
\end{align*}
ersetzen wir durch zwei Nebenbedingungen
\begin{eqnarray*}
    \sum_{j=1}^{n} a_{ij} x_j & \leq & b_i \\
    \sum_{j=1}^{n} a_{ij} x_j & \geq & b_i.
\end{eqnarray*}
````{prf:example}
TO DO
````
    
**(3)** Nebenbedingungen der $\geq$-Form 
\begin{align*}
\sum_{j=1}^{n} a_{ij} x_j \geq b_i
\end{align*}
multiplizieren wir mit $-1$ durch und erhalten 
\begin{align*}
\sum_{j=1}^{n} -a_{ij} x_j \leq -b_i
\end{align*}
````{prf:example}
TO DO
````
    
**(4)** Für jede Variable $x_i$, die negativ werden kann, fügen wir zwei neue Variablen 
\begin{align*}
x_i^+ \text{ und } x_i^- 
\end{align*}
mit den Nichtnegativitätsbedingungen 
\begin{align*}
x_i^+\geq 0\\
x_i^-\geq 0
\end{align*}
ein. Nun ersetzen wir jedes Vorkommen von $x_i$ durch $(x_i^+-x_i^-)$
````{prf:example}
TO DO
````

**(5)** Wir haben nun die Form des Zwischenschrittes erreicht: 
\begin{alignat*}{5}
\min_{x_1, \ldots, x_p} &\quad & \sum_{j=1}^{n}c_j x_j \\[2mm]
\text{s.t. } & &\sum_{j=1}^{n} a_{ij} x_j &\leq&  \ b_i & \quad\quad & & \forall i=1,\ldots,m \\
             & & x_j                      &\geq&  0 &  && \forall j =1 ,\ldots ,n
\end{alignat*}


Um das Problem in Standardform 
zu bringen, müssen wir die Nebenbedingungen von der $\leq$-Form in die $=$-Form bringen. Dies lässt sich durch das Zufügen von neuen Variablen, sogenannten *Schlupfvariablen* $x_{p+1},\ldots,x_n$  erreichen:
\begin{align*}
\begin{array}{llllll}
a_{11} x_1+\ldots +a_{1p} x_p	& +x_{p+1} & &  &   & =b_1\\ 
a_{21} x_1+\ldots +a_{2p} x_p	&  & +x_{p+2} & &   & =b_2\\
\vdots & & & \ddots & & \vdots\\
a_{m1} x_1+\ldots +a_{mp} x_p	&  & &&  +x_{p+m} & =b_m\\  
\end{array} 
\end{align*}
Auf unser Beispiel übertragen ergibt dies
````{prf:example}
TO DO
````

Damit ist das LP in Standardform. In Matrixform schreiben wir
````{prf:example}
TO DO
````

## Lösbarkeit von Linearen Programmen

Wir betrachten ein beliebiges lineares Problem LP. Wir haben gesehen, dass wir ohne Beschränkung der Allgemeinheit annehmen können, dass LP in Standardform gegeben ist. Wir nennen jedes $x$, das alle Nebenbedingungen erfüllt, eine *zulässige Lösung* des linearen Problems.

````{prf:definition} Zulässige Lösung
Gegeben ist ein Lineares Programm LP: $\min  c^Tx$ unter den Nebenbedingungen $Ax=b$ und $x\geq 0$. 
Es heißt
\begin{align*}
P=\{x \in \RR^n \mid Ax=b, \ x\geq 0\}
\end{align*}
die *Menge aller zulässigen Lösungen* von LP.
````

Eine zulässige Lösung heißt *optimal*, wenn es keine andere zulässige Lösung mit einem besseren Zielfunktionswert gibt.

````{prf:definition} Optimale Lösung
Gegeben ist ein lineares Programm LP: $\min  c^Tx$ unter den Nebenbedingungen $Ax=b$ und $x\geq 0$. 
Es sei $P$ die Menge der zulässigen Lösungen von LP. Es heißt $x^*\in P$ *optimal* für LP, wenn für alle $x' \in P$ gilt, dass $c^Tx^* \leq c^Tx'$.
````

Ein lineares Problem heißt *unbeschränkt*, wenn es für jeden Wert $k$ eine  zulässige Lösung mit Zielfunktionswert gibt, der besser als $k$ ist. Man kann also "beliebig gut werden".

````{prf:definition} Unbeschränktes Lineares Programm
Gegeben ist ein lineares Programm LP: $\min  c^Tx$ unter den Nebenbedingungen $Ax=b$ und $x\geq 0$. 
Es sei $P$ die Menge der zulässigen Lösungen von LP. LP heißt *unbeschränkt*, wenn es für alle $k \in \RR$ ein $x \in P$ gibt, so dass $c^Tx \leq k$.
````


Für jedes lineare Programm LP trifft genau einer der folgenden Möglichkeiten zu:
1. LP besitzt eine optimale Lösung.
2. LP besitzt keine zulässige Lösung.
3. LP ist unbeschränkt.

````{prf:example}
TO DO
````

(subsec:polyeder)=
## Der Polyeder der zulässigen Lösungen
Jede Gleichung der Form 
\begin{align*} \sum_{j=1}^{n} a_{ij} x_j = b_i \end{align*}
unterteilt den Raum $\RR^n$ in zwei *Halbräume*
$\sum_{j=1}^{n} a_{ij} x_j \leq b_i$ und
$\sum_{j=1}^{n} a_{ij} x_j \geq  b_i$.
````{prf:example}
TO DO
````

Wir erinnern uns, dass man die Menge $P$ der zulässigen Lösungen eines linearen Programms auch ausschließlich durch Ungleichungen des Typs $\sum_{j=1}^{n} a_{ij} x_j  \leq  b_i$ beschreiben kann. 
Es ist $P$ dann genau die Schnittmenge von den endlich vielen Halbräumen, die durch die Nebenbedingungen definiert sind. Man nennt eine solche Punktmenge einen *Polyeder*.

````{prf:definition} Polyeder
Ein *Polyeder* $P \subseteq \RR^n$ ist eine Punktmenge, die eine endliche Zahl an linearen Ungleichungen erfüllt, d.h. die durch die Form 

\begin{align*}
P=\{x \in \RR^n \mid Ax \leq b\}
\end{align*}

darstellbar ist für eine $m \times n$ Matrix A und einen $m$-dimensionalen Vektor $b$.
````

Ein Punkt $x \in P$ in einem Polyeder $P$ heißt *Ecke*, wenn er nicht in der Mitte von zwei anderen Punkten aus $P$ liegt.

````{prf:example}
TO DO
````

````{prf:definition} Ecke
Ein Punkt $x \in P$ in einem Polyeder $P$ heißt *Ecke* von $P$, falls es keine zwei Punkte $x^1, x^2 \in P$ gibt mit $x^1\not=x^2$, so dass $x=\frac{1}{2}x^1+\frac{1}{2}x^2$ gilt.
````

Eine Menge $T \subseteq \RR^n$ heißt *konvex*, wenn für jedes Punktepaar $x^1, x^2 \in T$ auch die komplette Verbindungslinie zwischen $x^1$ und $x^2$ in der Menge $T$ liegt. Polyeder sind konvexe Mengen.

````{prf:example}
TO DO
````

````{prf:definition} Konvexität
Eine Menge $T \subseteq \RR^n$ heißt *konvex*, falls aus $x^1 \in T$ und $x^2 \in T$ folgt, dass $\lambda x^1 + (1-\lambda) x^2 \in T$ gilt.
````

Besitzt ein lineares Programm eine optimale Lösung, so besitzt es auch mindestens eine optimale Lösung, die eine Ecke im zugehörigen Lösungspolyeder ist.

````{prf:example}
TO DO
````

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
