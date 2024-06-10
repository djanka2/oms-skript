---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(sec:ad)=
## Automatische Differentiation
Wie wir im Kapitel {ref}`sec:analysis` gelernt haben, kann man die partiellen Ableitungen zu einer gegebenen Funktion mit einer Handvoll einfacher Regeln bestimmen. Dieses Vorgehen hat allerdings Grenzen: In vielen Anwendungen, z.B. im Bereich maschinelles Lernen, trifft man auf sehr hochdimensionale, verschachtelte Funktionen. So sind beispielsweise neuronale Netze genau das: hochdimensionale, verschachtelte Funktionen. Obwohl es theoretisch mit den herkömmlichen Ableitungsregeln möglich wäre, bestimmt natürlich niemand deren partielle Ableitung mit Papier und Bleistift, da es zum Einen viel zu lange dauern würde und zum Anderen sehr fehleranfällig wäre. 

Wir schauen uns in diesem Kapitel an, wie Computer partielle Ableitungen automatisch, exakt und effizient berechnen. Wir tun dies hier teilweise anhand von entsprechenden Python Bibliotheken, weisen aber darauf hin, dass es die Verfahren auch in anderen Programmiersprachen gibt und diese dort nach den gleichen Prinzipien funktionieren.


### Vorbetrachtung: Mathematische Funktionen in Python
Wir schauen uns zunächst einmal an, wie Python (und die meisten anderen Programmiersprachen) mit mathematischen Funktionen, also Objekten der Art $f:\R^n\rightarrow \R$, arbeitet. Nehmen wir einmal an, wir möchten die univariate Funktion $f(x)=x^2-3x$ in Python darstellen. Dies könnten wir mit folgendem Code tun:

```{code-cell} ipython3
def f(x):
    return x*x - 3*x
```

Nun möchten wir die Funktion plotten, z.B. im Bereich $x\in[-2,4]$. Der Computer geht dabei genauso vor, wie Sie vorgehen würden, wenn Sie die Funktion auf ein Blatt Papier zeichnen würden: Wir nehmen einige $x$-Werte aus dem gewünschten Intervall, berechnen für jeden $x$-Wert den zugehörigen Funktionswert $x^2-3x$, tragen die Punkte in ein Koordinatensystem ein und verbinden sie dann. In Python:

```{code-cell} ipython3
import numpy as np
import seaborn as sns

# Erzeuge 50 äquidistante x-Werte
x = np.linspace(-2,4,50)

# Berechne für jeden x-Wert den Funktionswert
y = f(x)

# Zeichne ein Liniendiagramm für die beiden "Wertelisten" x und y
sns.lineplot(x=x, y=y)
```

Wie erwartet wird eine Parabel geplottet. Schauen wir uns aber genauer an, wie der Code eigentlich funktioniert: die Python-Funktion `f` "weiß" nicht, welcher Datentyp `x` ist. Falls `x` eine Zahl ist, liefert `f` auch nur eine Zahl zurück. Ist `x` aber ein NumPy Array, so wie hier, wird die Operation `x*x - 3*x` punktweise für jedes Element des Arrays ausgeführt (dies ist durch die Definition der Operatoren `*` und `+` für NumPy Arrays so festgelegt). Konsequenterweise liefert `f` in diesem Fall auch einen Array mit Funktionswerten zurück, der die gleiche Länge hat wie der Array `x` (hier: 50). Der Funktion `sns.lineplot` werden nun die beiden Arrays, d.h. einfach Listen mit Zahlen, übergeben, die diese dann in einem Koordinatensystem einzeichnet und mit Linien verbindet. Werden dabei genügend Punkte verwendet, so ist diese eigentlich stückweise lineare Funktion nicht mehr von einer Parabel zu unterscheiden. Probieren Sie einmal aus, was passiert, wenn `x` nur aus 5 Werten besteht. Interessant daran ist, dass `sns.lineplot` gar nicht "weiß", dass es sich um die Funktion $f(x)=x^2-3x$ handelt. Es bekommt lediglich Listen mit Zahlen übergeben. 

Dieses Paradigma des punktweisen Auswertens wird auch bei der automatischen Berechnung von Ableitungen verfolgt. Anstatt den algebraischen Ausdruck $x^2-3x$ bzw. dessen Code-Repräsentation `x*x - 3*x` umzuformen, so wie wir es tun würden, wenn wir per Hand die Ableitung berechnen, wird mittels eines speziellen Algorithmus sichergestellt, dass bei einer punktweisen Auswertung von `f` auch deren Ableitung an diesem Punkt ausgewertet wird.


% ### Finite Differenzen
% TODO


### Berechnungsgraphen
Um Ableitungen automatisch auszuwerten, wird jede mathematische Funktion als ein *gerichteter, azyklischer Graph* aufgefasst. Dies ist eine Menge aus Knoten und Kanten, die keine Kreise enthält.
```{figure} ./bilder/graphen.png
:width: 500px

Links: Gerichtetet, azyklischer Graph. Mitte: Ungerichteter azyklischer Graph. Rechts: Gerichteter Graph mit Zyklus.
```
Wenn eine Kante von Knoten a nach Knoten b existiert, so nennt man a auch ein *Kind* von b. Wir nennen außerdem Knoten, zu denen keine Kante hinführt, *Eingangsknoten*, und Knoten, von denen keine Kante wegführt, *Ausgangsknoten*.


```{prf:observation}
Jede in Quellcode implementierte mathematische Funktion kann als *Abfolge elementarer Operationen* aufgefasst werden und in einem gerichteten, azyklischen Graphen dargestellt werden. Unter dem Begriff "elementare Operationen" stellen wir uns zunächst die Operationen $+, -, \cdot, /$ sowie die mathematischen Funktionen $\exp, \sin, \cos, \ln$ vor. Später werden wir sehen, dass es hilfreich ist auch andere Operationen als "elementare Operation" zu definieren, insbesondere vektorwertige.
```

````{prf:example} 
Die Funktion 
\begin{align*}
f(x)=(x_1x_2\sin x_3 + e^{x_1x_2})/x_3
\end{align*}
kann als folgende Abfolge elementarer Operationen aufgefasst werden:
\begin{align*}
x_4&=x_1\cdot x_2\\
x_5&=\sin x_3\\
x_6&=e^{x_4}\\
x_7&=x_4\cdot x_5\\
x_8&=x_6+x_7\\
x_9&=x_8/x_3
\end{align*}
In jeder Zeile wird genau *eine* elementare Operation ausgeführt. Die Reihenfolge, in der die Operationen ausgeführt werden, ist dabei nicht immer eindeutig. Die Variablen $x_4,\dots,x_9$ sind *Zwischenvariablen* (im Gegensatz zu den *unabhängigen* Variablen $x_1,x_2,x_3$) und ergeben sich für beliebige Werte $x_1,x_2,x_3$. $x_9$ enthält den Funktionswert. 

Als Graph lässt sich das Ganze wie folgt darstellen:

```{figure} ./bilder/berechnungsgraph.png
:width: 500px
```
````
%Auch die Tatsache, dass der Term $x_4=x_1\cdot x_2$ an zwei Stellen wiederverwendet wird
Die Zwischenvariablen $x_4,\dots,x_9$ müssen übrigens nicht explizit als Variablen im Code eingeführt werden. Sie repräsentieren vielmehr die logische Abfolge der Berechnungsschritte. Tools zur automatischen Ableitungserzeugung erzeugen diesen Berechnungsgraphen automatisch (z.B. PyTorch, Tensorflow, autograd).


### Kettenregel und Berechnunsgraphen
Das Konzept von Berechnungsgraphen ist (hoffentlich) illustrativ und verständlich. Wir werden nun sehen, dass die Darstellung einer Funktion als Berechnungsgraph der Schlüssel dafür ist, automatisch ihre partielle Ableitungen auszuwerten. Dazu halten wir als nächsten Schritt folgendes fest:
```{prf:observation}
Berechnungsgraphen beschreiben die *Verkettung* von Funktionen, und zwar derjenigen Funktionen, die durch die elementaren Operationen definiert sind. 
```
Wie schauen uns dazu ein einfaches Beispiel an. Die Funktion $h(x)=\cos x^2$ kann als verkettete Funktion der beiden Funktionen $g(y)=\cos y$ und $f(x)=x^2$ aufgefasst werden:
\begin{align*}
h(x)=g(f(x))=\cos x^2
\end{align*}
Erinnerung: das hatten wir in den Abschnitten {ref}`sec:stetigkeit` und {ref}`sec:kettenregel` mit $g\circ f$ (erst $f$, dann $g$) bezeichnet.

Der Berechnungsgraph zur Funktion $h(x)=\cos x^2$ ist

```{figure} ./bilder/berechnungsgraph2.png
:name: fig:simplegraph
:width: 600px

Ein einfacher Berechnungsgraph.
```

Der Graph beschreibt also gerade die Verkettung $g(f(x))$. Dies ist auch nicht nur in diesem einfachen univariaten Beispiel so, sondern gilt allgemein für Berechnungsgraphen. Um nun die Ableitung dieses Berechnungsgraphen zu berechnen, der die *Verkettung* von Funktionen darstellt, benutzt man die ...... Kettenregel!

Wir schauen uns nun an, wie die Kettenregel für Berechnungsgraphen funktioniert. Dafür berechnen wir zunächst die Ableitung der Funktion $h$ mit der gewöhnlichen Kettenregel:[^kettenregel]
\begin{align*}
\derv{h}{x}=\derv{g(f(x))}{x}=\underbrace{\derv{g(f(x))}{f(x)}}_{-\sin{f(x)}}\cdot\underbrace{\derv{f}{x}}_{2x}=-2x\cdot \sin{x^2}
\end{align*}

[^kettenregel]: Obwohl wir es hier mit einer univariaten Funktion zu tun haben, nutzen wir trotzdem die Notation für die partielle Ableitung, da der multivariate Fall analog verlaufen wird.

Dies entspricht der bekannten Merkregel "Äußere Ableitung $\times$ innere Ableitung". In dem zugehörigen Berechnungsgraphen lässt sich die Kettenregel wie folgt interpretieren: 

```{prf:observation} Ableitung entlang eines Pfads
:label: obs:pfad
Annotiere jeden Knoten mit seiner Ableitung bezüglich des Inputs (d.h. die Ableitung einer der "elementaren Operationen") und multipliziere die Knoten entlang des Pfades.
```

Nun haben Berechnungsgraphen im Allgemeinen eine kompliziertere Gestalt als {numref}`fig:simplegraph`. Wie lässt sich die Pfadregel verallgemeinern? Wir betrachten dazu das (immer noch univariate) Beispiel $f(x)=\sin x^2 + \cos x^2$. Der Berechnungsgraph von $f$ ist:[^argumente]
```{figure} ./bilder/berechnungsgraph3.png
:name: fig:example_graph
:width: 600px
```
[^argumente]: Wir haben hier eigene Bezeichner $x,y,z,v,w$ für die Argumente der Teilfunktionen eingeführt. Dies ist eigentlich nicht nötig, es soll hier nur klar gemacht werden, dass die einzelnen Knoten nichts voneinander "wissen". D.h. jeder Knoten hat einen Eingangswert und einen Ausgangswert. Zwar können bestimmte Eingangs- bzw. Ausgangswerte identisch sein (im Beispiel wäre etwa $y=z=x^2$), das "wissen" aber die einzelnen Knoten nicht. 

Interessant ist, dass wir, um die Funktion $f$ wirklich als Berechnungsgraph und damit als Verkettung von Funktionen zu schreiben, auf mehrdimensionale Funktionen zurückgreifen müssen. Die $+$-Operation wird nämlich durch die Funktion $k:\R^2\rightarrow\R$ mit $k(v,w)=v+w$ dargestellt.

Wir berechnen nun für diese Verkettung die partielle Ableitung mit der multivariaten Kettenregel (das ist der schwierige Teil) und schauen dann, wie sie sich in dem Graph interpretieren lässt (das ist der einfache Teil). Es gilt:
\begin{align*}
f(x)&=k(v,w)=k(h(y),i(z))=k(h(g(x)),i(g(x)))\\
\derv{f}{x}&=\left(\derv{k(v,w)}{v},\derv{k(v,w)}{w}\right)\cdot \bmat \derv{h(y)}{y}\\\derv{i(z)}{z} \emat\cdot\derv{g}{x}\\
%\derv{f}{x}&=\derv{k(h(g(x)),i(g(x)))}{h(g(x)),i(g(x))}\cdot \bmat \derv{h(g(x))}{g(x)}\\\derv{i(g(x))}{g(x)} \emat\cdot  \derv{g}{x}\\
&=\bmat 1, & 1 \emat \cdot\bmat cos y \\ -\sin z \emat \cdot 2x\\
&=(\cos y-\sin z)2x \\
&= 2x\cdot \cos x^2 - 2x\cdot \sin x^2
\end{align*}
Während es bei der Anwendung der multivariaten Kettenregel oft schwerfällt, den Überblick über die Symbole und Dimensionen zu behalten, ist ihre Interpretation auf Berechnungsgraphen sehr einfach: Es gibt in dem Graphen zwei Pfade von $x$ nach $f$. Die Ableitung von $f$ nach $x$ ist die Summe der Ableitungen entlang der beiden Pfade. Entlang jedes Pfads wird die Ableitung gemäß 
{prf:ref}`obs:pfad` berechnet. Wir halten diese Beobachtung in folgendem Satz fest:

```{prf:theorem}
:label: thm:kettenregel_pfad
Sei $f:\R^n\rightarrow\R$ eine differenzierbare Funktion, die durch einen Berechnungsgraphen mit Eingangsknoten $x_1,x_2,\dots,x_n$ und Ausgangsknoten $f$ repräsentiert wird. Dann kann man die Ableitung $\derv{f}{\v x}$ mittels der multivariaten Kettenregel auf dem Berechnungsgraphen wie folgt interpretieren:
Die Ableitung der Variable im Output Knoten $f$ nach einer Variable in einem Eingangsknoten $x_i$ ist die Summe der Ableitungen entlang aller möglichen Pfade zwischen $x_i$ und $f$. Die Ableitungen entlang der Pfade können mit der unvariaten Kettenregel als Produkte der (lokalen) Ableitungen an jedem Knoten des Pfads berechnet werden.
```

Wir haben das Problem der Ableitungsberechnung nun also auf ein Problem auf Berechnungsgraphen zurückgeführt. Die Anzahl der möglichen Pfade zwischen Eingangs- und Ausgangsknoten wächst allerdings exponentiell, wie wir anhand des folgenden Beispiels sehen können.

```{figure} ./bilder/berechnungsgraph5.png
:name: fig:32paths
:width: 600px

Ein Berechnungsgraph, der die Funktion $f(x)=x^{32}$ durch fünfmaliges quadrieren der Eingangsvariablen berechnet. Insgesamt gibt es zwischen dem Eingangs- und Ausgangsknoten $2^5=32$ Pfade entlang deren die Ableitungen berechnet und aufsummiert werden müssen.
```

Das Beispiel ist natürlich recht konstruiert, es zeigt aber, wie schon bei simplen Beispielen, die Anzahl der Pfade bzw. Ableitungsberechnung schnell wächst. Berechnungsgraphen für Funktionen z.B. im maschinellen Lernen sind um ein Vielfaches größer, wodurch das Problem umso gravierender wird. 

Eine andere Sichtweise auf das Problem der vielen Pfade ist, dass mehrfach die gleichen Berechnungen eines Knotens durchgeführt werden. In dem Beispiel liegt jeder Zwischenknoten auf 16 Pfaden, es würde also 16 Mal exakt die gleiche Berechnung durchgeführt. 


### Rückwärtsmodus der automatischen Differentiation (Backpropagation)
Ein Ansatz, der die Iteration über alle möglichen Pfade vermeidet, ist der [dynamischen Programmierung](https://de.wikipedia.org/wiki/Dynamische_Programmierung) entlehnt. Hierbei werden Ergebnisse (Ableitungen) zwischengespeichert und an geeigneter Stelle wiederverwendet. Damit das funktioniert, müssen die Knoten in einer bestimmten Reihenfolge durchlaufen werden. Als Konsequenz, wird im Laufe des Verfahrens jeder Knoten und jede Kante des Graphen genau zweimal bearbeitet, das Verfahren unterliegt also keinem exponentiellen Wachstum.

Das Verfahren ist -- vor allem für den Bereich maschinelles Lernen -- einer der bekanntesten und wichtigsten mathematischen Algorithmen überhaupt und ist vor allem unter zwei Namen bekannt:
1. Rückwärtsmodus der automatischen Differentiation
2. Backpropagation (of errors)

Es ist nicht übertrieben zu sagen, dass alle aktuellen Entwicklungen im Bereich KI ohne dieses Verfahren nicht existieren würden. Es wurde im Laufe der Jahre von [verschiedenen Forschern](https://people.maths.ox.ac.uk/~trefethen/inventorstalk.pdf)  (wieder-)entdeckt. Die erste allgemeine Form geht auf den finnischen Mathematiker Seppo Linnainmaa zurück, der das Verfahren 1970 in seiner Masterarbeit entwickelte.

Der Algorithmus arbeitet auf einem Berechnungsgraphen einer Funktion $f:\R^n\rightarrow\R$, dessen Knoten wir mit $x_1,\dots,x_N$ bezeichnen. Dabei seien die ersten $n$ Knoten $x_1,\dots,x_n$ die Eingangsknoten und der letzte Knoten $x_N=f(\v x)$ der Ausgangsknoten. Der Algorithmus arbeitet in zwei Phasen:
1. Vorwärtsphase: Für einen gegebenen (beliebigen) Wert der Eingangsknoten $\v x'=(x_1',\dots,x_n')$ wird der Wert an allen Knoten $x_{n+1}',\dots,x_N'=f(\v x')$ des Berechnungsgraphen bestimmt.
2. Rückwärtsphase: Hier wird der Graph rückwärts, d.h. ausgehend vom Ausgangsknoten traversiert. Dabei werden alle partiellen Ableitungen $\derv{f}{x_i}(\v x'), i=1,\dots,N$ bestimmt.

Eigentlich möchten wir ja nur die Ableitung nach den Eingangsknoten, d.h. $\derv{f}{x_i}(\v x'), i=1,\dots,n$, aber durch die Art wie der Algorithmus arbeitet, bekommen wir die anderen Ableitungen gratis dazu. Wir führen für die partiellen Ableitungen die folgenden Bezeichner ein:
\begin{align*} 
\overline{x}_i:=\derv{f}{x_i}(\v x')
\end{align*}
Die Variablen $\overline{x}_i$ nennt man auch *adjungierte Variablen*. Diese werden im Verlauf des Algorithmus nach und nach berechnet. Damit können wir den Algorithmus wie folgt spezifizieren:


```{prf:algorithm} Rückwärtsmodus der automatischen Differentiation (Backpropagation)
:label: alg:backprop

Gegeben:
: - Gerichteter, azyklischer Berechnungsgraph mit Knoten $x_i, i=1,\dots,N$, wobei $x_N=f$ die Variable im Ausgangsknoten sei (die Funktion, deren Ableitung berechnet werden soll)
: - $\v x'=(x_1',\dots,x_n')$: Werte an den Eingangsknoten (die Stelle, an denen die Ableitung von $f$ ausgewertet werden soll)
: - Für jedes Kind $j$ des Knoten $i$ bezeichne $\derv{x_i}{x_j}$ die („lokale“) Ableitung (="wie ändert sich $x_j$, wenn sich $x_i$ ändert, unabhängig davon was vor $i$ und nach $j$ geschieht")

Gesucht:
: - Werte an allen Knoten $x_i'$, insbesondere der Wert am Ausgangsknoten $x_N'=f(\v x')$
: - Alle partiellen Ableitungen $\overline{x}_i=\derv{f}{x_i}(\v x')$, insbesondere die Ableitungen nach den Eingangsknoten $\overline{x}=\derv{f}{\v x}(\v x')$

**Algorithmus**:
1. Start: Initialisiere $\overline{x}_N=\derv{f}{f}=1$.
2. Solange noch Knoten vorhanden sind, die noch nicht ausgewählt wurden:
   1. Wähle unbearbeiteten Knoten $i$, von dem alle Werte $\overline{x}_j$ der Kinder bekannt sind.
   2. Setze
     \begin{align*}
     \overline{x}_i=\sum_{j: \textup{Kind von }i} \overline{x}_j\cdot \derv{x_j}{x_i}=\sum_{j: \textup{Kind von }i} \derv{f}{x_j}\cdot  \derv{x_j}{x_i}
     \end{align*}
```
Wie Sie sehen, ist der Algorithmus selbst relativ kurz. Die Formel zur Berechnung von $\overline{x}_i$ ist übrigens gerade die Kettenregel: Die Ableitung von $f$ nach $x_i$ ist die Ableitung von $f$ bis zu den Knoten, die unmittelbar nach $x_i$ kommen multipliziert mit der lokalen Ableitung $\derv{x_j}{x_i}$. Der gesuchte Gradient $\nabla f(x')$ ist nach Terminierung des Algorithmus in den adjungierten Variablen $\overline{x}_i, i=1,\dots,n$ gespeichert.

Wir führen den Algorithmus noch einmal am Beispiel von weiter oben, $f(x)=\sin x^2 + \cos x^2$ aus. Dabei verwenden wir die Notation der Zwischenknoten mit $x_i$ und notieren auch gleich die Adjungierten $\overline{x}_i$ an jeden Knoten (diese werden im Verlauf des Algorithmus berechnet).
```{figure} ./bilder/berechnungsgraph4.png
:name: fig:example_graph_x
:width: 600px
```
```{prf:example} Backpropagation für $f(x)=\sin x^2+\cos^2$ an der Stelle $x=\sqrt{\pi}$
Vorwärtsphase:
- $x_1=\sqrt{\pi}$
- $x_2=x_1^2=\pi$
- $x_3=\sin x_2=0$
- $x_4=\cos x_2=-1$
- $x_5=x_3+x_4$

Rückwärtsphase:
- Schritt 1: Start: Setze $\overline{x}_5=\derv{f}{f}=1$
Als nächstes müssen wir einen unbearbeiteten Knoten wählen, dessen Kinder bereits berechnet wurden. Wir können entweder $x_4$ oder $x_3$ wählen.
- Schritt 2: Wähle $x_4$. Setze $\overline{x}_4=\overline{x}_5\derv{x_5}{x_4}=1\cdot1=1$.
Der Ausdruck $\derv{x_5}{x_4}$ sieht etwas ungewohnt aus. Stellen sie sich dafür $x_5$ als *Funktion* vor, die abgeleitet wird. Als nächstes müssen wir $x_3$ wählen.
- Schritt 3: Wähle $x_3$. Setze $\overline{x}_3=\overline{x}_5\derv{x_5}{x_3}=1\cdot1=1$.
Nun können wir $x_2$ wählen. $x_2$ hat zwei Kinder, also müssen auch zwei lokale Ableitungen aufsummiert werden.
- Schritt 4: Wähle $x_2$. Setze $\overline{x}_2=\overline{x}_4\derv{x_4}{x_2}+\overline{x}_3\derv{x_3}{x_2}=1\cdot(-sin x_2)+1\cdot\cos x_2=-1$.
- Schritt 5: Wähle $x_1$. Setze $\overline{x}_1=\overline{x}_2\derv{x_2}{x_1}=-1\cdot2x_1=-2\sqrt{\pi}$

Damit sind alle Knoten bearbeitet und der Algorithmus terminiert. Der Funktionswert von $f$ an der Stelle $\sqrt{\pi}$ ist $f(\sqrt{\pi})=-1$, die Ableitung ist $\overline{x}_1=\derv{f}{x}=-2\sqrt{\pi}$.
```

Wir betrachten ein weiteres Beispiel, diesmal für eine Funktion in zwei Variablen. Da der Algorithmus ohnehin die Ableitungen nach *allen* Knoten berechnet, funktioniert er genauso. Der einzige Unterschied ist, dass nun mehr als ein Knoten als "Eingangsknoten" ausgezeichnet ist.

```{figure} ./bilder/berechnungsgraph6.png
:name: fig:example_graph_x2
:width: 600px
```
```{prf:example} Backpropagation für $f(x_1,x_2)=\frac{\exp x_1x_2}{x_2}$ an der Stelle $(x_1,x_2)=(0,2)$
Vorwärtsphase:
- $x_1=0$
- $x_2=2$
- $x_3=2\cdot 0=0$
- $x_4=\exp 0=1$
- $x_5=\frac{1}{2}$

Rückwärtsphase:
- Schritt 1: Start: Setze $\overline{x}_5=\derv{f}{f}=1$
Als nächstes müssen wir einen unbearbeiteten Knoten wählen, dessen Kinder bereits berechnet wurden. Das ist nur für $x_4$ der Fall.
- Schritt 2: Wähle $x_4$. Setze $\overline{x}_4=\overline{x}_5\derv{x_5}{x_4}=1\cdot\frac{1}{x_2}=\frac{1}{2}$.
Als nächstes müssen wir $x_3$ wählen.
- Schritt 3: Wähle $x_3$. Setze $\overline{x}_3=\overline{x}_4\derv{x_4}{x_3}=\frac{1}{2}\cdot \exp x_3=\frac{1}{2}$.
Nun können wir $x_2$ wählen. $x_2$ hat zwei Kinder, also müssen auch zwei lokale Ableitungen aufsummiert werden.
- Schritt 4: Wähle $x_2$. Setze $\overline{x}_2=\overline{x}_3\derv{x_3}{x_2}+\overline{x}_5\derv{x_5}{x_2}=\frac{1}{2}\cdot x_1+1\cdot \frac{-x_4}{x_2^2}=-\frac{1}{4}$.
- Schritt 5: Wähle $x_1$. Setze $\overline{x}_1=\overline{x}_3\derv{x_3}{x_1}=\frac{1}{2}\cdot x_2=1$

Damit sind alle Knoten bearbeitet und der Algorithmus terminiert. Der Funktionswert von $f$ an der Stelle $(0,2)$ ist $f(0,2)=\frac{1}{2}$, der Gradient ist $\nabla f(0,2)=(\overline{x}_1,\overline{x}_2)=(1,-\frac{1}{4})$.
```

Der Backpropagation Algorithmus erlaubt es, Ableitungen beliebig komplizierter Funktion mittels einem einfach Schema effizient zu berechnen. Dafür müssen die Ableitungen der elementaren Operationen, aus denen der Berechnungsgraph aufgebaut ist, einmalig fest hinterlegt werden. Weiterhin muss bei der Vorwärtsphase jeder Wert $x_1,\dots,x_N$ zwischengespeichert werden, damit er bei der Rückwärtsphase zur Verfügung steht. Der dafür benötigte Speicherplatz kann bei großen Funktionen (neuronalen Netzen), wie sie z.B. im Bereich maschinelles Lernen und KI vorkommen, signifikant sein. 


````{prf:remark} Vorwärtsmodus der automatischen Differentiation
Falls die abzuleitende Funktion selbst vektorwertig ist, ist es u.U. effizienter den *Vorwärtsmodus* der automatischen Differentiation einzusetzen. Dazu werden Funktionsauswertung und Ableitung in einem einzigen Vorwärtdurchlauf des Graphen berechnet. Der Vorwärtsmodus ist deshalb strukturell sogar einfacher als der Rückwärtsmodus, da keine Werte zwischengespeichert werden müssen. 

Die Frage, welcher der beiden Modi effizienter ist, hängt von der Art der Ableitungen ab, die berechnet werden müssen. Im Kontext von Optimierungsproblemen ist dies immer der Gradient, also eine Jacobimatrix mit einer Zeile und (sehr) vielen Spalten. In diesem Fall ist der Rückwärtsmodus viel effizienter. Soll dagegen z.B. die Jacobimatrix einer Funktion berechnet werden, die mehr Zeilen als Spalten hat, so geht dies schneller mit dem Vorwärtsmodus. Da diese Situation im Kontext der von uns betrachteten Optimierungsprobleme allerdings nicht auftritt, gehen wir hier nicht näher darauf ein und beschränken uns auf den Rückwärtsmodus (Backpropagation).
```` 


### Vektorisierung der Knotenoperationen
Wir haben eingangs erwähnt, dass Knoten im Berechnungsgraphen "elementare Operationen" symbolisieren. In den Beispielen kamen dafür die univariaten Funktionen $+, -, \cdot, /, \sin, \cos, \exp, \ln$ zu Einsatz. Diese Auswahl ist natürlich recht willkürlich. Tatsächlich besteht -- neben der effizienten Art, den Berechnungsgraphen zu traversieren -- eine weitere Stärke des Ansatzes der automatischen Differentiation darin, beliebige Funktionen als "elementare Operationen" zu definieren. Man muss für diese Operationen lediglich Code für deren Auswertung sowie die Auswertung der partiellen Ableitungen bereitstellen.

Eine wesentliche Stärke von Softwarepaketen wie `autograd`, [PyTorch](https://pytorch.org/) oder [TensorFlow](https://www.tensorflow.org/) besteht darin, vektorwertige Funktionen als elementare Operationen zu definieren, deren Funktionswerte und Ableitungen dann besonders effizient berechnet werden.

Wir schauen uns zwei Beispiele elementarer Operationen an:
1. Eine lineare Abbildung $f_1:\R^n \rightarrow \R^m$, dargestellt als Multiplikation eines Vektors mit einer (festen) Matrix:
  \begin{align*}
    f_1:\R^n &\rightarrow \R^m\\
    f_1(\v x)&=\m A \v x\\
    \derv{f_1}{\v x} &= \m A\in \R^{m\times n}
  \end{align*}
2. Das Skalarprodukt von zwei Vektoren:
  \begin{align*}
    f_2:\R^{2n} &\rightarrow \R\\
    f_2(\v x, \v y)&=\v x^T \v y\\
    \derv{f_2}{\v x} &= \v y^T \in R^{1\times n}\\
    \derv{f_2}{\v y} &= \v x^T \in R^{1\times n}
  \end{align*}

Damit kann man etwa die Ableitung der Funktion $f:\R^n \rightarrow \R$
$$
  f(\v x)=\v x^T \m H \v x,\quad \m A\in \R^{n\times n}
$$
berechnen. Der Berechnungsgraph der Funktion lässt sich wie folgt darstellen:
```{figure} ./bilder/berechnungsgraph7.png
:name: fig:example_graph_vect
:width: 600px
```
Um den Gradienten $\nabla f(\v x)$ an einer Stelle $\v x'$ zu berechnen, würde die Rückwärtsphase wie folgt ablaufen:
- Schritt 1: Start: Setze $\overline{x}_3=1$
- Schritt 2: Wähle $\v x_2$. Setze $\overline{\v x}_2=\overline{x}_3\derv{x_3}{\v x_2}=1\cdot \v x_1^T$.
- Schritt 3: Wähle $\v x_1$. Setze $\overline{\v x}_3=\overline{\v x}_2\derv{\v x_2}{\v x_1}+\overline{x}_3\derv{x_3}{\v x_1}=\v x_1^T \m H + 1\cdot \v x_2^T = \v x_1^T \m H + \v x_1^T \m H^T$.

Hier ein konkretes Beispiel mit Zahlen: Es soll der Gradient der Funktion

$$
  f(x_1,x_2,x_3)= \bmat x_1 & x_2 &x_3 \emat \bmat 1 & 2 & 3\\ 4 & 5 & 6 \\ 7 & 8 & 9 \emat \bmat x_1 \\ x_2 \\ x_3 \emat
$$

an der Stelle $(-1,1,0)$ berechnet werden. Dazu zunächst die Vorwärtsphase:

- $x_1=\bmat -1 \\ 2 \\ 0 \emat$
- $x_2=\bmat 1 & 2 & 3\\ 4 & 5 & 6 \\ 7 & 8 & 9 \emat \bmat -1 \\ 2 \\ 0 \emat = \bmat 3 \\ 6 \\ 9 \emat$
- $x_3=\bmat -1 & 2 & 0 \emat \bmat 3 \\ 6 \\ 9 \emat= 9$

Rückwärtsphase:
- \begin{align*}
  \overline{x}_3=1
  \end{align*}
- \begin{align*}
  \overline{\v x}_2=\overline{x}_3\derv{x_3}{\v x_2}=\bmat -1 & 2 & 0 \emat
  \end{align*}
- \begin{align*}
  \overline{\v x}_3&=\overline{\v x}_2\derv{\v x_2}{\v x_1}+\overline{x}_3\derv{x_3}{\v x_1}\\
    &=\bmat -1 & 2 & 0 \emat\bmat 1 & 2 & 3\\ 4 & 5 & 6 \\ 7 & 8 & 9 \emat + \v x_2\\
    &=\bmat 7 & 8 & 9 \emat + \bmat 3 & 6 & 9 \emat = \bmat 10 & 14 & 18\emat
  \end{align*}



### Das `autograd` Paket
Im Paket `autograd` ist der Rückwärtsmodus der automatischen Differentiation implementiert. Es ist sehr benutzerfreundlich. Sie können es mittels 
> pip install autograd

aus den Python Paketquellen installieren. `autograd` baut auf NumPy auf und erweitert es um automatische Ableitungsberechnung. Wir schauen uns das Paket anhand der Beispielfunktion aus dem vorherigen Abschnitt an. Zunächst müssen wir anstatt NumPy `autograd.numpy` importieren. Dies ist ein Wrapper für die NumPy Klassen und Funktionen, d.h. es lässt sich bedienen wie NumPy, aber es wird der entsprechende Berechnungsgraph mit erzeugt. Weiterhin importieren wir die Methode grad, mit der Gradienten berechnet werden.

```{code-cell} ipython3
:tags: []

import autograd.numpy as np
from autograd import grad
```

Wir definieren nun unsere Funktion $f(x)=\sin x^2 +\cos x^2$ und werten sie testhalber an der Stelle $\sqrt{\pi}$ aus:
```{code-cell} ipython3
:tags: []
def f(x):
    return np.sin (x**2) + np.cos(x**2)

x_0 = np.sqrt(np.pi)

print(f(x_0))
```
Nun kommt die Ableitungsberechnung. Wir rufen die eben importierte Funktion `grad` auf und übergeben ihr unsere Funktion `f` als Argument. Das Rückgabewert ist wieder eine Funktion, nämlich eine Funktion, die den Gradienten von `f` an einer beliebigen Stelle auswertet.
```{code-cell} ipython3
:tags: []

grad_f = grad(f)
print(grad_f(x_0))
```
Sobald die Funktion ausgewertet wird (hier in der Zeile: `grad_f(x_0)`) wird der Graph zunächst vorwärts (Funktion wird ausgewertet) und anschließend rückwärts durchlaufen (Ableitung nach Eingangsgröße wird ausgewertet). Es wird nur der Wert der Ableitung (in der Sprache des Backpropagation Algorithmus: der Wert der Adjungierten an den Eingangsknoten) ausgegeben. 

Das funktioniert auch mit mehrdimensionalen Funktionen, z.B. $g(x,y,z)=xy^2+z(x-y)$. Der Rückgabewert ist dann ein NumPy Array (Vektor) der Länge 3.
```{code-cell} ipython3
:tags: []

import autograd.numpy as np
from autograd import grad

def g(x):
    return x[0]*x[1]**2 + x[2]*(x[0]-x[1])

x0 = np.array([1.,2.,3.])

print(g(x0))

grad_g = grad(g)

print(grad_g(x0))
```
