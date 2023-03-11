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

(sec:gradientenverfahren)=
# Gradientenverfahren
In diesem Abschnitt schauen wir uns Details zu Gradientenverfahren an. Wir wollen das weiterhin anhand von einfachen, niedrig-dimensionalen (1d und 2d) Beispielen tun, um die Konzepte und Probleme der Verfahren zu verstehen. 

Behalten Sie aber im Hinterkopf, dass die eigentliche Motivation von aktuellen Gradientenverfahren die Lösung von sehr schwierigen, hochdimensionalen Problemen ist. Gradientenverfahren werden z.B. dazu eingesetzt moderne KI-Systeme mit vielen Millionen bzw. Milliarden von Variablen zu trainieren.

Das big picture: Wir sind nach wie vor an Optimierungsproblemen der Form
\begin{align*}
\min_{\v x\in\R^n} f(\v x)
\end{align*}
interessiert. Wir begnügen uns dabei mit *lokalen* Lösungen (von denen wir für streng konvexe Funktionen immerhin wissen, dass sie auch global sind). 

````{note}
Die Aufgabe, globale Minima für allgemeine, nicht-konvexe Funktionen $f$ zu finden ist um ein vielfaches schwerer. Es gibt sog. *globale Optimierungsverfahren*, doch diese funktionieren nur für vergleichsweise kleine Probleme. In dieser Vorlesung behandeln wir sie nicht. In {ref}`sec:ml` werden wir sehen, dass der Verzicht auf globale Lösungen zumindest im Bereich maschinelles Lernen kein großes Problem ist.
````


## Allgemeines Framework
Der in {ref}`sec:gd-preview` vorgestellte Gradientenabstieg ist ein Vertreter einer ganzen Familie von Gradientenverfahren. Sie folgen alle einem bestimmten Aufbau, unterscheiden sich aber in der Ausgestaltung der einzelnen Schritte. Wie zuvor bezeichnen wir mit $k$ unseren Iterationszähler und wir schreiben $^{[k]}$ an jede Größe, die sich von Iteration zu Iteration ändern kann.

Bevor das allgemeine Verfahren aufschreiben, schauen wir uns zunächst noch einmal an, wie wir begründet haben, dass der Gradientenabstieg funktioniert. Wir haben das Taylor-Polynom erster Ordnung am Entwicklungspunkt $\v x^{[k]}$, der aktuellen Iterierten, aufgestellt (man sagt auch: die Funktion $f$ *linearisiert*) und damit den Funktionswert an der neuen Iterierten angenähert.

\begin{align*}
f(\v x^{[k+1]})=f(\v x^{[k]}+\v d^{[k]})&\approx f(\v x^{[k]})+\nabla f(\v x^{[k]})\v d^{[k]}\\
&=f(\v x^{[k]})-\alpha^{[k]}\nabla f(\v x^{[k]})\nabla f(\v x^{[k]})^T\\
&=f(\v x^{[k]})-\underbrace{\alpha^{[k]}\norm{\nabla f(\v x^{[k]})}^2}_{>0}
\end{align*}
In Worten: Der Funktionswert am neuen Punkt $\v x^{[k+1]}$ ist kleiner als am aktuellen Punkt $\v x^{[k]}$, wenn als Schritt $\v d^{[k]}=-\alpha^{[k]}\nabla f(\v x^{[k]})$ gewählt wird (mit einer geeignete Schrittweite $\alpha^{[k]}>0$). Wenn man für $\v d^{[k]}$ den Gradienten wählt, kann auf jeden Fall ein Abstieg erzielt werden.

An der ersten Gleichung sieht man aber auch, dass eigentlich nur $\nabla f(\v x^{[k]})\v d^{[k]}<0$ gelten muss, um zu garantieren, dass sich der Funktionswert verringert (Voraussetzung nach wie vor: man bleibt nahe genug bei $\v x^{[k]}$, so dass die Linearisierung eine ausreichend gute Approximation ist). Interessant:  $\nabla f(\v x^{[k]})\v d^{[k]}$ ist die Richtungsableitung in Richtung $\v d^{[k]}$, siehe {ref}`sec:richtung`. Man nennt *jedes* $\v d^{[k]}$, für das gilt $\nabla f(\v x^{[k]})\v d^{[k]}<0$ eine *Abstiegsrichtung*. 

Wenn $\v d^{[k]}=\nabla f(\v x^{[k]})$ gewählt wird, so liefert dies zwar den kleinstmöglichen Wert $\nabla f(\v x^{[k]})\v d^{[k]}$, siehe {ref}`sec:interpretation`, aber die Linearisierung ist evtl. nur in einer sehr kleinen Umgebung von $\v x^{[k]}$ gültig. Oft ist es klüger, nicht den aktuell steilsten Abstieg zu wählen um längerfristig eine bessere Reduktion der Funktion zu finden.

Zur Notation : wir ziehen ab jetzt den skalaren Faktor $\alpha^{[k]}$ aus dem $\v d^{[k]}$ heraus, schreiben also $\v x^{[k+1]}=\v x^{[k]}+\alpha^{[k]}\v d^{[k]}$ statt $\v x^{[k+1]}=\v x^{[k]}+\v d^{[k]}$.

````{prf:algorithm} Allgemeines Framework Abstiegsverfahren
Gegeben: 
: Differenzierbare Funktion $f:\R^n\rightarrow\R$.

Gesucht: 
: Lokales Minimum von $f$.

**Algorithmus**:

Starte mit initialer Schätzung $\v x^{[0]}$, setze $k=0$.

Für $k=0,1,2,\dots$:
1. Überprüfe, ob $\v x^{[k]}$ die **Abbruchbedingung** erfüllt. 
    - Falls ja: Abbruch mit Lösung $\v x^{[k]}$
    - Falls nein: gehe zu Schritt 2.
2. Bestimme **Abstiegsrichtung** $\v d^{[k]}$ unter Verwendung lokaler Information (z.B. Gradient, Hessematrix)
3. Bestimme **Schrittweite** $\alpha^{[k]}$.
4. Berechne neue Iterierte $\v x^{[k+1]}=\v x^{[k]}+\alpha^{[k]}\v d^{[k]}$.
````
Es gibt viele Abstiegsverfahren, die sich darin unterscheiden, wie die Abstiegsrichtung $\v d$ und die Schrittweite $\alpha$ bestimmt werden. Außerdem gibt es unterschiedliche Abbruchbedingungen. Wir schauen uns diese Aspekte in den folgenden Abschnitten an.


## Abbruchbedingungen
Irgendwie muss man entscheiden, wann die Iterationen eines Gradientenverfahrens abbrechen sollen. Idealerweise würde man dann und nur dann abbrechen, wenn tatsächlich ein lokales Minimum erreicht ist (oder das Verfahren divergiert). Das ist aber aus mehreren Gründen problematisch:
1. Gradientenverfahren finden ein Minimum nur näherungsweise, selbst wenn mit exakter Arithmetik gerechnet würde.
2. Moderne Computer verwenden Arithmetik von endlicher Präzision. Neben dem approximativen Charakter des (exakten) Gradientenverfahren wird man schon allein deshalb nicht erwarten können, ein Minimum exakt zu treffen, sondern wenn überhaupt, dann nur bis auf Maschinengenauigkeit (normalerweise ungefähr $10^{-16}$).
3. Wenn man die beiden obigen Punkte akzeptiert, kann es trotzdem sehr (!) lange dauern, bis das Verfahren in der Nähe eines Minimums landet.

In der Praxis werden oft folgende Abbruchbedingungen benutzt.

Maximale Anzahl Iterationen
: Die Abbruchbedingung ist erfüllt, wenn $k>\hyper{k_{max}}$, wobei $\hyper{k_{max}}$ vorher festgelegt wird (alternativ wird eine maximale Zeit festgelegt, nach der das Verfahren abbricht). Beispiele: Abbruch nach 100 Iterationen. Abbruch wenn eine Stunde Rechenzeit überschritten wurde. Der Nachteil dieses Kriteriums ist natürlich, dass man überhaupt keine Garantie hat, dass das Verfahren in der Nähe einer Lösung ist.

Absolute Verbesserung
: Die Abbruchbedingung ist erfüllt, wenn der Funktionswert sich von einem zum nächsten Schritt weniger ändert als eine vorher festgelegte Schranke $\hyper{\epsilon_{abs}}$: 
  \begin{align*}
  \left|f(\v x^{[k]})-f(\v x^{[k+1]})\right|<\hyper{\epsilon_{abs}}
  \end{align*} 
  $\hyper{\epsilon_{abs}}$ ist in der Regel eine "kleine" Zahl, z.B. im Bereich $10^{-8}-10^{-4}$.

Relative Verbesserung
: Die Abbruchbedingung ist erfüllt, wenn die Verbesserung relativ zum aktuellen Funktionswert kleiner als eine vorher festgelegte Schranke $\hyper{\epsilon_{rel}}$ ist: 
  \begin{align*}
  \frac{\left|f(\v x^{[k]})-f(\v x^{[k+1]})\right|}{\left|f(\v x^{[k]})\right|}<\hyper{\epsilon_{rel}}
  \end{align*}
  $\hyper{\epsilon_{rel}}$ ist in der Regel eine "kleine" Zahl, z.B. im Bereich $10^{-8}-10^{-4}$.

Norm des Gradienten
: Die Abbruchbedingung ist erfüllt, wenn die Norm des Gradienten kleiner als eine vorher festgelegte Schranke $\hyper{\epsilon_{grad}}$ ist:
  \begin{align*}
  \norm{\nabla f(\v x^{[k]})}<\hyper{\epsilon_{grad}}
  \end{align*}
  Die Idee dahinter ist, dass an einem Minimum die Ableitung $\v 0$ ist. Ähnlich wie bei den beiden vorherigen Kriterien ist $\hyper{\epsilon_{grad}}$ eine "kleine" Zahl, z.B. im Bereich $10^{-8}-10^{-4}$, die vorab gewählt werden muss.

````{note}
Die Parameter $\hyper{\epsilon_{abs}}, \hyper{\epsilon_{rel}}, \hyper{\epsilon_{grad}}$ und $\hyper{k_{max}}$ sind Beispiele für *Hyperparameter* des Verfahren. Ähnlich wie in Texten über maschinelles Lernen bezeichnet der Begriff Hyperparameter hier eine Größe, die *vor* dem Ausführen des Verfahrens gewählt werden muss. Die Wahl der Hyperparameter beeinflusst die Performance des Verfahrens und die Qualität der Lösungen. Wie die Abhängigkeit eines Verfahrens von einem bestimmten Parameter ist ("Was passiert, wenn ich Hyperparameter "X" um Faktor 10 erhöhe?") lässt sich oft nur schwer vorhersagen. Jedoch gibt es für einige wichtige Hyperparameter Erfahrungswerte.

Alle Verfahren, die wir in dieser Vorlesung kennenlernen besitzen Hyperparameter. Um sie von den anderen Symbolen abzuheben, werden Sie $\hyper{\text{farbig}}$ hervorgehoben.
```` 

Die Wahl der Hyperparameter der Abbruchbedingungen ist ein Trade-Off zwischen Laufzeit und Genauigkeit bzw. Robustheit des Verfahrens. Wird der Parameter $\hyper{\epsilon}$ sehr klein gewählt, z.B. $10^{-8}$, so wird das Verfahren viel länger brauchen als, wenn der Parameter z.B. $10^{-4}$ ist. Andererseits ist man bei einem größeren Wert wie $10^{-4}$ weiter vom Minimum entfernt. Außerdem ist die Wahrscheinlichkeit höher, dass man gar nicht in der Nähe eines Minimums ist, sondern nur in einem Bereich der Funktion, in der die Steigung gering (aber nicht $0$) ist. Speziell die Hyperparameter $\hyper{\epsilon}$ nennt man auch *Abbruchtoleranz*.

Wir schauen uns ein Beispiel an um den Unterschied zwischen den drei Kriterien absolute Verbesserung, relative Verbesserung und Norm des Gradienten zu verstehen. Wir betrachten die beiden Funktionen
\begin{align*}
f_1(x,y)&=x^2+y^2\\
f_2(x,y)&=0.2x^2+0.2y^2=0.2f_1(x,y)
\end{align*}
Beide haben ein globales Minimum bei $(0,0)$. So sehen die Funktionen aus:
````{code-cell} ipython3
:tags: [hide-input]
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

x = np.linspace(-2,2,100)
y = np.linspace(-2,2,100)
X,Y = np.meshgrid(x,y)
z = X**2 + Y**2
z2 = 0.2*(X**2 + Y**2)

fig = make_subplots(rows=1, cols=2,
    specs=[[{'type': 'surface'}, {'type': 'surface'}]])

fig.add_trace(go.Surface(x=x,y=y,z=z, colorscale="Blues", showscale=False),
            row=1, col=1)
fig.add_trace(go.Surface(x=x,y=y,z=z2, colorscale="Blues", showscale=False),
            row=1, col=2)
fig.update_layout( height=300, margin=go.layout.Margin(l=0, r=0, b=0, t=0))

````

Wir schauen uns an, wie die drei Abbruchbedingungen einen Schritt für ein Gradientenverfahren bewerten würde. Die Details des Verfahrens sind hier nicht wichtig, wir möchten nur verstehen, wie die Abbruchbedingungen funktionieren.
Angenommen, unser Verfahren für die beiden Funktion $f_1$ und $f_2$ macht einen Schritt von $\bmat 1\\1\emat$ nach $\bmat 0.8\\0.8\emat$. In beiden Fällen wäre also der gleiche Fortschritt in Richtung der Lösung erzielt worden.

Wir schauen uns nun die linken Seiten der Abbruchbedingungen an, an Hand derer entschieden wird, ob das Verfahren abbricht.

Absolute Verbesserung
: Zur Bewertung braucht man die Funktionswerte vor und nach dem Schritt, also bei $\bmat 1\\1\emat$ und $\bmat 0.8\\0.8\emat$.
  \begin{align*}
  f_1(1,1)=1^2+1^2=2,\quad f_1(0.8,0.8)=0.8^2+0.8^2=1.28
  \end{align*}
  Die absolute erzielte Verbesserung für $f_1$ wäre also $f_1(1,1)-f(0.8,0.8)=0.72$.
  Eine ähnliche Rechnung für $f_2 ergibt
  \begin{align*}
  f_2(1,1)=0.2\cdot 1^2+0.2\cdot 1^2=0.4,\quad f_2(0.8,0.8)=0.2\cdot 0.8^2+0.2\cdot 0.8^2=0.256
  \end{align*}
  Die absolute erzielte Verbesserung für $f_2$ wäre also $f_1(1,1)-f(0.8,0.8)=0.144$. Wenn also z.B. $\hyper{\epsilon_{abs}}=0.2$ gewählt worden wäre würde das Verfahren für $f_1$ noch weiterlaufen, für $f_2$ aber nicht, da weniger absoluter Fortschritt erzielt wurde (was aber nur an der Skalierung der Funktion liegt).

Norm des Gradienten
: Zur Bewertung müssen wir den Gradienten am neuen Punkt $\bmat 0.8\\0.8\emat$ auswerten (es kommt gar nicht auf die Länge des Schrittes an):
  \begin{align*}
  \norm{\nabla f_1(0.8,0.8)}&=\norm{\bmat 2\cdot 0.8\\2\cdot 0.8\emat}=\sqrt{1.6^2+1.6^2}\approx 2.26\\
  \norm{\nabla f_2(0.8,0.8)}&=\norm{\bmat 0.4\cdot 0.8\\0.4\cdot 0.8\emat}=\sqrt{0.32^2+0.32^2}\approx 0.45
  \end{align*}
  Auch hier würde das Verfahren bei gleicher Toleranz bei $f_2$ vorher abbrechen als bei $f_1$, weil die Norm des Gradienten kleiner ist, also näher an Null, was ja die notwendige Bedingung für ein Minimum ist.

Beide Kriterien sind nicht *skalierungsinvariant*, d.h. das Verfahren würde ---bei gegebenem Werten $\hyper{\epsilon_{abs}}$ bzw. $\hyper{\epsilon_{grad}}$--- an unterschiedlichen Stellen abbrechen, obwohl $f_1$ und $f_2$ lediglich Vielfache voneinander sind. Anders bei der relativen Verbesserung.

Relative Verbesserung
: Wir berechnen die linke Seite mit den oben berechneten Funktionswerten $f_i(1,1)$ und $f_i(0.8,0.8)$:
  \begin{align*}
  \frac{f_1(1,1)-f_1(0.8,0.8)}{f_1(1,1)}&=\frac{0.72}{2}=0.36\\
  \frac{f_2(1,1)-f_2(0.8,0.8)}{f_1(1,1)}&=\frac{0.144}{0.4}=0.36
  \end{align*}
  Das Kriterium zur relativen Verbesserung ist skalierungsinvariant. Das heißt, durch Multiplizieren der Zielfunktion mit einer Zahl ändert sich das Verhalten des Gradientenverfahrens nicht. Aber auch dieses Kriterium hat seine Tücken: wenn die Funktionswerte zufällig Null sind (oder sehr nahe an Null liegen), so wird die Division numerisch instabil.

In der Praxis werden alle Kriterien eingesetzt. Wie bei allen Hyperparametern empfiehlt es sich, zunächst auf default-Werte aus der Implementierung bzw. der Literatur zurückzugreifen.

## Wahl der Schrittweite 
### Liniensuche
### Näherungsweise Liniensuche
### Dämpfung

## Probleme des Gradientenabstiegs

## Gradientenabstieg mit Momentum
### Nesterov Modifikation

