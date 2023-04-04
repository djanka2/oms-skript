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
% # Seaborn color palette:
% # '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
% # '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'

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

Bevor das allgemeine Verfahren aufschreiben, schauen wir uns zunächst noch einmal die Begründung, warum der Gradientenabstieg funktioniert, an. Wir haben das Taylor-Polynom erster Ordnung am Entwicklungspunkt $\v x^{[k]}$, der aktuellen Iterierten, aufgestellt (man sagt auch: die Funktion $f$ *linearisiert*) und damit den Funktionswert an der neuen Iterierten angenähert.

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
:label: alg:gd_allgemein
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


````{important}
Neben dem Gradientenabstieg gibt es viele weitere Abstiegsverfahren, die nach einem ähnlichen Prinzip funktionieren. Sie unterscheiden sich im wesentlichen in folgenden beiden Punkten:
1. Wie wird die Abstiegsrichtung $\v d$ bestimmt?
2. Wie wird die Schrittweite $\alpha$ bestimmt?
````
Außerdem gibt es unterschiedliche Abbruchbedingungen, die das Verhalten der Verfahren beeinflussen. Wir schauen uns diese Aspekte in den folgenden Abschnitten an. Zunächst jedoch schauen wir uns das Verfahren in Aktion an.

### Implementierung und Visualisierung des Verfahrens
Eine einfache Implementierung des Verfahrens (hier mit fest gewählter Schrittweite) in Python sieht so aus:
```{code-cell} ipython3
import numpy as np

def f(x):
    """ Function to minimize """
    return 4*x[0]**2 + x[1]**2
    
def df(x):
    """ Derivative of the function to minimize """
    return np.array([8*x[0], 2*x[1]])

def gd(func, derv, alpha, x0, n_steps):
    """ Perform n_steps iterations of gradient descent with steplength alpha and return iterates """
    x_history = [x0]
    x = x0
    for k in range(n_steps):
        dx = derv(x)
        x = x - alpha * dx
        x_history.append(x)

    return np.array(x_history)

x0 = np.array([-1,1])
x_history = gd(func=f, derv=df, alpha=0.01, x0=x0, n_steps=30)
```

Das Gradientenverfahren in Aktion: die Iterierten $x^{[k]}$, die das Gradientenverfahren (hier für die Funktion $f(x,y)=4x^2+y^2$) erzeugt, sind eine Folge von Vektoren. Visualisieren kann man das Ganze für Funktionen zweier Variablen wie folgt:
```{code-cell} ipython3
:tags: [hide-input]
import numpy as np
import plotly.graph_objects as go

def plot_iterates(iterates, func):
    """Plot objective function func as contour plot and visualize iterates"""
    iterates_T = iterates.T
    x1_min = min(0,np.min(iterates_T[0]))-0.1
    x1_max = max(0,np.max(iterates_T[0]))+0.1
    x2_min = min(0,np.min(iterates_T[1]))-0.1
    x2_max = max(0,np.max(iterates_T[1]))+0.1

    x1_range = np.linspace(x1_min, x1_max, 100)
    x2_range = np.linspace(x2_min, x2_max, 100)
    A = np.meshgrid(x1_range, x2_range)
    Z = func(A)

    n_iter = len(iterates_T[1])
    fig = go.Figure(data=[go.Contour(z=Z, x=x1_range, y=x2_range, 
                                     colorscale="Blues",
                                     contours=dict(start=0,
                                                   end=10,
                                                   size=0.2,
                                                    ))])

    fig.add_scatter(x=iterates_T[0], y=iterates_T[1], 
                    mode='lines+markers', name='iterates',
                    marker=dict(color=np.arange(n_iter), cmin=0, cmax=n_iter, size=7, colorbar=dict(title="k", x=1.15), 
                    colorscale="Oranges"),
                    line=dict(color="grey")
                   )

    fig.show()


def f(x):
    """ Function to minimize """
    return 4*x[0]**2 + x[1]**2
    
def df(x):
    """ Derivative of the function to minimize """
    return np.array([8*x[0], 2*x[1]])

def gd(func, derv, alpha, x0, n_steps):
    """ Perform n_steps iterations of gradient descent with steplength alpha and return iterates """
    x_history = [x0]
    x = x0
    for k in range(n_steps):
        dx = derv(x)
        x = x - alpha * dx
        x_history.append(x)

    return np.array(x_history)

x0 = np.array([-1,1])
x_history = gd(func=f, derv=df, alpha=0.01, x0=x0, n_steps=30)
plot_iterates(x_history, f)
```


## Wahl der Schrittweite 
In diesem Abschnitt schauen wir uns verschiedene Strategien an, die Schrittweite in jeder Iteration $k$, $\alpha^{[k]}$, zu wählen. Dazu nehmen wir an, wir hätten eine Abstiegsrichtung $\v d^{[k]}$ gefunden, also eine Richtung, für die gilt $ \nabla f(\v x^{[k]})\v d^{[k]}<0$. Das kann, muss aber nicht, der negative Gradient sein, also $\v d^{[k]}=-\nabla f(\v x^{[k]})$. Wir werden später noch andere Möglichkeiten kennenlernen.

Zunächst schauen wir uns das grundsätzliche Verhalten bei unterschiedlichen Schrittweiten anhand eines simplen Beispiels an. Wir minimieren die Funktion $f(x)=x^2$ mittels Gradientenabstieg. Der folgende Plot zeigt die ersten 15 Iterationen für vier Werte von $\alpha$, nämlich $\alpha\in\{0.01,0.1,0.9,1.1\}$.
```{code-cell} ipython3
:tags: [hide-input]
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def f(x):
    """ Function to minimize """
    return x**2

def df(x):
    """ Derivative of the function to minimize """
    return 2*x

def gd(func, derv, alpha, x0, n_steps):
    """ Perform n_steps iterations of gradient descent with steplength alpha and return iterates """
    x_history = [x0]
    x = x0
    for k in range(n_steps):
        dx = derv(x)
        x = x - alpha * dx
        x_history.append(x)

    return np.array(x_history)

x_history1 = gd(func=f, derv=df, alpha=0.01, x0=3.0, n_steps=15)
x_history2 = gd(func=f, derv=df, alpha=0.1, x0=3.0, n_steps=15)
x_history3 = gd(func=f, derv=df, alpha=0.9, x0=3.0, n_steps=15)
x_history4 = gd(func=f, derv=df, alpha=1.1, x0=3.0, n_steps=15)

x = np.linspace(-4,4,100)

fig = make_subplots(rows=2, cols=2)
fig.add_trace(go.Scatter(x=x, y=f(x), name="f(x)=x²", showlegend=False,
                         mode="lines", 
                         marker_color='#1f77b4'), row=1, col=1)
fig.add_trace(go.Scatter(x=x_history1, y=f(x_history1), name="alpha=0.01",
                         mode="lines+markers", 
                         marker_color='#ff7f0e'), row=1, col=1)

fig.add_trace(go.Scatter(x=x, y=f(x), name="f(x)=x²", showlegend=False,
                         mode="lines", 
                         marker_color='#1f77b4'), row=1, col=2)
fig.add_trace(go.Scatter(x=x_history2, y=f(x_history2), name="alpha=0.1", 
                         mode="lines+markers", 
                         marker_color='#2ca02c'), row=1, col=2)

fig.add_trace(go.Scatter(x=x, y=f(x), name="f(x)=x²", showlegend=False,
                         mode="lines", 
                         marker_color='#1f77b4'), row=2, col=1)
fig.add_trace(go.Scatter(x=x_history3, y=f(x_history3), name="alpha=0.9",
                         mode="lines+markers", 
                         marker_color='#d62728'), row=2, col=1)

fig.add_trace(go.Scatter(x=x, y=f(x), name="f(x)=x²", showlegend=False,
                         mode="lines", 
                         marker_color='#1f77b4'), row=2, col=2)
fig.add_trace(go.Scatter(x=x_history4, y=f(x_history4), name="alpha=1.1",
                         mode="lines+markers", 
                         marker_color='#9467bd'), row=2, col=2)
fig.show()
```
An dem Beispiel lassen sich folgende, auch für kompliziertere Beispiele oft zutreffende, Beobachtungen machen:
- Wenn die Schrittweite zu klein ist, ist der Fortschritt in Richtung der Lösung gering (Beispiel: $\alpha=0.01$).
- Wenn die Schrittweite zu groß ist, divergiert das Verfahren, d.h. es entfernt sich von der Lösung (Beispiel: $\alpha=1.1$)
- Das Verfahren kann konvergieren, indem es sich "Stück für Stück" auf die Lösung zubewegt (Beispiel: $\alpha=0.1$ und $\alpha=0.01$) oder auch, indem es "um die Lösung herum fluktuiert" (Beispiel: $\alpha=0.9$).

Wichtig: Die konkreten Werte für $\alpha$ (hier $\alpha\in\{0.01,0.1,0.9,1.1\}$) sind von der zu minimierenden Funktion $f$ abhängig. Für die Funktion $f(x)=x^2$ (und den Startwert $x^{[0]}=3$) ist $\alpha=0.01$ anscheinend zu klein. Für eine andere Funktion kann $\alpha=0.01$ aber auch zu groß sein.

In dem Beispiel wurde die Schrittweite konstant gewählt, also $\alpha^{[k]}=\alpha$ für jede Iteration $k$. In der Tat ist eine konstante Schrittweite in der Praxis eine gängige Option, oft trifft man sie in Form von $10$er Potenzen, z.B. $\alpha=10^{-3}, \alpha=10^{-1}$ oder allgemein $\alpha=10^{\gamma}$, wobei $\gamma$ eine einstellige, oft negative ganze Zahl ist. Die Kunst ist es, eine Schrittweite zu finden, die bestmöglichen Fortschritt in Richtung der (unbekannten) Lösung macht. Für konstante Schrittweiten bedeutet das oft, die *größtmögliche* Schrittweite zu finden, so dass das Verfahren *nicht* divergiert.

Im folgenden schauen wir uns weitere gängige Möglichkeiten vor, die Schrittweite zu wählen.

### Dämpfung
Eine weitere beliebte Strategie ist die gedämpfte Schrittweite. ier wird, ausgehend von einer Startschrittweite, die Schrittweite in jedem Schritt (oder allgemeiner alle $m$ Schritte) reduziert.
Typische Dämpfungsstrategien sind:
- Inverse Dämpfung: $\alpha^{[k]}=\frac{\hyper{\alpha_0}}{k}$.
- Exponentielle Dämpfung: $\alpha^{[k+1]}=\hyper{\gamma}\alpha^{[k]}=\hyper{\gamma}^k\hyper{\alpha_0}$. Mit dem Hyperparameter $\hyper{\gamma}\in(0,1)$: je näher $\hyper{\gamma}$ an $1$ ist, desto weniger wird die Schrittweite in jedem Schritt reduziert. Wenn $\hyper{\gamma}$ nahe $0$ ist, wird die Schrittweite nach wenigen Iterationen sehr klein.

In beiden Fällen ist die Startschrittweite $\hyper{\alpha_0}\in\R$ ein Hyperparameter.

````{note}
Die Parameter $\hyper{\alpha_0} und \hyper{\gamma}$ sind Beispiele für *Hyperparameter* des Verfahrens. Ähnlich wie in Texten über maschinelles Lernen bezeichnet der Begriff Hyperparameter hier eine Größe, die *vor* dem Ausführen des Verfahrens gewählt werden muss. Die Wahl der Hyperparameter beeinflusst die Performance des Verfahrens und die Qualität der Lösungen. Wie die Abhängigkeit eines Verfahrens von einem bestimmten Parameter ist ("Was passiert, wenn ich Hyperparameter "X" um Faktor 10 erhöhe?") lässt sich oft nur schwer vorhersagen. Jedoch gibt es für einige wichtige Hyperparameter Erfahrungswerte.

Alle Verfahren, die wir in dieser Vorlesung kennenlernen, besitzen Hyperparameter. Um sie von den anderen Symbolen abzuheben, werden Sie $\hyper{\text{farbig}}$ hervorgehoben.
```` 

Die Motivation, eine gedämpfte Schrittweite zu verwenden ist, dass die Iterationen nicht "um die Lösung herum springen" bzw. oszillieren, sondern irgendwann, langsam aber sicher, in die Lösung "hineinlaufen". Wie so oft besteht ein Nachteil in der richtigen Wahl der Hyperparameter, wie durch folgendes Beispiel illustriert wird:

Es wird die exponentielle Dämpfungsstrategie mit $\hyper\gamma=0.9$ angewendet, die Schrittweite in einer Iteration $k+1$ wird also bestimmt durch:
\begin{align*}
\alpha^{[k+1]}=0.9^k\hyper{\alpha_0}
\end{align*}
Nun werden für $\hyper{\alpha_0}$ die Werte $0.2$ und $2$ getestet. Hier das Ergebnis der beiden Läufe:

```{figure} ./bilder/damped_stepsize.png
:width: 400px
```
Man sieht: Beim Wert $\hyper{\alpha_0}=0.2$ (blaue Kurve) werden die Schrittweiten zu schnell gedämpft, das Verfahren kommt nicht in die Nähe der Lösung. Beim Wert $\hyper{\alpha_0}=2$ (rote Kurve) werden die Schrittweiten zu langsam gedämpft. Die Iterierten fluktuieren stark oder divergieren.
 

### Exakte Liniensuche
Wie wir bisher gesehen haben, ist die Wahl der Schrittweite im Allgemeinen nicht so einfach und eine falsche Wahl kann schnell dazu führen, dass das Verfahren entweder sehr langsam oder überhaupt nicht konvergiert. 

Die Idee der Liniensuche ist nun, in jedem Schritt die *beste* Schrittweite, also diejenige, die dafür sorgt, dass die Zielfunktion am meisten reduziert wird. Das ist ein Optimierungsproblem innerhalb des Optimierungsproblems. 

Wie funktioniert das? Wenn wir eine Abstiegsrichtung $\v d^{[k]}$ identifiziert haben, schauen wir, wo die Funktion $f$ *entlang der Richtung* $\v d^{[k]}$ ihr Minimum annimmt. Das kann man sich etwa so vorstellen:

```{code-cell} ipython3
:tags: [hide-input]

import plotly.graph_objects as go
import numpy as np

# Die Funktion f als Surface Plot
x = np.linspace(-2,3,100)
y = np.linspace(-2,3,100)
X,Y = np.meshgrid(x,y)
z = 1/4*(X**4 + Y**4) - 1/3*(X**3+Y**3) - X**2 - Y**2 + 4

fig = go.Figure(go.Surface(x=x,y=y,z=z, colorscale="Blues", showscale=False))

# Aktuelle iterierte
xk = np.array([-1.5])
yk = np.array([-0.75])
z = 1/4*(xk**4 + yk**4) - 1/3*(xk**3+yk**3) - xk**2 - yk**2 + 4
fig.add_trace(go.Scatter3d(x=xk,y=yk,z=z, 
                           mode="markers", 
                           line=dict(width=5), 
                           marker_color="black", 
                           marker_symbol=['circle'], 
                           name="Aktuelle Iterierte"))

# Abstiegsrichtung d=(2,1)
d1 = 2
d2 = 1
# Konstruiere Gerade entlang der Abstiegsrichtung, die durch (xk,yk) geht
t = np.linspace(-0.15,1.25,100)
x = xk + t*(d1-xk)
y = yk + t*(d2-yk)
# Projektion der Gerade auf die Oberfläche
z = 1/4*(x**4 + y**4) - 1/3*(x**3+y**3) - x**2 - y**2 + 4

# x,y,z enthält jetzt die Koordinaten der Kurve f(xk+t*a). 
fig.add_trace(go.Scatter3d(x=x,y=y,z=z, 
                           mode="lines", marker_color='#ff7f0e',
                           line=dict(width=5),
                           name="Funktion für die Liniensuche"))


# Minimum entlang der Abstiegsrichtung
xk = np.array([7/3])
yk = np.array([7/6])
z = 1/4*(xk**4 + yk**4) - 1/3*(xk**3+yk**3) - xk**2 - yk**2 + 4
fig.add_trace(go.Scatter3d(x=xk,y=yk,z=z, 
                           mode="markers", 
                           line=dict(width=5), 
                           marker_color="red",
                           marker_symbol=['cross'], 
                           name="Nächste Iterierte"))

fig.update_layout( autosize=True,
                  margin=go.layout.Margin(l=0, r=0, b=0, t=0))
```
Der schwarze Punkt $(-1.5,-0.75)^T$ ist die aktuelle Iterierte $\v x^{[k]}$. Die Abstiegsrichtung $\v d^{[k]}=(2,1)^T$ wird auf die Oberfläche des Graphen projiziert und durch die Linie dargestellt. Eine Liniensuche fasst nun diese Linie als **eindimensionale** Funktion auf und sucht auf ihr das Minimum, im Graphen dargestellt durch das rote Kreuz[^fn:linesearch]. Das ist die nächste Iterierte $\v x^{[k+1]}$. Die Schrittweite $\alpha^{[k]}$ wird so gewählt, dass der Schritt genau bis zu diesem Minimum geht. Dann berechnet man in $\v x^{[k+1]}$ eine neue Abstiegsrichtung und bestimmt $\alpha^{[k+1]}$ nach dem gleichen Verfahren und so weiter.

[^fn:linesearch]: Das ist nicht das Gleiche wie das Minimum von $f$, da man ja nicht im gesamten Raum sucht, sondern nur entlang einer Linie. 

Mathematisch kann man die Schrittweite $\alpha^{[k]}$ als Lösung des folgenden **eindimensionalen** Optimierungsproblems auffassen:
\begin{align*}
\min_{\alpha} f(\v x^{[k]}+\alpha \v d^{[k]})
\end{align*}
Das Problem in Worte übersetzt: Suche dasjenige $\alpha$, dass die Funktion $f$ von $\v x^{[k]}$ ausgehend entlang der Richtung (Linie) $\v d^{[k]}$ minimiert. Dieses Problem muss in jedem Schritt (also $k=0,1,2,\dots$) des Abstiegsverfahrens neu gelöst werden. Dafür könnte man auch wieder ein Gradientenverfahren nehmen, man kann es aber auch mit Verfahren machen, die speziell für 1D-Optimierung entwickelt wurden, wie z.B. das [Bisektionsverfahren](https://de.wikipedia.org/wiki/Bisektion#Kontinuierlicher_Fall).

Dieses Verfahren zur Bestimmung der Schrittweite nennt man (*exakte*) *Liniensuche* (*line search*).

````{prf:example} Exakte Liniensuche
Für die Funktion $f:\R^3\rightarrow \R$
\begin{align*}
f(x_1,x_2,x_3)=\sin (x_1x_2)+\exp(x_2+x_3)-x_3
\end{align*}
soll ausgehend vom Punkt $\v x^{[k]}=\bmats 1\\2\\3\emats$ eine Liniensuche für die Abstiegsrichtung $\v d^{[k]}=\bmats 0\\-1\\-1\emats$ durchgeführt werden.

Dafür müssen wir $f$ an der Stelle $\v x^{[k]}+\alpha \v d^{[k]}$ auswerten und als eindimensionale Funktion von $\alpha$ auffassen. Es gilt
\begin{align*}
\v x^{[k]}+\alpha \v d^{[k]}&=\bmat 1\\2\\3 \emat+\alpha \bmat 0\\-1\\-1 \emat\\
                            &=\bmat 1\\ 2-\alpha \\ 3-\alpha\emat
\end{align*}
Einsetzen in $f$:
\begin{align*}
f(\v x^{[k]}+\alpha \v d^{[k]})=f(1, 2-\alpha, 3-\alpha)=\sin(1(2-\alpha))+\exp((2-\alpha)(3-\alpha))-(3-\alpha)
\end{align*}
Dies fassen wir als Zielfunktion des eindimensionalen Optimierungsproblems auf, mit dem wir $\alpha$ bestimmen:
\begin{align*}
\min_{\alpha} \sin(2-\alpha)+\exp(5-2\alpha)+\alpha-3
\end{align*}
Der Graph dieser Funktion:
```{figure} ./bilder/exact_linesearch.png
:width: 400px
```
Das Minimum liegt bei $\alpha\approx 3.127$. Damit wählen wir für die Schrittweite in Schritt $k$ $\alpha^{[k]}=3.127$ und erhalten somit als neue Iterierte des Gradientenverfahrens:
\begin{align*}
\v x^{[k+1]}=\v x^{[k]}+3.127\v d^{[k]}=\bmat 1\\ -1.126\\ -0.126 \emat
\end{align*}
````

### Näherungsweise Liniensuche
Ein Nachteil der exakten Liniensuche ist, dass für jeden Schritt $k$ des Abstiegsverfahrens ein 1D-Optimierungsproblem (normalerweise iterativ) gelöst werden muss. Dabei muss die Funktion $f$ an verschiedenen Punkten ausgewertet werden. Besonders wenn $f$ sehr "teuer" ist (z.B. eine Verlustfunktion im maschinellen Lernen für ein sehr großes Trainingsset oder ein Simulationsmodell), ist dies in der Praxis zu aufwendig. 

%Außerdem dient das 1D-Optimierungsproblem ja nur dazu eine Schrittweite zu berechnen, die nur für den aktuellen Schritt des übergeordneten Verfahrens von Bedeutung ist, d.h. 

Stattdessen macht man eine näherungsweise Liniensuche (approximate line search). Man möchte also nicht unbedingt die *beste* Schrittweite $\alpha$, sondern begnügt sich mit einer *guten* Schrittweite $\alpha$, kommt aber dafür mit möglichst wenigen zusätzlichen Auswertungen von $f$ aus.

Frage: Wann ist eine Schrittweite gut bzw. akzeptabel? Antwort: wenn der Schritt die Zielfunktion um ein vorgegebenes Mindestmaß reduziert. Also: Statt zu fordern, dass die Differenz von einem zum nächsten Schritt $f(\v x^{[k]})-f(\v x^{[k+1]})$ so groß wie möglich ist (das wäre die exakte Liniensuche), fordert man, dass die Differenz $f(\v x^{[k]})-f(\v x^{[k+1]})$ "hinreichend groß" ist. 

Die Überlegungen und Details, die hinter der Angabe "hinreichend groß" verbergen, sind theoretisch motiviert. Wir schreiben die Bedingung zunächst hin und versuchen dann, uns ihr Stück für Stück zu nähern.

````{prf:Definition} Bedingung für hinreichenden Abstieg (1. Wolfe-Bedingung)
:label: def:wolfe

Eine Schrittweite $\alpha$ erfüllt die *Bedingung für hinreichenden Abstieg* (*1. Wolfe-Bedingung*), wenn gilt:
\begin{align*}
f(\v x^{[k+1]})=f(\v x^{[k]}+\alpha \v d^{[k]})\leq f(\v x^{[k]})+\hyper{\beta}\alpha \nabla f(\v x^{[k]})\v d^{[k]},
\end{align*}
wobei $\hyper{\beta}$ ein Hyperparameter zwischen $0$ und $1$ ist. Der default ist oft $\hyper\beta = 10^{-4}$
````
Was bei dieser Bedingung eigentlich überprüft wird, lässt sich am besten mit einer Skizze beschreiben:
```{figure} ./bilder/Wolfe_Bedingung.png
Entlehnt aus: *Kochenderfer & Wheeler: Optimization Algorithms*, S. 56
```
Die Abbilung zeigt folgende Situation: Es wurde eine Abstiegsrichtung $\v d$ bestimmt und man seht nun vor der Frage, wie weit man in diese Richtung gehen soll, wie groß also $\alpha$ sein soll (den Iterationszähler $^{[k]}$ lassen wir hier aus Gründen der Lesbarkeit weg). Für unterschiedliche Werte von $\alpha$ wird die Zielfunktion $f$ nach dem Schritt, also $f(\v x + \alpha \v d)$ unterschiedlich groß. Bei der Bestimmtung "schaut" man in der Optimierungslandschaft also in Richtung $\v d$ und erhält so (egal in welcher Dimension $\v x$ lebt) einen eindimensionalen Schnitt durch diese Landschaft, also eine eindimensionale Funktion, dessen Argument die Schrittweite $\alpha$ ist. Bei $\alpha=0$ befindet man sich am alten Iterationspunkt $\v x^{[k]}$. Da $\v d$ eine Abstiegsrichtung ist (das kann, muss aber nicht der Gradient selbst sein), ist die Richtungsableitung auf jeden Fall negativ, also $\nabla f(\v x) \v d<0$. Laut Taylor-Entwicklung wird $f$ auf jeden Fall kleiner, wenn man $\alpha$ nur klein genug macht. Unter Umständen ist die Reduktion und die Schrittweite aber sehr klein; der Algorithmus bleibt gewissermaßen stecken.

Die Bedingung für hinreichenden Abstieg fordert nun, dass nicht ein *beliebig* kleiner Abstieg erzielt wird, sondern ein Abstieg, der proportional zur Größe der Ableitung ist. Sie ist angelehnt an die Reduktion, die durch die lineare Approximation vorhergesagt wird (die untere Gerade):
\begin{align*}
f(\v x) + \alpha\nabla f(\v x) \v d
\end{align*}
So viel Reduktion kann nicht immer erzielt werden, deshalb wird die Bedingung "entschärft", indem man den Term $\nabla f(\v x) \v d$ mit einer Zahl $\hyper{\beta}\in(0,1)$ multipliziert:
\begin{align*}
f(\v x) + \hyper{\beta}\alpha\nabla f(\v x) \v d
\end{align*}
 Wenn man nun fordert, dass $f(\v x+\alpha \v d)\leq f(\v x) + \hyper{\beta}\alpha\nabla f(\v x) \v d$, fordert man also nicht ganz so viel Abstieg wie durch die lineare Approximation vorhergesagt. In der Grafik wird das durch die obere Gerade dargestellt. Diese ist weniger steil als die Gerade $f(\v x) + \alpha\nabla f(\v x) \v d$ und man kann im Gegensatz zu dieser immer eine Schrittweite finden, die dazu führt, dass der Funktionswert darunter liegt. Im Beispiel bezeichnet der blau markierte Bereich alle zulässigen Schrittweiten $\alpha$, also alle $\alpha$s, die für einen hinreichenden Abstieg sorgen.

Wie wählen wir nun ein solches $\alpha$ aus? Eine Faustregel bei der Bestimmung der Schrittweite war ja, diese so groß wie möglich zu wählen, ohne dass das Verfahren divergiert. Die sog. *Backtracking Liniensuche* zur Bestimmung der Schrittweite geht wie folgt vor: wir starten mit einer großen Schrittweite $\hyper{\alpha_0}$, z.B. $\hyper{\alpha_0}=10$. Wenn die uns (laut Wolfe-Bedingung) keinen hinreichenden Abstieg verschafft, halbieren wir die Schrittweite und testen die Wolfe-Bedingung erneut. Das machen wir so lange, bis wir eine Schrittweite gefunden haben, für die die Bedingung erfüllt ist. Dass es die gibt, stellt die Theorie sicher. Tatsächlich kann man beweisen, dass die {prf:ref}`def:wolfe` zusammen mit der Backtracking Liniensuche garantiert zu einem lokalen Minimum konvergiert. Wir geben erst das allgemeine Verfahren an und zeigen in {prf:ref}`ex:backtracking` wie es bei einem konkreten Beispiel funktioniert. 

````{prf:algorithm} Backtracking Liniensuche
Gegeben: 
: Differenzierbare Funktion $f:\R^n\rightarrow\R$.
: Ein fester Punkt $\v x$.
: Abstiegsrichtung $\v d$.
: Hyperparameter: Startschrittweite $\hyper{\alpha_0}$ (default: $\hyper{\alpha_0}=10$)
: Hyperparameter: Faktor für die Reduktion $\hyper{p}<1$ (default: $\hyper{p}=0.5$)
: Hyperparameter der Wolfe-Bedingung $\hyper{\beta}$ (default: $\hyper{\beta}=10^{-4}$)

Gesucht: 
: Schrittweite $\alpha$, die die Bedingung für den hinreichenden Abstieg erfüllt. .

**Algorithmus:**
1. Setze $\alpha \leftarrow \alpha_0$
2. Solange $f(\v x+\alpha \v d)> f(\v x)+\hyper{\beta}\alpha \nabla f(\v x)\v d$:  
&nbsp;&nbsp;&nbsp;&nbsp;Setze $\alpha \leftarrow \hyper{p}\alpha$
3. Gib als Ergebnis $\alpha$ zurück.
````
Der Algorithmus wird typischerweise in *jedem* Schritt des Gradientenverfahrens aufgerufen. Eine einfache Python Implementierung sieht so aus:

```{code-cell} ipython3
def backtracking(x, d, func, dfx):
    """ 
    Compute stepsize alpha by backtracking line search.
    
    :param np.array x: Current iterate
    :param np.array d: Current descent direction
    :param function func: Objective function
    :param np.array dfx: Gradient evaluated at current iterate
    :return float: Stepsize alpha that provides sufficient reduction of the objective function
    """
    
    # Hyperparameter
    alpha = 10
    beta = 1e-4
    p = 0.5
    
    # Evaluate functions that are needed in every iteration
    fx = func(x)
    dfx_dot_d = np.dot(dfx, d)
    # Test 1. Wolfe condition
    while func(x + alpha*d) > fx + beta*alpha*dfx_dot_d:
        alpha = p*alpha
        # Stop if stepsize gets too small
        if alpha < 1e-16:
            break
    return alpha
```

Die Hyperparameter kann man grob wie folgt interpretieren:
$\hyper{\alpha_0}$ ist die größtmögliche Schrittweite in jeder Iteration $k$ des Gradientenverfahrens. Je größer $\hyper{\alpha_0}$ und $\hyper{p}$, die Reduktion der Testschrittweite, desto größer (und hoffentlich besser) wird potentiell der Schritt, aber es besteht die Gefahr, dass das Backtracking Verfahren viele Iterationen benötigt, bis eine geeignete Schrittweite gefunden wird.

````{prf:example} Backtracking Liniensuche
:label: ex:backtracking

Wir befinden uns in Schritt $k$ eines Gradientenverfahrens zur Minimierung der Funktion
\begin{align*}
f(\v x)=x_1^2+x_1x_2+x_2^2 
\end{align*}
ausgehend vom Punkt $(x_1,x_2)^T=(1,2)^T$ haben wir als Abstiegsrichtung den Vektor $\v d=(−1,−1)^T$ bestimmt und möchten nun eine geeignete Schrittweite $\alpha$ identifizieren.

Dafür führen wir die Backtracking Liniensuche mit den Hyperparametern Maximalschrittweite $\hyper{\alpha_0}=10$, Reduktionsfaktor $\hyper{p}=0.5$ und dem Parameter $\hyper{\beta}=10^{−4}$ aus.

Der Gradient an der Stelle $(1,2)^T$ ist
\begin{align*}
\nabla f(1,2)=(4, 5).
\end{align*}
Die Richtungsableitung in Richtung der Abstiegsrichtung ist
\begin{align*}
\nabla f(1,2)\v d=\nabla f(1,2)\bmat -1\\-1\emat=-9.
\end{align*}
Wir führen nun die Iterationen der Backtracking Liniensuche durch:

Iteration 1
: Teste Wolfe Bedingung
  \begin{align*}
  f(\v x+\alpha \v d) &\leq f(\v x)+10^{-4}{\color{red}{\alpha}}\nabla f(1,2)\v d\\
  \Leftrightarrow f((1,2)+{\color{red}{10}}\cdot (−1,−1))&\leq 7+10^(−4)\cdot {\color{red}{10}}\cdot (−9)\\
  \Leftrightarrow 217&\leq 6.991
  \end{align*}
  Die Ungleichung ist nicht erfüllt, also muss $\alpha$ verringert werden:
  \begin{align*}
  \alpha \leftarrow 0.5\alpha = 5
  \end{align*}

Iteration 2
: Teste Wolfe Bedingung
  \begin{align*}
  f((1,2)+{\color{red}{5}}\cdot (−1,−1))&\leq 7+10^(−4)\cdot {\color{red}{5}}\cdot (−9)\\
  \Leftrightarrow 37&\leq 6.996
  \end{align*}
  Die Ungleichung ist nicht erfüllt, also muss $\alpha$ verringert werden:
  \begin{align*}
  \alpha \leftarrow 0.5\alpha = 2.5
  \end{align*}

Iteration 3
: Teste Wolfe Bedingung
  \begin{align*}
  f((1,2)+{\color{red}{2.5}}\cdot (−1,−1))&\leq 7+10^(−4)\cdot {\color{red}{2.5}}\cdot (−9)\\
  \Leftrightarrow 3.25&\leq 6.998
  \end{align*}
  Die Bedingung ist erfüllt, die Liniensuche terminiert und gibt als Schrittweite $\alpha=2.5$ zurück.
````


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
Angenommen, unser Verfahren für die beiden Funktion $f_1$ und $f_2$ macht einen Schritt von $\bmat 1\\1\emat$ nach $\bmat 0.8\\0.8\emat$. In beiden Fällen wäre also der gleiche Fortschritt (im $(x,y)$-Raum!) in Richtung der Lösung erzielt worden.

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


## Probleme des Gradientenabstiegs
Der Gradientenabstieg ist ein Optimierungsverfahren, das in jeder Iteration den negativen Gradienten der Funktion, die minimiert werden soll, benutzt. Die Analysis garantiert, dass der negative Gradient eine Abstiegsrichtung ist. Außerdem können Gradienten oft einfach und schnell ausgewertet werden können (die Details werden in {ref}`sec:ad` beschrieben). Das macht den Gradientenabstieg in der Praxis sehr beliebt. Allerdings hat der Gradientenabstieg auch zwei fundamentale Probleme, durch die er in der Praxis oft sehr viele Iterationen benötigt.

Woher kommen die Probleme des Gradientenabstiegs? Der (negative) Gradient, unsere Suchrichtung, ist ein *Vektor*. Wie jeder Vektor hat er eine *Richtung* und eine *Länge*. Abhängig von der Funktion, die minimiert werden soll, kann eines dieser
Attribute -- oder beide -- Probleme verursachen, wenn man den negativen Gradienten
als Abstiegsrichtung wählt. 

Die *Richtung* des negatien Gradienten kann während der Iterationen des Gradientenverfahrens wild oszillieren, so dass "Zick-Zack Schritte" gemacht werden, bei denen es lange dauert, bis man ein Minimum erreicht.

Die *Länge* des negativen Gradienen kann in der Nähe von kritischen Punkten sehr klein werden, was dazu führt, dass der Gradientenabstieg in flachen Regionen, insbesondere in der Nähe von Minima und Sattelpunkten, langsam durch die Optimierungslandschaft "kriecht".

Diese beiden Probleme sind nicht bei jeder einzelnen Funktion zu beobachten, tauchen aber gerade bei Optimierungsproblemen des maschinellen Lernens oft auf. Viele Funktionen dort weisen lange, schmale Täler auf, die das oben beschriebene Verhalten begünstigen.

(sec:zickzack)=
### Zick-Zack Verhalten
In {ref}`sec:interpretation` hatten wir überlegt, dass eine Eigenschaft des (negativen) Gradienten ist, dass er senkrecht auf den Höhenlinien der Funktion steht. Das ist eine universelle Eigenschaft und gilt für jede differenzierbare Funktion. In der Praxis kann diese Eigenschaft dazu führen (hängt natürlich von der genauen Funktion ab, die man betrachtet), dass die Gradientenrichtungen während des Gradientenabstiegs ein *Zick-Zack*-Verhalten aufweisen, was wiederum dazu führt, dass wenig Fortschritt in Richtung der Lösung gemacht wird. Konsequenz: das Verfahren benötigt sehr viele Schritte bis zur Konvergenz. 

Wir betrachten das Verhalten anhand dreier Testbeispiele, den drei quadratischen Funktionen $f_i\R^2\rightarrow \R$:
\begin{align*}
f_1(x,y)&=0.5 x^2 + 9y^2\\
f_2(x,y)&=0.1 x^2 + 9y^2\\
f_3(x,y)&=0.01 x^2 + 9y^2
\end{align*}
Alle drei Funktionen haben dasselbe globale Minimum $(0,0)^T$. Die Funktionen $f_1,f_2,f_3$ sind (von oben nach unten) in den folgenden Plots dargestellt:
```{code-cell} ipython3
:tags: [hide-input]
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_iterates(iterates_list, func, c_list):
    """Plot objective function func as contour plot and visualize iterates"""
    fig = make_subplots(rows=len(iterates_list), cols=1)

    for k, (iterates, c) in enumerate(zip(iterates_list, c_list)):
        iterates_T = iterates.T
        x1_min = min(0,np.min(iterates_T[0]))-0.1
        x1_max = max(1,np.max(iterates_T[0]))+0.1
        x2_min = min(0,np.min(iterates_T[1]))-0.1
        x2_max = max(1,np.max(iterates_T[1]))+0.1

        x1_range = np.linspace(x1_min, x1_max, 100)
        x2_range = np.linspace(x2_min, x2_max, 100)
        A = np.meshgrid(x1_range, x2_range)
        Z = func(A, c)

        n_iter = len(iterates_T[1])
        fig.add_contour(z=Z, x=x1_range, y=x2_range, 
                                        colorscale="Blues",
                                        contours=dict(start=0,
                                                    end=50,
                                                    size=1),
                                        row=k+1, col=1, showscale=False, showlegend=False)

        fig.add_scatter(x=iterates_T[0], y=iterates_T[1], 
                        mode='lines+markers', name='iterates',

                        marker=dict(color=np.arange(n_iter), cmin=0, cmax=n_iter, size=7, colorbar=dict(title="k", x=1.15), 
                        colorscale="Oranges"),
                        line=dict(color="grey"),
                        row=k+1, col=1, showlegend=False
                    )

    fig.update_layout(template="simple_white", height=800, margin=go.layout.Margin(l=0, r=0, b=0, t=0) )
    fig.show()


def f(x, c):
    """ Function to minimize """
    return c*x[0]**2 + 9*x[1]**2

def df(x, c):
    """ Derivative of the function to minimize """
    return np.array([2*c*x[0], 18*x[1]])

def gd(func, derv, alpha, x0, n_steps, c):
    """ Perform n_steps iterations of gradient descent with steplength alpha and print iterates """
    x_history = [x0]
    x = x0
    for k in range(n_steps):
        dx = derv(x, c)
        x = x - alpha * dx
        x_history.append(x)

    return np.array(x_history)


x0 = np.array([10,1])
x_history1 = gd(func=f, derv=df, alpha=0.1, x0=x0, n_steps=25, c=0.5)
x_history2 = gd(func=f, derv=df, alpha=0.1, x0=x0, n_steps=25, c=0.1)
x_history3 = gd(func=f, derv=df, alpha=0.1, x0=x0, n_steps=25, c=0.01)
plot_iterates([x_history1, x_history2, x_history3], f, c_list=[0.5,0.1,0.01])
```
Je kleiner der Koeffizient von $x$ ist, desto länger und schmäler wird das Tal. Im unteren Plot der Funktion $f_3$ sind die Höhenlinien nahezu parallel in der Nähe des initialen Punktes $(10, 1)^T$. Von diesem Punkt machen wir 25 Schritte mit dem Gradientenabstieg mit Schrittweite $\alpha=0.1$. Beim Betrachten der Plots sehen wir in jedem Fall, aber zunehmend vom ersten bis zum dritten Beispiel, das Zick-Zack-Verhalten des Gradientenabstiegs. Im dritten Fall wird insgesamt sehr wenig Fortschritt in Richtung des Minimums erzielt.  

Wir können auch die Ursache dieses Zick-Zack-Kurses erkennen: Der negative Gradient
steht stets senkrecht zu den Höhenlinien der Funktion, und bei sehr schmalen Funktionen werden diese Konturen fast parallel.
Dieses Zick-Zack-Verhalten kann zwar durch eine Verringerung der Schrittlänge verbessert werden.
Das löst aber nicht das zu Grunde liegende Problem -- nämlich die langsame Konvergenz.

(sec:gdslow)=
### Langsames Kriechen durch flache Regionen
Wie wir wissen aus den notwendigen Optimalitätsbedingungen wissen, verschwindet der Gradient bei kritischen Punkten, d.h. wenn $\v x$ ein Minimum, Maximum oder ein Sattelpunkt ist gilt $\nabla f(\v x)=\v 0$. Das bedeutet aber auch, dass die Länge des Gradientenvektors bei kritischen Punkten $0$ ist, also $\norm{\nabla f(\v x)}_2=0$. In der Nähe kritischer Punkte hat der negative Gradient eine Richtung, aber es gilt $\norm{\nabla f(\v x)}_2\approx 0$ (wegen der Stetigkeit der Ableitung). Diese Eigenschaft hat folgende Konsequenz für die Schritte des Gradientenabstiegs: Sie machen sehr wenig Fortschritt, sie "kriechen" förmlich in der Nähe von stationären Punkten. Das hat folgenden Grund: die Distanz, die der Gradientenabstieg in einem Schritt zurücklegt, also $\norm{\v x^{[k+1]}-\v x^{[k]}}_2$ hängt nicht nur von der Schrittweite ab, sondern auch von der Länge des Gradientenvektors:
\begin{align*}
\v x^{[k+1]}&=\v x^{[k]}-\alpha \nabla f(\v x^{[k]})\\
\Leftrightarrow \v x^{[k+1]}-\v x^{[k]}&=-\alpha \nabla f(\v x^{[k]})\\
\Leftrightarrow \norm{\v x^{[k+1]}-\v x^{[k]}}_2&=\alpha \norm{\nabla f(\v x^{[k]})}_2
\end{align*}
Da der Gradient weit weg von der Lösung oft groß ist, z.B. bei den initialen Punkten, die zufällig initialisiert werden, sind die ersten Schritte eines Gradientenverfahrens typischerweise groß und es wird guter Fortschritt in Richtung der Lösung gemacht. Umgekehrt, wenn sich das Verfahren einem kritischen Punkt annähert, wird die Norm des Gradienten klein, und es wird nur noch wenig Fortschritt in Richtung der Lösung gemacht. Leider passiert das nicht nur in der Nähe von Minima, sondern auch in der Nähe von Sattelpunkten. In manchen Fällen kann es passieren, dass der Gradientenabstieg in der Nähe von Sattelpunkten vollständig zum Stillstand kommt.

Wir illustrieren das am Beispiel der Funktion $f(x)=x^4$ mit dem Startwert $x^{[0]}=1$. Wie man sieht, sind die Schritte zu Beginn des Verfahrens noch sehr groß und werden dann immer kleiner in der Nähe der Lösung $x=0$. Der Gradient ist sehr groß, wenn sich der Punkt weit weg von der Lösung befindet und sehr klein in der Nähe der Lösung.
```{code-cell} ipython3
:tags: [hide-input]
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def f(x):
    """ Function to minimize """
    return x**4

def df(x):
    """ Derivative of the function to minimize """
    return 4*x**3

def gd(func, derv, alpha, x0, n_steps):
    """ Perform n_steps iterations of gradient descent with steplength alpha and return iterates """
    x_history = [x0]
    x = x0
    for k in range(n_steps):
        dx = derv(x)
        x = x - alpha * dx
        x_history.append(x)

    return np.array(x_history)

n_iter = 10
x_history = gd(func=f, derv=df, alpha=0.1, x0=1.0, n_steps=n_iter)

x = np.linspace(-1.1,1.1,100)

fig = go.Figure(go.Scatter(x=x, y=f(x), name="f(x)=x²", showlegend=False,
                         mode="lines", 
                         marker_color='#1f77b4'))
fig.add_trace(go.Scatter(x=x_history, y=f(x_history),
                         mode="markers", 
                         marker=dict(color=np.arange(n_iter+1), cmin=0, cmax=n_iter+1, size=7, colorbar=dict(title="k", x=1.15), 
                         colorscale="Oranges"), showlegend=False))

fig.update_layout(width=500)
fig.show()
```

## Gradientenabstieg mit Momentum
Im Abschnitt {ref}`sec:zickzack` haben wir ein fundamentales Problem mit der *Richtung* des negativen Gradienten beobachtet: sie kann (je nach der zu minimierenden Funktion) schnell oszillieren, was zu zickzackförmigen Gradientenabstiegsschritten führt, die die
Optimierung verlangsamen. In diesem Abschnitt beschreiben wir eine beliebte Erweiterung des Standard Gradientenabstiegsschritt, das sogenannte *Momentum*, das speziell darauf ausgelegt ist, dieses Problem zu beheben. 

Die Grundidee ist, dass man in jedem Schritt nicht mehr nur dem aktuellen negativen Gradienten folgt, sondern auch die Richtung aus dem vorherigen Schritt mit berücksichtigt. Jeder Schritt $\v d^{[k]}$ ist eine Summe aus aktuellem negativen Gradienten und dem vorherigen Schritt. In Formeln:
\begin{align*}
\v d^{[k]} = \hyper{\beta}\v d^{[k-1]}-\nabla f(\v x^{[k]})
\end{align*}
Mit dem so berechneten Schritt generiert man dann gemäßt dem allgemeinen Framework {prf:ref}`alg:gd_allgemein` die nächste Iterierte $\v x^{[k+1]}$ als
\begin{align*}
\v x^{[k+1]} = \v x^{[k]}+\alpha^{[k]}\v d^{[k]}
\end{align*}
Als Start der Rekursion wählt man $\v d^{[0]}=\v 0$; der erste Schritt ist also ein normaler Gradientenschritt. Die Schrittweite $\alpha^{[k]}$ wird davon unabhängig bestimmt. Sie kann wie in den vergangenen Abschnitten beschrieben zum Beispiel konstant, gedämpft oder mittels Liniensuche bestimmt werden. 


 Der Hyperparameter $\hyper{\beta}\in [0,1]$ bestimmt, wie viel von der "alten" Richtung mit in den aktuellen Schritt mit einfließen soll. Für sehr kleine Werte von $\hyper{\beta}$ wird für den aktuellen Schritt nur wenig alte Information verwendet und viel vom aktuellen Gradienten. Im Extremfall $\hyper{\beta}=0$ erhält man den normalen Gradientenabstieg. Für große Werte von $\hyper{\beta}$ wird mehr Wert auf alte Information gelegt. In der Praxis wählt man $\hyper{\beta}$ z.B. im Intervall $[0.7,1.0]$.
 
 %Im Extremfall $\hyper{\beta}=1$ ist für *jeden* Schritt die Abstiegsrichtung $\v d^{[k]}=\v d^{[0]}=-\nabla f(\v x^{[0]})$, da der zweite Term $(-\nabla f(\v x^{[k]}))$ für $\hyper{\beta}=1$ ja immer gleich Null ist.
 
 Wie können wir uns diese "alte" Gradienteninformation vorstellen? Durch die Rekursion hinterlassen ja *alle* Gradienten vom Start des Gradientenverfahrens an ihre Spuren im aktuellen Schritt. Wie genau, das schauen wir uns in einem Beispiel an, indem wir die Rekursion über die ersten drei Schritte ausrollen.

 \begin{align*}
  \v d^{[0]}&=-\nabla f(\v x^{[0]})\\
  \v d^{[1]}&=\hyper{\beta}\v d^{[0]}-\nabla f(\v x^{[1]})\\
          &=-\hyper{\beta}\nabla f(\v x^{[0]})-\nabla f(\v x^{[1]})\\
  \v d^{[2]}&=\hyper{\beta}\v d^{[1]}-\nabla f(\v x^{[2]})\\
          &=\hyper{\beta}(-\hyper{\beta}\nabla f(\v x^{[0]})-\nabla f(\v x^{[1]}))-\nabla f(\v x^{[2]})\\
  \v d^{[3]}&=\hyper{\beta}\v d^{[2]}-\nabla f(\v x^{[3]})\\
          &=\hyper{\beta}(\hyper{\beta}(-\hyper{\beta}\nabla f(\v x^{[0]})-\nabla f(\v x^{[1]}))-\nabla f(\v x^{[2]}))-\nabla f(\v x^{[3]})
\end{align*}
Was fällt auf? Schauen wir uns einmal den letzten Schritt $\v d^{[3]}$ an und multiplizieren die Klammern aus:
\begin{align*}
  \v d^{[3]}&=-\hyper{\beta}^3\nabla f(\v x^{[0]})-\hyper{\beta}^2\nabla f(\v x^{[1]})-\hyper{\beta}\nabla f(\v x^{[2]})-\nabla f(\v x^{[3]})
\end{align*}
Neben der "neuen" Gradienteninformation $\nabla f(\v x^{[3]})$ tauchen alle "alten" Gradienten $\nabla f(\v x^{[2]}), \nabla f(\v x^{[1]})$ und $\nabla f(\v x^{[0]})$ im Schritt $\v d^{[3]}$ auf. Sie werden aber exponentiell mit $\hyper{\beta}$ gedämpft (Annahme: $\hyper{\beta}<1$), während die Iterationen fortschreiten: $\nabla f(\v x^{[0]})$ wird mit $\hyper{\beta}^3$ multipliziert, $\nabla f(\v x^{[1]})$ mit $\hyper{\beta}^2$ und $\nabla f(\v x^{[2]})$ mit $\hyper{\beta}$. In der nächsten Iteration $k=4$ würde dann $\nabla f(\v x^{[0]})$ mit $\hyper{\beta}^4$ multipliziert, $\nabla f(\v x^{[1]})$ mit $\hyper{\beta}^3$ und so weiter. Die Dämpfung ist umso stärker, je kleiner $\hyper{\beta}$ ist ($0.1^4$ ist z.B. viel kleiner als $0.9^4$).

Verhindert das nun wirklich das Zick-Zack Verhalten des Gradientenabstiegs? Ja! Wir betrachten wieder das quadratische Beispiel $f(x_1,x_2)=0.1x_1^2+9x_2^2$. Im folgenden Plot sieht man oben das normale Gradientenverfahren (also $\hyper{\beta}=0$) und darunter Gradientenverfahren mit Momentum für $\hyper{\beta}=0.2$ und $\hyper{\beta}=0.7$.
```{code-cell} ipython3
:tags: [hide-input]
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_iterates(iterates_list, func, c_list):
    """Plot objective function func as contour plot and visualize iterates"""
    fig = make_subplots(rows=len(iterates_list), cols=1)

    for k, (iterates, c) in enumerate(zip(iterates_list, c_list)):
        iterates_T = iterates.T
        x1_min = min(0,np.min(iterates_T[0]))-0.1
        x1_max = max(1,np.max(iterates_T[0]))+0.1
        x2_min = min(0,np.min(iterates_T[1]))-0.1
        x2_max = max(1,np.max(iterates_T[1]))+0.1

        x1_range = np.linspace(x1_min, x1_max, 100)
        x2_range = np.linspace(x2_min, x2_max, 100)
        A = np.meshgrid(x1_range, x2_range)
        Z = func(A, c)

        n_iter = len(iterates_T[1])
        fig.add_contour(z=Z, x=x1_range, y=x2_range, 
                                        colorscale="Blues",
                                        contours=dict(start=0,
                                                    end=50,
                                                    size=1),
                                        row=k+1, col=1, showscale=False, showlegend=False)

        fig.add_scatter(x=iterates_T[0], y=iterates_T[1], 
                        mode='lines+markers', name='iterates',

                        marker=dict(color=np.arange(n_iter), cmin=0, cmax=n_iter, size=7, colorbar=dict(title="k", x=1.15), 
                        colorscale="Oranges"),
                        line=dict(color="grey"),
                        #line=dict(color="#ff7f0e"),
                        row=k+1, col=1, showlegend=False
                    )

    fig.update_layout(template="simple_white", height=800, margin=go.layout.Margin(l=0, r=0, b=0, t=0) )
    fig.show()


def f(x, c):
    """ Function to minimize """
    return c*x[0]**2 + 9*x[1]**2

def df(x, c):
    """ Derivative of the function to minimize """
    return np.array([2*c*x[0], 18*x[1]])

def gd(func, derv, alpha, x0, beta, n_steps, c):
    """ Perform n_steps iterations of gradient descent with steplength alpha and print iterates """
    x_history = [x0]
    x = x0
    d = np.zeros_like(x)
    for k in range(n_steps):
        d = beta*d - derv(x,c)
        x = x + alpha * d

        x_history.append(x)

    return np.array(x_history)


x0 = np.array([10,1])
x_history1 = gd(func=f, derv=df, alpha=0.1, x0=x0, beta=0.0, n_steps=25, c=0.1)
x_history2 = gd(func=f, derv=df, alpha=0.1, x0=x0, beta=0.2, n_steps=25, c=0.1)
x_history3 = gd(func=f, derv=df, alpha=0.1, x0=x0, beta=0.7, n_steps=25, c=0.1)
plot_iterates([x_history1, x_history2, x_history3], f, c_list=[0.1,0.1,0.1])
```
Man sieht, die beiden Verfahren mit Momentum viel weniger Zick-Zack Verhalten aufweisen und durch das Momentum viel näher an die Lösung herangeführt werden.

Zusammenfassend: Momentum dämpft Oszillationen und macht mehr Fortschritt in Richtungen die "auf Lange Sicht" Verbesserung bringen (d.h. Richtungen, die über mehrere Iterationen konsistent sind). 

%Ein physikalisches Analogon dazu: Eine Kugel, die ein gekrümmtes Tal hinabrollt: Die Bewegungen in Richtung der steilen Seitenwände werden kleiner, je mehr Schwung die Kugel aufnimmt.


<!-- ### Nesterov Modifikation
Ein Problem mit Momentum ist, dass die Abstiegsrichtung eventuell zu *viel* Schwung in der Nähe eines Minimums besitzt. Die Iterierten "schießen" dann über das Minimum hinweg und müssen wieder Momentum in die entgegengesetzte Richtung sammeln.

Die Idee von [Nesterovs](https://de.wikipedia.org/wiki/Juri_Jewgenjewitsch_Nesterow) Variante des Momentum Gradientenabstiegs ist, dass das Verfahren im Voraus wissen soll, dass der Gradient an der nächsten Iterierten flacher wird. Das kann nämlich bedeuten, dass das Minimum näher kommt. Es wäre doch gut, wenn wir in die aktuelle Abstiegsrichtung $\v d^{[k]}$ statt dem Gradienten am aktuellen Punkt $\nabla f(\v x^{[k]})$ den Gradienten am *nächsten* Punkt einfließen lassen könnten, also $\nabla f(\v x^{[k]}+\alpha^{[k]}\v d^{[k]})$. Das ist aber natürlich nicht möglich, da wir für diesen ja wiederum $\v d^{[k]}$ kennen müssten. 

Aber einen Teil von $\v d^{[k]}$ kennen wir ja schon ohne den Gradienten auszurechnen: Nämlich den Momentumsterm $\hyper{\beta}\v d^{[k-1]}$, den wir zum aktuellen Gradienten addieren.

Die Idee des "Nesterov Accelerated Gradient" Verfahren ist es, den Gradienten nicht bei $\v x^{[k]}$, sondern bei $\v x^{[k]} +\hyper{\beta}d{[k-1]}$ auszuwerten. Dieser Punkt sollte näher an $\v x^{[k+1]}$ liegen und somit nützlichere Gradienteninformation besitzen.

Die Iterationsvorschrift lautet:
\begin{align*}
\v d^{[k]} = \hyper{\beta}\v d^{[k-1]}-\nabla f(\v x^{[k]} +\hyper{\beta}^d{[k-1]})
\v x^{[k+1]} = \v x^{[k]}+\alpha^{[k]}\v d^{[k]}
\end{align*}

Zum Vergleich noch einmal die Iteration für das „normale“ Momentum:
\begin{align*}
\v d^{[k]} = \hyper{\beta}\v d^{[k-1]}-\nabla f(\v x^{[k]})
\v x^{[k+1]} = \v x^{[k]}+\alpha^{[k]}\v d^{[k]}
\end{align*}

In der Praxis ist die Frage "Nesterov ja oder nein?" meistens genauso zu beantworten wie meistens bei Hyperparametern: Ausprobieren! Bei manchen Problemen funktioniert das Gradientenverfahren mit normalem Momentum besser, bei manchen das mit Nesterov.  -->


## Normalisierter Gradientenabstieg
Im Abschnitt {ref}`sec:gdslow` haben wir ein fundamentales Problem mit der *Länge* des negativen Gradienten (als Vektor betrachtet) beobachtet. Die Tatsache, dass sie in der Nähe eines Minimums verschwindend klein wird, führt dazu, dass das Verfahren in der Nähe von kritischen Punkten, also neben Minima auch Sattelpunkten, anhalten kann. Wir beschreiben in diesem Abschnitt eine beliebte Erweiterung des normalen Gradientenverfahrens namens *normalisierter Gradientenabstieg*, das speziell entwickelt wurde, um dieses Verhalten zu verbessern. Der Kern dieser Idee liegt in einer einfachen Frage:
Da die (verschwindende) Länge des negativen Gradienten die Ursache dafür ist, dass der Gradientenabstieg in der Nähe stationärer Punkte langsam kriecht oder an Sattelpunkten anhält, was passiert, wenn wir die Größe bei jedem Schritt einfach ignorieren, indem wir sie herausrechnen, oder *normalisieren*?

Wir haben in {ref}`sec:gdslow` gesehen, dass die Länge des Standard Gradientenschritt proportional zur Länge des Gradienten ist, algebraisch:
\begin{align*}
\alpha^{k}\norm{\nabla f(\v x^{[k]})}_2
\end{align*}
Weil diese Länge daran Schuld ist, dass das Verfahren in der Nähe von kritischen Punkten nur langsam kriecht, dividieren wir den Gradienten einfach durch seine Norm. Der Schritt ist dann:
\begin{align*}
\v d^{[k]}=-\alpha^{k}\frac{\nabla f(\v x^{[k]})}{\norm{\nabla f(\v x^{[k]})}_2}
\end{align*}
 Der entstehende Vektor hat Länge 1, aber er zeigt immer noch in dieselbe Richtung wie der Gradient. Die Länge des Schrittes wird jetzt nur noch durch die Schrittweite $\alpha^{[k]}$ bestimmt.

Illustriert am Beispiel aus {ref}`sec:gdslow` $f(x)=x^4$ sieht man, das jeder Schritt (also die Veränderung in $x$-Richtung) gleich groß ist, unabhängig von der aktuellen Steigung:
```{code-cell} ipython3
:tags: [hide-input]
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def f(x):
    """ Function to minimize """
    return x**4

def df(x):
    """ Derivative of the function to minimize """
    return 4*x**3

def gd(func, derv, alpha, x0, n_steps):
    """ Perform n_steps iterations of gradient descent with steplength alpha and return iterates """
    x_history = [x0]
    x = x0
    for k in range(n_steps):
        dx = derv(x) / np.linalg.norm(derv(x))
        x = x - alpha * dx
        x_history.append(x)

    return np.array(x_history)

n_iter = 10
x_history = gd(func=f, derv=df, alpha=0.1, x0=1.0, n_steps=n_iter)

x = np.linspace(-1.1,1.1,100)

fig = go.Figure(go.Scatter(x=x, y=f(x), name="f(x)=x²", showlegend=False,
                         mode="lines", 
                         marker_color='#1f77b4'))
fig.add_trace(go.Scatter(x=x_history, y=f(x_history),
                         mode="markers", 
                         marker=dict(color=np.arange(n_iter+1), cmin=0, cmax=n_iter+1, size=7, colorbar=dict(title="k", x=1.15), 
                         colorscale="Oranges"), showlegend=False))

fig.update_layout(width=500)
fig.show()
```
Der Nachteil ist, dass die ersten Schritte möglicherweise zu klein sind und dort dem normalen Gradientenabstieg unterlegen sind.

%## Zusammenfassung
%TODO

