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

# Stochastischer Gradientenabstieg
Alle derzeit gebräuchlichen KI-Modelle (GPT, Midjourney, DALLE-E) werden mit einer besonderen Variante von ableitungsbasierten Optimierungsverfahren, dem *stochastischen Gradientenabstieg* trainiert.

In diesem Abschnitt erklären wir anhand von {ref}`sec:umsatz` zunächst, was ein stochastisches Optimierungsproblem ist und führen den stochastischen Gradientenabstieg für dieses Problem ein. Anschließend schauen wir uns an, warum das Trainieren eines Modells im maschinellen Lernens eigentlich ein stochastisches Optimierungsproblem ist und zeigen dann, wie der stochastisches Gradientenabstieg dafür verwendet werden kann. 

## Ein stochastisches Optimierungsproblem
Wir betrachten noch einmal das Problem der Umsatzmaximierung im Einproduktfall. Ziel war es, den Verkaufspreis so festzulegen, dass der Umsatz maximal wird. Wird der Verkaufspreis zu hoch gewählt, wird pro verkauftem Produkt zwar viel Umsatz erzielt, die Nachfrage sinkt jedoch. Wird der Preis zu niedrig gewählt, werden zwar mehr Einheiten verkauft, aber zu einem geringeren Preis pro Einheit, was sich auf den Gesamtumsatz auswirkt. Wir hatten dies mit folgendem simplen Modell beschrieben:

\begin{align*}
\max_{p} p\cdot D(p)=p\cdot(M-\eta\cdot p) = pM-\eta p^2,
\end{align*}

wobei $M$ die maximale Nachfrage beschreibt und $-\eta$ die Preiselastizität, also die Änderung der Nachfrage bei einer Änderung des Preises. Im Beispiel haben wir angenommen, dass $M$ und $\eta$ feste, positive Zahlen sind. Mit dieser Annahme gibt es zwei offensichtliche Probleme:

1. Wir kennen $M$ und $\eta$ in der Realität nicht.
2. $M$ und $\eta$ werden in der Regel nicht immer gleich sein.

Nehmen wir z.B. an, dass es sich bei dem Produkt um Eiscreme handelt und die Nachfrage bezieht sich auf einen Tag. Dann wird an einem heißen Sommertag $M$ größer als an einem verregneten Tag, d.h. es gibt grundsätzlich mehr Nachfrage nach Eis. Wenn zudem die Konkurrenz-Eisdiele geschlossen hat und es weit und breit keine Alternative zu unserem Eis gibt, werden die Kunden womöglich auch weniger preissensitiv sein (kleineres $\eta$), d.h. die Nachfrage wird also bei einer Preiserhöhung weniger zurückgehen.

Wir modellieren daher $M$ und $\eta$ als *Zufallsvariablen*. Das sind, wie der Name schon sagt, Variablen, die zufällig verschiedene Werte annehmen können. Welche Werte $M$ und $\eta$ mit welcher Wahrscheinlichkeit annehmen, gibt ihre *Wahrscheinlichkeitsverteilung* an. Für Wahrscheinlichkeitsverteilungen gibt es eine ganze Reihe von Verteilungsmodellen, z.B. die [Normalverteilung]{https://de.wikipedia.org/wiki/Normalverteilung}, [Logarithmische Normalverteilung]{https://de.wikipedia.org/wiki/Logarithmische_Normalverteilung}, [Exponentialverteilung]{https://de.wikipedia.org/wiki/Exponentialverteilung} oder [Gamma-Verteilung]{https://de.wikipedia.org/wiki/Gammaverteilung}, um nur einige zu nennen. Jedes Modell hat gewisse Voraussetzungen unter denen es angewendet wird. Zum Beispiel wird die [Binomialverteilung]{https://de.wikipedia.org/wiki/Binomialverteilung} angewendet, wenn die Anzahl der Treffer in einer Serie von gleichartigen und unabhängigen Versuchen, die jeweils genau zwei mögliche Ergebnisse haben, modelliert werden soll. Die Realität ist aber häufig deutlich komplizierter und derartige Modelle sind oft nur grobe Approximationen.

Für unser Umsatzmaximierungsproblem bedeutet die Modellierung als Zufallsvariable, dass wir es jeden Tag - zufällig - mit einer anderen Zielfunktion zu tun haben, bei der natürlich auch die optimalen Preise unterschiedlich sind:

```{figure} ./bilder/umsatzmaximierung_samples.png
:name: fig:umsatz
:width: 600px

Umsatzkurven für verschiedene zufällige $M$ und $\eta$.
```

Dass etwas zufällig ist, bedeutet ja gerade, dass man es *nicht* genau vorhersehen kann. Unser ursprüngliches Optimierungsproblem

```{math}
:label: eq:stochopt

\begin{align}
\max_{p} p\red{M}-\red{\eta}p^2,
\end{align}
```

ist deshalb gar nicht mehr sinnvoll definiert (wie soll man eine unbekannte Größe minimieren, die jeden Tag anders ist?). Deshalb formulieren wir das Problem nun leicht anders: Anstatt nach dem optimalen Preis suchen wir nach dem Preis, der *im Mittel*, also über viele Tage hinweg, optimal ist. Mathematisch ist das der *Erwartungswert* einer Zufallsvariable, geschrieben als $\E[\cdot]$. Wir ersetzen also unser ursprüngliches Problem {eq}`eq:stochopt` durch

\begin{align*}
\max_{p} \E[pM-\eta p^2].
\end{align*}

Diese Formulierung ist sinnvoll, da der Operator $\E[\cdot]$ die von Zufallsvariablen abhängige Funktion in eine deterministische "verwandelt", für die wir  das heißt unsere Begriffe wie Optimalität sind sinnvoll definiert.

Wir geben eine allgemeine Definition, wie üblich als Minimierungsproblem.

```{prf:definition} Stochastisches Optimierungsproblem
:label: def:stochopt

Ein Problem der Form 

\begin{align*}
\min_{\v x \in \R^n} \E[f(\v x, \v Y)].
\end{align*}

mit einer Zufallsvariable $\v Y\in\R^m$ nennt man ein *stochastisches Optimierungsproblem*. 
```

Stochastische Optimierungsprobleme zeichnen sich dadurch aus, dass durch die Anwesenheit von $\v Y\in\R^m$ die Funktion $f$ nicht deterministisch ist, das heißt wenn $f$ mehrmals an demselben Punkt $\v x$ ausgewertet wird, können verschiedene, zufällige Funktionswerte $f(\v x, \v Y)$ angenommen werden, da die Zufallsvariable $\v Y$ verschiedene Werte annimmt. Man kann sich die Variablen $\v x$ wie bisher als Entscheidungsvariablen vorstellen, während die Zufallsvariable $\v Y$ eine exogene Information darstellt, also etwas, das wir nicht beeinflussen können.

Zurück zum Umsatzmaximierungsproblem. Für die Funktion $pM-\eta p^2$ spielt $p$ die Rolle einer Entscheidungsvariable ($\v x$ in der allgemeinen Definition), während das Paar $(M,\eta)$ der Zufallsvariable $\v Y$ aus der Definition entspricht. Wenn man den Erwartungswert von $M$ und $\eta$ kennt und davon ausgeht, dass beide voneinander stochastisch unabhängig sind, dann kann man den optimalen Preis $p^*$ analog zu {ref}`sec:umsatz` analytisch berechnen. Er lautet in diesem Fall
\begin{align*}
p^*=\frac{\E[M]}{2\E[\eta]}
\end{align*}

%In der Regel kennt man aber die Verteilung von $M$ und $k$ nicht und kann deshalb deren Erwartungswert nicht ausrechnen. Wenn man aber die Möglichkeit hat, Stichproben für $M$ und


## Stochastischer Gradientenabstieg
Wir schauen uns nun die Situation an, dass man die Lösung nicht analytisch ausrechnen kann. Ähnlich wie bei deterministischen Optimierungsproblemen ist das eigentlich der Normalfall. Neben der Schwierigkeit, die Optimalitätsbedingungen nach der Variablen aufzulösen, kommt hier noch das Problem dazu, dass man den Erwartungswert meist gar nicht berechnen kann, weil man die Wahrscheinlichkeitsverteilung nicht genau kennt.

Wir gehen im Folgenden davon aus, dass wir zwar die Wahrscheinlichkeitsverteilung der Zielfunktion nicht kennen, dass wir aber die Möglichkeit haben, einzelne Stichproben (Beobachtungen) der Zufallsvariablen zu generieren. Für das Umsatzmaximierungsproblem bezeichnen wir diese mit $(M^{[k]}, \eta^{[k]})$ für $k=0,1,2,\dots$

Die Idee des stochastischen Gradientenverfahrens ist es nun, nachdem eine Stichprobe -- also ein Vektor mit Zahlen! -- generiert wurde, diese in die Funktion einzusetzen. Für die entstehende Funktion berechnet man dann den Gradienten (nach $p$). Diesen nennt man auch einen *stochastischen Gradienten*, weil er auf einer Realisation der Zufallsvariablen beruht. Damit wird die neue Iterierte erzeugt. Nun wird wieder eine Stichprobe generiert, in die Funktion eingesetzt und der nächste Gradientenschritt gemacht, usw.

Formal lässt sich der Algorithmus wie folgt beschreiben:

````{prf:algorithm} Stochastischer Gradientenabstieg
:label: alg:sgd
Gegeben: 
: Stochastisches Optimierungsproblem $\min_{\v x \in \R^n} \E[f(\v x, \v Y)]$, mit Entscheidungsvariablen $\v x$ und Zufallsvariablen $\v Y$.
: Folge von Stichproben $\v Y^{[k]}$, für $k=0,1,2,\dots$.
: Folge von Schrittweiten $\alpha^{[k]}$, für $k=0,1,2,\dots$

Gesucht: 
: Lokales Minimum von $\E[f(\v x, \v Y)]$.

**Algorithmus**:
- Starte mit initialer Schätzung $\v x^{[0]}$, setze $k=0$.
- Für $k=0,1,2,\dots$:
    1. Falls Abbruchbedingung erfüllt, beende Algorithmus mit Lösung $\v x^{[k]}$.
    2. Berechne stochastischen Gradienten 
        \begin{align*}\nabla_x f(\v x^{[k]}, \v Y^{[k]})\end{align*}
    3. Berechne neue Iterierte 
        \begin{align*}\v x^{[k+1]}=x^{[k]}-\alpha^{[k]}\nabla f(\v x^{[k]}, \v Y^{[k]}), \alpha^{[k]}>0.\end{align*}
````

Für die Schrittweitenfolge $\alpha^{[k]}$ müssen folgende Bedingungen gelten:
\begin{align*}
\sum_{k=0}^{\infty} \alpha^{[k]} = \infty && \textup{und} && \sum_{k=0}^{\infty} \left(\alpha^{[k]}\right)^2 < \infty
\end{align*}
Das bedeutet, dass die Schrittweiten gegen Null gehen müssen (2. Bedingung), aber nicht zu schnell (1. Bedingung). Wenn das nicht eingehalten wird, so werden die Iterierten "um die Lösung herumspringen", da ja in jedem Schritt der Gradient auf einer etwas anderen Funktion berechnet wird.

Eine Folge, die die Vorgaben erfüllt, ist 
\begin{align*}
\alpha^{[k]} = \frac{\alpha_0}{k+1}
\end{align*}


### Beispielimplementierung
Wir implementieren den stochastischen Gradientenabstieg für das Umsatzmaximierungsbeispiel. Dazu nehmen wir den Maximalumsatz $M$ als normalverteilt mit Erwartungswert $10$ und Standardabweichung $2$ an und die Preiselastizität $\eta$ als normalverteil mit Erwartungswert $2$ und Standardabweichung $0.2$. Die Optimallösung liegt somit bei

\begin{align*}
 p^*=\frac{\E[M]}{2\E[\eta]}=\frac{10}{2\cdot 2}=2.5
\end{align*}

Wir gehen nun davon aus, dass wir das Verteilungsmodell (und die Optimallösung nicht kennen). Wir sehen in jeder Iteration nur eine Realisation der Zufallsvariablen.

```{code-cell} ipython3
import autograd.numpy as np
from autograd import grad
import plotly.express as px

# Pseudo random number generator
prng = np.random.default_rng()

def umsatz_sample(p):
    # maximum demand: normally distributed around M
    M = 10
    M_sample = prng.normal(M, 2)
    # (negative) price elasticity: normally distributed around eta
    eta = 2
    eta_sample = prng.normal(eta, 0.2)
    
    return p*(M_sample - eta_sample*p)

# Gradientenfunktion
grad_u = grad(umsatz_sample)

# Startwert für p
p = 1.8

# Startschrittweite
alpha0 = 0.5

all_p = []
for k in range(150):
    # Harmonische Schrittweitenfolge
    alpha = 1/(k+1) * alpha0

    # Gradientenschritt
    p = p + alpha * grad_u(p)

    all_p.append(p)


print(f"Lösung nach {k+1} Iterationen: {p}")

# Verlauf der Zielfunktion über die Iterationen
px.line(all_p, markers=True, labels={"index":"p", "value":"f(p) (sample)"})
```

Wie man sieht, ist das Konvergenzverhalten nicht monoton wie beim normalen Gradientenverfahren. Die Funktion kann in einem Schritt sowohl steigen als auch fallen. Langfristig wird aber ein Abstieg und Konvergenz in der Nähe der korrekten Lösung $p=2.5$ erzielt.


## Trainingsdaten und Minibatch-Gradientenabstieg

Im Beispiel oben haben wir ein stochastischen Modell angenommen, aus dem man mittels Zufallszahlen beliebig Stichproben generieren kann. Im Beispiel war das die Normalverteilung, aus der wir mit dem Befehl `prng.normal` zufällige Samples generiert haben. In vielen Anwendungen ist es aber so, dass man gar nicht weiß, ob eine Zufallsgröße normalverteilt, exponentialverteilt oder sonstwie verteilt ist. Stattdessen hat man oft eine (endliche) Menge von Daten in Form von Beobachtungen $\v Y_i, i=1,\dots,N$ gesammelt. Man nennt diese auch *Trainingsdaten* und wir interpretieren sie als Stichprobe der Zufallsvariable $\v Y$. In {prf:ref}`alg:sgd` würde man dann, sobald der Datensatz einmal durchlaufen wurde, wieder vorne beginnen, d.h. in Iteration $N+1$ würde man wieder das erste Sample benutzen, in Iteration $N+2$ das zweite, usw. Man hat dann allerdings keine Garantie mehr, dass das Verfahren gegen ein Minimum von $\E[f(\v x, \v Y)]$ konvergiert. Dies hängt vom Umfang und der Güte der Trainingsdaten ab.

Der Übergang von stochastischem Modell zu einem Trainingsdatensatz bietet auch eine alternative Formulierung von {prf:ref}`alg:sgd`. Dazu erinnern wir uns, dass der Erwartungswert einer Zufallsvariable durch den arithmetischen Mittelwert einer Stichprobe approximiert werden kann:

```{math}
:label: eq:expectation

\begin{align}
\E[f(\v x, \v Y)] \approx \frac{1}{N}\sum_{i=1}^N f(\v x, \v Y_i)
\end{align}
```

Dasselbe gilt für den Gradienten des Erwartungswerts 

\begin{align*}
\nabla_x \E[f(\v x, \v Y)] \approx \nabla_x \left( \frac{1}{N}\sum_{i=1}^N f(\v x, \v Y_i) \right)= \frac{1}{N}\sum_{i=1}^N \nabla_x f(\v x, \v Y_i)
\end{align*}

Der stochastische Gradientenabstieg kann nun aufgefasst werden als (normaler) Gradientenabstieg für die Funktion 
$F(\v x)=\frac{1}{N}\sum_{i=1}^N f(\v x, \v Y_i)$, nur dass statt des Gradienten $\nabla_x F(\v x)=\nabla_x \left(\frac{1}{N}\sum_{i=1}^N f(\v x, \v Y_i)\right)$ in jeder Iteration nur der Gradient eines Summanden, also $\nabla_x f(\v x, \v Y_i)$, berechnet wird, um den Schritt zu bestimmen.

Eine beliebte Variante des stochastischen Gradientenabstieg ist der *Minibatch-Gradientenabstieg*. Hier wird der Schritt basierend auf einer *Teilmenge* der Summanden berechnet. Der Minibatch-Gradientenabstieg bewegt sich also zwischen dem normalen Gradientenabstieg (Gradient aller Summanden) und dem stochastischen Gradientenabstieg (Gradient eines Summanden). Wir geben nun stochastischen, Minibatch- und normalen (oder auch "Batch-") Gradientenabstieg in einem Algorithmus an.

Während in {prf:ref}`alg:sgd` die Indizes für die Stichprobe und die Iterationen identisch waren, ist dies beim Minibatch-Gradientenabstieg nicht mehr der Fall. Wir führen einen zweiten Index $i$ ein, der über die Beobachtungen aus den Trainingsdaten läuft. Der Iterationsindex $k$ wird nun erst dann erhöht, wenn einmal über den gesamten Trainingsdatensatz (also alle Minibatches) iteriert wurde. $k$ bezeichnet man als *Epoche*.

````{prf:algorithm} Minibatch-Gradientenabstieg
:label: alg:minibatch
Gegeben: 
: Stochastisches Optimierungsproblem $\min_{\v x \in \R^n} \E[f(\v x, \v Y)]$, mit Entscheidungsvariablen $\v x$ und Zufallsvariablen $\v Y$.
: Trainingsdaten $\v Y_i$, für $i=1,\dots, N$.
: Minibatch Größe $1\leq m \leq N$
: Folge von Schrittweiten $\alpha^{[k]}$, für $k=0,1,2,\dots$

Gesucht: 
: Lokales Minimum von $\E[f(\v x, \v Y)]$.

**Algorithmus**:
- Starte mit initialer Schätzung $\v x^{[0]}$, setze $k=0$.
- Für $k=0,1,2,\dots$:
    1. Falls Abbruchbedingung erfüllt, beende Algorithmus mit Lösung $\v x^{[k]}$.
    2. Setze $\v x^{[k+1,0]} =\v x^{[k]}$ 
    3. Für $i=1,\dots, N/m$:
        - Berechne stochastischen Gradienten 
            \begin{align*}\v g = \frac{1}{m}\sum_{(i-1)m}^{i\cdot m}\nabla_x f(\v x^{[k]}, \v Y_i)\end{align*}
        - Berechne neue Iterierte 
            \begin{align*}\v x^{[k+1,i]}=\v x^{[k+1,i-1]}-\alpha^{[k]}\v g, \alpha^{[k]}>0.\end{align*}
    4. Setze $\v x^{[k+1]}=\v x^{[k+1,N]}$
````

Anmerkungen:
- Der Einfachheit halber nehmen wir an, dass $N/m$ ganzzahlig ist. Ist dies nicht der Fall, ist die letzte Minibatch kleiner als die vorherigen. Dies stellt aber keine Einschränkung dar.
- Die Minibatch-Größe $m$ ist ein Hyperparameter. Für $m=1$ erhält man den stochastischen Gradientenabstieg, für $m=N$ erhält man den Batch-Gradientenabstieg.
- Der Batch-Gradientenabstieg konvergiert gegen ein Minimum von $\frac{1}{N}\sum_{i=1}^N f(\v x, \v Y_i)$. Achtung: Dies ist nicht unbedingt gleichbedeutend mit dem Minimum von $\E[f(\v x, \v Y)]$.
- Je kleiner $m$ gewählt wird, desto mehr Iterationen besitzt die innere Schleife (Index $i$). Dafür ist die Berechnung einer einzelnen Iteration in der inneren Schleife bei kleinem $m$ schneller, da der Gradient von weniger Summanden ausgewertet werden muss. 
- Das Verfahren kann auch mit anderen Suchrichtungen kombiniert werden. Bei einem stochastischen Newton-Verfahren werden z.B. auch die Hessematrizen pro Minibatch gebildet. 


## Stochastischer Gradientenabstieg und Maschinelles Lernen 
Die Begriffe Trainingsdaten, Minibatch und stochastischer Gradientenabstieg kennen sie vermutlich aus Vorlesungen über maschinelles Lernen.

Das Ziel im maschinellen Lernen ist folgendes: Man möchte eine Funktion $\v f(\v x, \v w)=\v{\hat{y}}$ identifizieren (lernen), die für gegebene Features $\v x$ eine Vorhersage $\v{\hat{y}}$ macht. Ein einfaches Beispiel ist etwa {ref}`sec:linreg`, kompliziertere Beispiele sind die Erkennung von Objekten in einem Bild oder die Antwort auf eine gegebene Frage. Die Funktion $\v f(\v x, \v w)$ hängt dabei nicht nur von den Features $\v x$ ab sondern auch von Parametern $\v w$, die während des Modelltrainings identifiziert -- man sagt auch: gelernt -- werden müssen. Die Parameter ergeben sich dabei aus der gewählten Funktionsklasse. Funktionsklassen, die für $\v f$ in Frage kommen, reichen von linearen Funktion bis hin zu neuronalen Netzen.  


Das Lernen geschieht mit Hilfe einer Verlustfunktion $\ell(\v y, \v f(\v x, \v w))$, die für ein Beispiel $(\v y, \v f(\v x, \v w) )$ den "Verlust" quantifiziert, der entsteht, wenn man für das Label (den echten Wert) $\v y$ die Vorhersage $\v f(\v x, \v w)$ macht. Eine beliebte Verlustfunktion im maschinellen Lernen ist z.B. der quadratische Verlust:

\begin{align*}
\ell(y, f(\v x, \v w)) = (y-f(\v x, \v w))^2
\end{align*}

Die Paare $(\v x, \v y)$ werden nun als Stichprobe einer Wahrscheinlichkeitsverteilung aufgefasst und man möchte, dass das Modell den erwarteten Verlust minimiert. Das Optimierungsproblem lautet also:

```{math}
:label: eq:minrisk

\begin{align*}
\min_{\v w} \E [\ell (\v y,\v f(\v x, \v w))]
\end{align*}
```

Das bedeutet, dass das Modell möglichst gute Vorhersagen auf beliebigen Datenpunkten machen soll.

Wenn wir dieses Problem mit der Definition {prf:ref}`def:stochopt` vergleichen, so spielt $\v w$ die Rolle der Entscheidungsvariablen ($\v x$ in der Definition) und die Paare $(\v x, \v y)$ die Rolle der Zufallsvariablen bzw. exogenen Information, also das, was wir nicht beeinflussen können.

Die Wahrscheinlichkeitsverteilung der Feature-Label Paar $(\v x, \v y)$ ist im allgemeinen natürlich extrem kompliziert. Das bedeutet, dass wir den Erwartungswert $\E [\ell (\v y,\v f(\v x, \v w))]$ über diese Verteilung nicht einfach berechnen können. Stattdessen starten wir mit einem Trainingsdatensatz von Feature-Label Paaren $(\v x_i,\v y_i)$, für den wir den durchschnittlichen Verlust minimieren, analog zur Approximation {eq}`eq:expectation`:

```{math}
:label: eq:erm

\begin{align}
\min_{\v w} \frac{1}{N}\sum_{i=1}^N \ell (\v y_i,\v f(\v x_i, \v w))
\end{align}
```

Für den quadratischen Verlust wäre das z.B. der mittlere quadratische Fehler:

\begin{align*}
\min_{\v w} \frac{1}{N}\sum_{i=1}^N (y_i - f(\v x_i, \v w))^2
\end{align*}

Dies ist die Formulierung, die sie vermutlich aus Vorlesungen über maschinelles Lernen kennen: das Minimieren einer Verlustfunktion auf den Trainingsdaten. Wir halten fest: Das Optimierungsproblem {eq}`eq:erm` ist nur ein Ersatzproblem für das Problem, was man eigentlich lösen möchte, nämlich {eq}`eq:minrisk`, die Minimierung des Verlustes auf allen möglichen Daten (auch unbekannten). Das Optimum von Problem {eq}`eq:erm` ist also gar nicht von Interesse, im Gegenteil: da die Lösung von {eq}`eq:erm` nur die Trainingsdaten berücksichtigt, liefert sie auf unbekannten Daten in der Regel schlechtere Werte. Dies bezeichnet man als *Overfitting*. Weiterhin muss sichergestellt werden, dass die Trainingsdaten eine repräsentative und unabhängige Stichprobe aller Daten darstellen, da sonst die Approximation $\E [\ell (\v y,\v f(\v x, \v w))]\approx \frac{1}{N}\sum_{i=1}^N \ell (\v y_i,f(\v x_i, \v w))$ nicht gültig ist.

Diese Betrachtungen liefern die theoretische Begründung, warum der stochastische bzw. Minibatch-Gradientenabstieg dem normalen Gradientenabstieg vorzuziehen ist. 

Auch aus technischer Sicht ist der stochastische Gradientenabstieg günstig. In modernen Anwendungen gilt normalerweise
- $N$ ist sehr groß (viele Trainingsdaten)
- Dimension von $\v w$ ist sehr groß (viele Modellparameter)
- Dimension von $\v x$ ist sehr groß (viele Features)

Das macht die Auswertung der Verlustfunktion aufwändig, was Rechen- und Speicherbedarf betrifft. Beim Minibatch-Gradientenabstieg benötigt man in der inneren Schleife (über die Minibatches) aber immer nur einen Teil der Trainingsdaten, d.h. der Rechen- und Speicherbedarf einer Iteration (nicht aber einer Epoche) ist unabhängig von der Anzahl $N$ der Trainingsdaten. Man muss diese also nie komplett in den Speicher laden, für den stochastischen Gradientenabstieg genügt es, immer nur ein einziges Trainingsbeispiel im Speicher zu haben. Die Größe der Minibatch $m$ kann somit auf den vorhandenen Speicher und die Problemdimension abgestimmt werden. 