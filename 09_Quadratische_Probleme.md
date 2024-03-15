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
# Quadratische Probleme
Wir schauen uns in diesem Kapitel unrestringierte quadratische Optimierungsprobleme an. Diese sind zwar nichtlinear aber dennoch ohne iterative Methoden lösbar. 

## Definition und Beispiele
In {prf:ref}`ex:quadratic` haben wir bereits ein Beispiel für eine quadratische Funktion gesehen. Quadratische Funktionen gibt es auch in mehr als zwei Variablen. Sie bestehen aus Summen von quadratischen und linearen Termen, sog. *Monome*, wobei die quadratischen Terme sowohl Terme der Form $x_3^2$ als auch gemischte quadratische Terme, also z.B. $x_1x_5$, umfassen. Jeder Term hat außerdem einen Koeffizienten. 

```{prf:example} Sind die folgenden Funktionen quadratisch?
- $f_1:\R³\rightarrow \R$, $f_1(\v x)=2+x_1+3x_2²-x_3²$ ist eine quadratische Funktion, da jedes Monom entweder konstant, linear oder aus dem Produkt einer Variable mit sich selbst besteht.
- $f_2:\R²\rightarrow \R$, $f_2(\v x)=x_1x_2+2x_2$ ist eine quadratische Funktion, da in keinem Monom mehr als zwei Variablen miteinander multipliziert werden.
- $f_3:\R²\rightarrow \R$, $f_3(\v x)=x_1²x_2 +x_1²$ ist keine quadratische Funktion, da das erste Monom das Produkt dreier Variablen ist.
```
Die allgemeine Form in $n$ Variablen lautet
\begin{align*}
f(\v x)=\sum_{i=1}^n\sum_{j=1}^n a_{ij}x_ix_j + \sum_{i=1}^n b_ix_i + c
\end{align*}
wobei $a_{ij}, b_i$ und $c$ reelle Zahlen sind (diese können natürlich auch $0$ sein).

Im eindimensionalen ist der Graph jeder quadratische Funktion $f(x)=ax²+bx+c$ eine Parabel, die entweder nach oben oder nach unten geöffnet ist. Sie hat entweder ein Minimum oder ein Maximum, je nachdem welches Vorzeichen der Koeffizient $a$ hat. Dies ist in zwei Dimensionen nicht mehr der Fall. Wir betrachten dazu die Graphen der Funktionen
- $f_1(\v x)=x_1²+x_2²$
- $f_2(\v x)=x_1²$
- $f_3(\v x)=x_1\cdot x_2$
- $f_4(\v x)=x_1²-x_2²$

```{code-cell} ipython3
:tags: [hide-input]

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

x = np.linspace(-2,2,100)
y = np.linspace(-2,2,100)
X,Y = np.meshgrid(x,y)
z1 = X**2 + Y**2
z2 = X**2
z3 = X*Y
z4 = X**2 - Y**2

fig = make_subplots(rows=2, cols=2,
                    specs=[[{'type': 'surface'}, {'type': 'surface'}],
                           [{'type': 'surface'}, {'type': 'surface'}]],
                    subplot_titles=(r'f1',r"f2",r"f3",r"f4")
                    )
fig.add_trace(go.Surface(x=x,y=y,z=z1, colorscale="Blues"), row=1, col=1)
fig.add_trace(go.Surface(x=x,y=y,z=z2, colorscale="Blues"), row=1, col=2)
fig.add_trace(go.Surface(x=x,y=y,z=z3, colorscale="Blues"), row=2, col=1)
fig.add_trace(go.Surface(x=x,y=y,z=z4, colorscale="Blues"), row=2, col=2)


fig.update_layout(  height=600, width=600,
                  margin=go.layout.Margin(l=0, r=0, b=30, t=30))

```
$f_1$ besitzt ein Minimum, $f_2$ sogar unendlich viele (der "Rinnenboden" ist überall gleich hoch). Die beiden Funktionen $f_3$ und $f_4$ besitzen sogenannte *Sattelpunkte* und sind nach unten und nach oben unbeschränkt.


## Standardform und kritische Punkte
Wir haben nun Beispiele für unterschiedliche kritische Punkte von quadratischen Funktionen beobachtet. Kann man das einer quadratischen Funktion vielleicht im Voraus ansehen, welche und wie viele kritischen Punkte sie hat? Ja, indem man die quadratische Funktion auf eine Standardform bringt, aus der sich alle wichtigen Eigenschaften des quadratischen Optimierungsproblems (mit Hilfe von etwas linearer Algebra) bestimmen lassen.

Allgemein lässt sich *jede* quadratische Funktion $f:\R^n\rightarrow \R$ in $n$ Variablen auf folgende Form bringen:
\begin{align*}
f(x_1,x_2,\dots,x_n)=\frac{1}{2}\v x^T\v A\v x+\v b^T\v x+c,
\end{align*}
wobei $\v A\in\R^{n\times n}$ eine symmetrische Matrix ist, $\v b\in\R^n$ ein Vektor und $c\in\R$ eine reelle Zahl. 

```{prf:example} Quadratische Funktion in Standardform I
:label: qpex1

Die Funktion 
\begin{align*}
f(x,y)=3x^2+y^2
\end{align*}
lässt sich schreiben als
\begin{align*}
f(x,y)=\frac{1}{2}(x,y) \bmat 6 & 0\\0&2\emat  \bmat x\\y\emat   + (0,0)\bmat x\\y\emat  +0.
\end{align*}
```
```{prf:example} Quadratische Funktion in Standardform II
:label: qpex2

Die Funktion 
\begin{align*}
f(x,y)=x^2+y^2+xy+3x-1
\end{align*}
lässt sich schreiben als
\begin{align*}
f(x,y)=\frac{1}{2}(x,y) \bmat  2 & 1\\ 1 & 2\emat   \bmat  x\\y\emat  +(3,0) \bmat  x\\y\emat  +(-1),
\end{align*}
```
Der Vorteil dieser Darstellung wird deutlich wenn man aus der allgemeinen Form Gradienten und Hessematrix bestimmt. Es gilt nämlich
```{math}
:label: eq:grad-qp
\nabla f(x_1,x_2,\dots,x_n) = \v A\v x + \v b
```
Dies wäre für {prf:ref}`qpex1`
\begin{align*}
\nabla f(x,y) = \bmat  6 & 0\\ 0 & 2\emat   \bmat  x\\y\emat   
\end{align*}
und für {prf:ref}`qpex2`
\begin{align*}
\nabla f(x,y) = \bmat  2 & 1\\ 1 & 2\emat   \bmat  x\\y\emat  + \bmat  3\\0\emat   
\end{align*}

Die Hessematrix ist einfach die Matrix $\v A$, was man sieht, wenn man {eq}`eq:grad-qp` nach $\v x$ ableitet.
Damit können wir unter Verwendung von {prf:ref}`thm:OBn` die kritischen Punkte quadratischer Funktionen vollständig charakterisieren.
```{prf:theorem} Kritische Punkte quadratischer Funktionen
Die kritischen Punkte $\v x^*$ der quadratischen Funktion
\begin{align*}
f(x_1,x_2,\dots,x_n)=\frac{1}{2}\v x^T\v A\v x+\v b^T\v x+c,
\end{align*}
sind Lösungen des linearen Gleichungssystems
\begin{align*}
\v A\v x=-\v b.
\end{align*}
Falls $\v A$ invertierbar ist, ist der einzige kritische Punkt $\v x^*=-\v A^{-1}\v b$.

Falls $\v A$ positiv definit ist (nur positive Eigenwerte), ist $\v x^*$ ein globales *Minimum* von $f$.

Falls $\v A$ negativ definit ist (nur negative Eigenwerte), ist $\v x^*$ ein globales *Maximum* von $f$.

Falls $\v A$ indefinit ist (positive und negative Eigenwerte), ist $\v x^*$ weder Minimum noch Maximum, sondern ein *Sattelpunkt*.
```

```{prf:example}
Der kritische Punkt der Funktion
\begin{align*}
f:\R²\rightarrow \R,\quad f(\v x)=\frac{1}{2}\bmat x_1&x_2\emat \bmat 2 & 0\\0& 4\emat\bmat x_1\\x_2\emat+\bmat 1&0\emat\bmat x_1\\x_2\emat+4,
\end{align*}
ist gegeben als Lösung des linearen Gleichungssystems
\begin{align*}
\bmat 2 & 0\\0& 4\emat\bmat x_1\\x_2\emat = -\bmat 1\\0\emat
\end{align*}
Als Lösung ergibt sich $x^*=\bmat -\frac{1}{2},0\emat$. Da die Matrix $\bmat 2 & 0\\0& 4\emat$ positiv definit ist, ist $x^*$ ein globales Minimum von $f$.
```

```{prf:example}
Die Funktion
\begin{align*}
f:\R²\rightarrow \R,\quad f(\v x)=\frac{1}{2}\bmat x_1&x_2\emat \bmat 2 & 0\\0& 0\emat\bmat x_1\\x_2\emat+\bmat 0&2\emat\bmat x_1\\x_2\emat+3,
\end{align*}
hat keine kritischen Punkte, da das Gleichungssystem
\begin{align*}
\bmat 2 & 0\\0& 0\emat\bmat x_1\\x_2\emat = -\bmat 0\\2\emat
\end{align*}
keine Lösung hat.
```


%## Anwendung: Umsatzmaximierung im Einproduktfall
% TODO


%## Anwendung: Training von linearen Regressionsmodellen
% TODO


%## Anwendung: Ridge Regression
% TODO


<!-- ## Grundlagen der beschränkten Optimierung


### Gleichungsbeschränkte Optimierung

### Ungleichungsbeschränkte Optimierung
````{prf:example} Aufstellen der KKT-Bedingungen
:label: example:KKT

Gegeben sei das Optimierungsproblem

\begin{align*}
\min_{x,y \in \mathbb{R}} \quad & \frac{1}{2}(x-2)^2+\frac{1}{2}(y-\frac{1}{2})^2 \\
\text{s.t.} \quad & (x+1)^{-1}-y-\frac{1}{4}\geq 0\\
& x\geq 0\\
& y\geq 0
\end{align*}

Wir stellen dafür nun die KKT-Bedingungen auf. Dazu benötigen wir die Lagrange-Funktion, bei der wir für jede Nebenbedingung einen Lagrange-Multiplikator $\mu_i$ einführen:

\begin{align*}
\mathcal{L}(x,y,\mu_1,\mu_2,\mu_3) = \frac{1}{2}(x-2)^2+\frac{1}{2}(y-\frac{1}{2})^2 - \mu_1\left((x+1)^{-1}-y-\frac{1}{4}\right) - \mu_2 x - \mu_3 y
\end{align*}

Nun können wir die KKT-Bedingungen aufstellen. Dies sind die folgenden Gruppen von Gleichungen bzw. Ungleichungen (insgesamt 5 Gleichungen und 6 Ungleichungen):

1. Der Gradient der Lagrange-Funktion nach $x$ und $y$ muss $0$ sein (Stationarität):  
    \begin{align*}
    \frac{\partial \mathcal{L}}{\partial x} &= x-2 + \frac{\mu_1}{(x+1)^2} - \mu_2 = 0\\
    \frac{\partial \mathcal{L}}{\partial y} &= y-\frac{1}{2} + \mu_1 - \mu_3 = 0
    \end{align*}
2. Die Nebenbedingungen müssen erfüllt sein (Zulässigkeit):  
    \begin{align*}
    (x+1)^{-1}-y-\frac{1}{4}&\geq 0\\
    x&\geq 0\\
    y&\geq 0
    \end{align*}  
3. Die Lagrange-Multiplikatoren müssen nicht-negativ sein (Nicht-Negativität):  
    \begin{align*}
    \mu_1 &\geq 0\\
    \mu_2 &\geq 0\\
    \mu_3 &\geq 0
    \end{align*}  
4. Entweder muss die Ungleichungsnebenbedingung gleich $0$ sein oder der zugehörige Lagrange-Multiplikator (Komplementarität):  
    \begin{align*}
    \mu_1\left((x+1)^{-1}-y-\frac{1}{4}\right) &= 0\\
    \mu_2 x &= 0\\
    \mu_3 y &= 0
    \end{align*}

Die Schwierigkeit, einen KKT-Punkt (also einen Punkt, der alle Bedingungen erfüllt) zu finden, liegt darin, dass wir es mit einem System aus Gleichungen und *Ungleichungen* zu tun haben. Wir können nicht einfach die Gleichungen nach $x, y$ und $\mu_1,\mu_2,\mu_3$ auflösen. Stattdessen müssen wir Fallunterscheidungen machen, je nachdem, ob die Ungleichungsnebenbedingungen aktiv sind (d.h. es gilt $=$) oder nicht (d.h. es gilt $>$).

Praktisch müsste man alle $2^3$ Möglichkeiten durchgehen, welche der drei Ungleichungsnebenbedingungen mit Gleichheit erfüllt sind, also *aktiv* sind. Bei den Ungleichungen, die $>0$ sind (die *inaktiven* Ungleichungsnebenbedingungen) muss der zugehörige Lagrange-Multiplikator $0$ sein, damit Komplementarität erfüllt ist. 

Für die aktiven Ungleichungen muss man nun testweise ein Gleichungssystem lösen. Nach der Lösung muss man das Vorzeichen der $\mu_1,\mu_2,\mu_3$ überprüfen: Nur wenn diese nicht negativ sind, ist die Nicht-Negativitätsbedingung der KKT-Bedingungen erfüllt und der so berechnete Punkt ist ein KKT-Punkt. Ist das nicht der Fall, muss eine andere Kombination von aktiven Ungleichungsnebenbedingungen getestet werden.
````
 -->
%## Anwendung: Support Vector Maschinen