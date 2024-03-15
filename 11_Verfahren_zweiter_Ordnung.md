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

(sec:newton)=
# Verfahren zweiter Ordnung
Bei Experimenten mit pathologischen Funktionen wie der Rosenbrock Funktion (siehe Übungen) stellt man fest, dass Gradientenverfahren sehr viele Schritte benötigen. Ein Problem ist, dass die Richtung des steilsten Abstiegs fast orthogonal auf der Richtung steht, die direkt zum Minimum führt, im folgenden Bild etwas unmathematisch "Tal des besten Abstiegs" genannt. 

```{figure} ./bilder/newton_motivation.png
:name: fig:rosenbrock

Typisches Verhalten eines Gradientenabstiegs für die Rosenbrock Funktion.
```

Im vergangen Kapitel haben wir gesehen, wie man dieses Zick-Zack Verhalten sowie das langsame "Kriechen" des Gradientenabstiegs durch einen Momentumsterm und Normalisierung verbessern kann. Dies funktioniert leider nicht in allen Fällen und es hat außerdem den Nachteil, dass man mit diesen Optionen immer mehr zusätzliche Hyperparameter einführt (Schrittweite, Schrittweitenstrategie, Parameter der Schrittweitenstrategie, Gewicht $\beta$ des Momentumsterms, Normalisierung), die sorgfältig aufeinander abgestimmt werden müssen. Dies muss man potentiell für jede neue Funktion tun.

Wir schauen uns das Verhalten am Beispiel der Rosenbrock Funktion genauer an. Der Graph der [Rosenbrock Funktion](https://en.wikipedia.org/wiki/Rosenbrock_function) (auch *Banana Valley Function*) ist ein gekrümmtes, steiles Tal, das an den Rändern sehr steil ist und bei dem Tal die Talsohle in einem bananenförmigen Verlauf nur leicht in Richtung des globalen Minimums $(1,1)$ abfällt. Die Funktion ist definiert als:

$$ 
f(\v x) = (x_1-1)^2 + 100(x_1^2 - x_2)^2
$$

Ihre Hessematrix $H(\v x)=\nabla^2 f(\v x)$ ist

$$
H(\v x)=\bmat 2+1200x_1^2-400x_2 & -400x_1\\
      -400x_1 & 200 \emat
$$

Wir werten die Hessematrix an einem Punkt in der Nähe der Lösung aus, z.B. $(0.97,0.94)$ (siehe schwarzer Punkt in {numref}`fig:rosenbrock`):

$$
H(0.97,0.94)=\bmat 2+1200 \cdot 0.97^2-400\cdot 0.94 & -400\cdot 0.97\\
      -400\cdot 0.97 & 200 \emat = \bmat 755.08 & -388 \\ -388 & 200\emat
$$

Was sagen uns diese Werte? Noch gar nichts -- wir erinnern uns, dass die Eigen*werte* der Hessematrix die Krümmung von $f$ in Richtung der Eigen*vektoren* beschreiben. Berechnen wir also Eigenwerte und Eigenvektoren:
```{code-cell} ipython3
import numpy as np

def grad(x):
    """ Gradient der Rosenbrock Funktion """
    return np.array([2*(x[0]-1)+400*x[0]*(x[0]**2-x[1]), -200*(x[0]**2-x[1])])

def hess(x):
    """ Hessematrix der Rosenbrock Funktion """
    ddf1 = np.array([2+1200*x[0]**2-400*x[1], -400*x[0]])
    ddf2 = np.array([-400*x[0], 200])
    return np.array([ddf1, ddf2])

x0 = [0.97,0.94]
lam, e = np.linalg.eig(hess(x0))
print(f"Eigenwert 1:{lam[0]}\nEigenwert 2:{lam[1]}")
print(f"Eigenvektor 1:{e[:,0]}\nEigenvektor 2:{e[:,1]}")
print(f"Richtung des steilsten Anstiegs:{grad(x0)/np.linalg.norm(grad(x0))}")
```
Wir stellen fest: Die Krümmung in Richtung $e_1=\bmats 0.89\\-0.46\emats$ ist etwa 1900 Mal so groß wie in Richtung $e_2=\bmats 0.46\\0.89\emats$. 

Schauen wir uns zum Vergleich die Richtung des steilsten Abstiegs am Punkt $(0.97,0.94)$ an: Der (normalisierte) Gradient von $f$ ausgewertet am Punkt $(0.97,0.94)$ ist:

$$ 
\frac{\nabla f(0.97,0.94)}{\norm{\nabla f(0.97,0.94)}_2}= \bmat 0.85,&-0.52 \emat
$$

% TODO Bild von e1, e2, steilster Abstieg

Wir sehen: die Richtung des steilsten Abstiegs (bzw. Anstiegs, aber das ist ja die gleiche Richtungsvektor nur mit dem Skalar $-1$ multipliziert) ist der stark gekrümmten Richtung $e_1$ sehr ähnlich. Das Verfahren macht Schritte in Richtungen sehr starker Krümmung (tatsächlich ist die Krümmung von $f$ in Richtung des steilsten Anstiegs -- oder Abstiegs, das Ergebnis ist dasselbe -- gegeben durch $\nabla f(\v x)H(\v x) \nabla f(\v x)^T$, hier also $\bmats 0.85,&-0.52 \emats \bmats 755.08 & -388 \\ -388 & 200\emats \bmats 0.85\\-0.52 \emats=179.6$).

Welche Konsequenz hat das? Dazu muss man sich vor Augen halten, dass *Krümmung* die *Änderung der Steigung* beschreibt. Eine starke Krümmung bedeutet eine große (lokale) Änderungsrate der Steigung. Anschaulich: Geht man ein sehr kleines Stück in eine Richtung, in der die Funktion stark gekrümmt ist, ist dort die Steigung plötzlich ganz anders. Im Falle des Gradientenabstiegs für die Rosenbrock Funktion: Geht man ein Stück in Richtung des steilsten Abstiegs, hat die Funktion dort keinen steilen Abstieg mehr, sondern nur einen flachen Abstieg oder sogar einen Anstieg. Das sagt uns ihre starke Krümmung.

Umgekehrt verspricht die Richtung der schwachen Krümmung, $e_2$ (entspricht ungefähr dem "Tal des besten Abstiegs" im Bild) zwar lokal nur wenig Abstieg. Da sich die Steigung aber wenig ändert, könnte man durchaus einen größeren Schritt in diese Richtung gehen.

Diese Überlegungen konnten wir mit Hilfe der Hessematrix anstellen. Die Idee von Verfahren zweiter Ordnung ist es, lokale Krümmungsinformation zu benutzen um bessere Richtungen und Schrittweiten zu erhalten. Wir schauen uns im folgenden zwei Varianten dieser Verfahren ein: Das Newton Verfahren und Quasi-Newton Verfahren.


## Newton Verfahren
Der Gradientenabstieg basiert auf einer Taylor-Entwicklung erster Ordnung -- einer Linearisierung. Mit Hilfe des Gradienten berechnet man eine lineare Approximation der Funktion und geht auf dieser linearen Funktion ein Stück bergab. Am neuen Punkt linearisiert man wieder usw. Wie weit man jeweils vom Linearisierungspunkt weggeht wird durch die Schrittweite gesteuert. Diese braucht man zwingend, denn da eine lineare Funktion kein Minimum hat, würde es dort ja beliebig lange bergab gehen.

Eine Idee, sich dem Newton Verfahren für Optimierung zu nähern ist folgende: Im Gegensatz zum Gradientenabstieg approximiert man die Funktion lokal nicht durch eine lineare, sondern eine quadratische Funktion. Diese minimiert man und wählt als nächste Iterierte das berechnete Minimum. Dort bildet man wieder eine quadratische Approximation usw.

Die quadratische Approximation erhält man -- Sie ahnen es -- mit Hilfe des Taylor-Polynoms zweiten Grades berechnet an der Entwicklungsstelle $\v x^{[k]}$:

$$
T(\v x^{[k]} + \v d)=f(\v x^{[k]})+\nabla f(\v x^{[k]})d+\frac{1}{2}\v d^T\v H(\v x^{[k]})\v d
$$

Dies ist eine quadratische Funktion in der Variablen $\v d$. Wie wir am Ende von {ref}`sec:konvex` gesehen haben, hat eine quadratische Funktion ein eindeutiges Minimum, wenn die Hessematrix $H(\v x^{[k]})$ positiv definit ist (dann ist die Funktion strikt konvex). Weiterhin haben wir in {prf:ref}`ex:quadratic` gesehen, dass man den kritischen Punkt einer quadratischen Funktion durch Lösung eines linearen Gleichungssystems bestimmen kann.

Diese Lösung wäre dann der Schritt $\v d^{[k]}$, mit dem wir zur nächsten Iterierten $\v x^{[k+1]}$ kommen.

Wir berechnen den kritischen Punkt des Taylor Polynoms. Es muss gelten $\nabla T=0$, also 
\begin{align*}
\nabla T(\v x^{[k]} + \v d) &= \nabla f(\v x^{[k]})+\v H(\v x^{[k]})\v d=0\\
&=\v H(\v x^{[k]})\v d = -\nabla f(\v x^{[k]})
\end{align*}

Falls $\v H(\v x^{[k]})$ invertierbar ist, ergibt sich die optimale Suchrichtung durch:

$$
\v d=-\v H(\v x^{[k]})^{-1}\nabla f(\v x^{[k]})
$$

Aber Achtung: dies ist nur für positiv definite $\v H(\v x^{[k]})$ eine Abstiegsrichtung, denn sonst hätte die quadratische Approximation ja ein Maximum statt ein Minimum.

Insgesamt haben wir also folgenden Algorithmus, der sich gut in {prf:ref}`alg:gd_allgemein` aus dem letzten Abschnitt einfügt:
````{prf:algorithm} Newton Verfahren zur Optimierung von Funktionen
:label: alg:newton
Gegeben: 
: Zwei Mal differenzierbare Funktion $f:\R^n\rightarrow\R$.

Gesucht: 
: Lokales Minimum von $f$.

**Algorithmus**:

Starte mit initialer Schätzung $\v x^{[0]}$, setze $k=0$.

Für $k=0,1,2,\dots$:
1. Überprüfe, ob $\v x^{[k]}$ die **Abbruchbedingung** erfüllt. 
    - Falls ja: Abbruch mit Lösung $\v x^{[k]}$
    - Falls nein: gehe zu Schritt 2.
2. Bestimme **Abstiegsrichtung** $\v d^{[k]}$ durch
    \begin{align*}
    \v d^{[k]}=-\v H(\v x^{[k]})^{-1}\nabla f(\v x^{[k]})^T
    \end{align*}
3. *Optional:* Bestimme Schrittweite $\alpha^{[k]}$.
4. Berechne neue Iterierte $\v x^{[k+1]}=\v x^{[k]}+\alpha^{[k]}\v d^{[k]}$.
````
Einige Anmerkungen zu dem Verfahren:
1. Die Inverse der Hessematrix modifiziert nicht nur die Richtung, sondern auch die Schrittlänge geeignet. Oft wird deshalb $\alpha^{[k]}=1$ gesetzt, d.h. es wird "unsichtbar". 
2. Voraussetzung, dass das Verfahren zu einem Minimum konvergiert ist, dass die Hessematrix positiv definit sein muss. Sonst ist nämlich $\v d^{[k]}$ keine Abstiegsrichtung. Positive Definitheit der Hessematrix ist in der Nähe der Lösung zwar gegeben, aber weit weg von der Lösung (z.B. bei einem x-beliebigen Startwert) ist das nicht immer der Fall.

Wir schauen uns das Verfahren am Beispiel der Rosenbrock Funktion an.

```{code-cell} ipython3
import numpy as np

def f(x):
    """ Function to minimize """
    return (x[0]-1)**2 + 100*(x[0]**2 - x[1])**2
    
def df(x):
    """ Derivative of the function to minimize """
    return np.array([2*(x[0]-1)+400*x[0]*(x[0]**2-x[1]), -200*(x[0]**2-x[1])])

def ddf(x):
    """ 2nd Derivative of the function to minimize """
    ddf1 = np.array([2+1200*x[0]**2-400*x[1], -400*x[0]])
    ddf2 = np.array([-400*x[0], 200])
    return np.array([ddf1, ddf2])

def newton(func, derv, hessian, x0, alpha0=1, n_steps=100):
    """ Perform n_steps iterations of newton's method and return iterates """
    x_history = [x0]
    x = x0
    for k in range(n_steps):
        # Evaluate gradient
        g = derv(x)

        # Stop if norm (length) of gradient vector is small
        if np.linalg.norm(g) < 1e-6:
            break

        # Descent direction
        H = hessian(x)
        d = -np.linalg.inv(H)@g

        # Step length
        alpha = alpha0

        # Next iterate
        x = x + alpha * d

        # Store iterate for analysis
        x_history.append(x)

    return np.array(x_history)

x0 = [-1,1]
newton(f, df, ddf, x0)
```

Wow! Die Funktion, mit der sich das Gradientenverfahren so abgeplagt hat, erledigt das Newton Verfahren in nur wenigen Iterationen. Tatsächlich hat das Newton Verfahren eine starke Eigenschaft, nämlich *lokal quadratische* Konvergenz.


### Exkurs: Konvergenzgeschwindigkeit
Numerische Verfahren, die eine Folge von Iterierten $\v x^{[k]}$, $k=1,2,\dots$ produzieren, kann man anhand ihrer Konvergenzgeschwindigkeit charakterisieren. Die Analyse der Konvergenzgeschwindigkeit ist ein theoretisches Konstrukt und dient dazu, das Verhalten von Verfahren in der Nähe einer (exakten) Lösung $\v x^*$ zu erklären.
 
Folgende drei Fälle spielen dabei in der Praxis eine Rolle:

Lineare Konvergenz
: Ein Verfahren konvergiert (lokal) **linear**, wenn für aufeinanderfolgende Iterierte $\v x^{[k]}$ und $\v x^{[k+1]}$ gilt:
    \begin{align*}
    \frac{\left\|\v x^{[k+1]}-\v x^*\right\|}{\left\|\v x^{[k]}-\v x^*\right\|}\leq c < 1,\quad \text{für }k\rightarrow \infty
    \end{align*}    
    In Worten: Der Abstand zur Lösung nach dem Schritt ist $c\cdot100\%$ des Abstandes vor dem Schritt. Der Zugewinn wird also kleiner, je näher man der Lösung kommt. Je kleiner dabei der Wert $c$ ist, desto besser. Das deckt sich mit unserer empirischen Beobachtung beim Gradientenverfahren. Dieses ist ein linear konvergentes Verfahren.

Quadratische Konvergenz
: Ein Verfahren konvergiert (lokal) **quadratisch**, wenn für aufeinanderfolgende Iterierte $\v x^{[k]}$ und $\v x^{[k+1]}$ gilt:
    \begin{align*}
    \frac{\left\|\v x^{[k+1]}-\v x^*\right\|}{\left\|\v x^{[k]}-\v x^*\right\|^2}\leq c < 1,\quad   \text{für }k\rightarrow \infty
    \end{align*}
    Die Definition ist etwas technisch und ihre Konsequenzen sind möglicherweise nicht direkt klar. Es bedeutet aber in der Praxis, dass sich in der Nähe der Lösung mit jedem Schritt die Anzahl der korrekten Dezimalstellen in etwa *verdoppelt* -- also eine sehr rapide Konvergenz.
    Die Konvergenzordnung des Newton Verfahrens ist lokal quadratisch.
    
Superlineare Konvergenz
: Ein Verfahren konvergiert (lokal) **superlinear**, wenn für aufeinanderfolgende Iterierte $\v x^{[k]}$ und $\v x^{[k+1]}$ gilt:
    \begin{align*}
    \frac{\left\|\v x^{[k+1]}-\v x^*\right\|}{\left\|\v x^{[k]}-\v x^*\right\|}\leq c_k,
    \end{align*}  
    wobei $c_k$ eine Folge ist, die gegen $0$ konvergiert. Ein Verfahren, das superlinear konvergiert, konvergiert schneller als ein lineare konvergentes Verfahren aber in der Regel langsamer als ein quadratisch konvergentes.

Man sollte noch hervorheben, dass die Konvergenz des Newton Verfahrens *lokal* quadratisch ist. Lokal bedeutet "in der Nähe" der Lösung, was sich oft nicht einfach charakterisieren lässt. Weiter weg von der Lösung verliert es diese Eigenschaft (auch wenn die Hessematrix positiv definit ist). Man kann das Newton Verfahren z.B. mittels einer Liniensuche global konvergent machen. Das heißt, es konvergiert dann von beliebigen Startwerten aus, aber unter Umständen nicht mehr so schnell.

### Newton Verfahren für quadratische Funktionen
Wir haben das Newton Verfahren als lokale Approximation durch ein Taylor-Polynom zweiter Ordnung eingeführt, welches exakt minimiert wird. Das bedeutet aber, dass das Newton Verfahren für eine quadratische Funktion von einem beliebigen Startwert aus konvergiert. Wir rechnen das nach. Sei also

$$
f(\v x)=\frac{1}{2}\v x^T\v A\v x+\v b^T\v x+c,
$$

eine quadratische Funktion mit positiv definiter Hessematrix $\v A$. Dann kann man das Minimum einerseits analytisch bestimmen durch
\begin{align*}
&\nabla f(\v x)=\v A\v x + \v b=0 \Leftrightarrow \v x=-\v A^{-1}\v b
\end{align*}

Andererseits berechnen wir den ersten Schritt des Newton Verfahrens mit beliebigem Startwert $\v x^{[0]}$:
\begin{align*}
\v x^{[1]}=\v x^{[0]}-\v H(\v x^{[0]})^{-1}\nabla f(\v x^{[0]})^T=\v x^{[0]}-\v A^{-1}(\v A\v x^{[0]}+\v b)=-\v A^{-1}\v b
\end{align*}
Unabhängig vom Startwert landet das Verfahren in derselben Lösung $\v A^{-1}\v b$


### Regularisierung des Verfahrens
Wir haben weiter oben schon darauf hingewiesen, dass die Richtung $H(\v x^{[k]})\nabla f(\v x^{[k]})$Newton nur für positiv definite $\v H(\v x^{[k]})$ eine Abstiegsrichtung ist. Falls das nicht der Fall sein sollte, kann die Hessematrix *regularisieren* um einen Abstieg zu erwzingen. Dafür muss man eine Zahl $\lambda^{[k]}>0$ bestimmen, so dass

$$
\v H(\v x^{[k]}) + \lambda^{[k]}\I
$$

positiv definit ist. $\I$ steht hier für die Einheitsmatrix. Man kann zeigen, dass $\lambda^{[k]}$ mindestens so groß sein muss wie der Betrag des kleinsten Eigenwertes von $\v H(\v x^{[k]})$ (da $\v H(\v x^{[k]})$ nicht positiv definit ist, ist dieser auf jeden Fall negativ).

Der regularisierte Newton Schritt ist dann

$$
\v x^{[k+1]}=\v x^{[k]} - (\v H(\v x^{[k]}) + \lambda^{[k]}\I)^{-1}\nabla f(\v x^{[k]})^T
$$

Typischerweise wird man versuchen $\lambda^{[k]}$ so klein wie möglich zu wählen. Es aber interessant festzustellen, dass sich die Abstiegsrichtung des regularisierten Newton Schrittes mit steigendem $\lambda^{[k]}$ immer mehr der Richtung des steilsten Abstiegs annähert. Allerdings wird der Schritt mit sehr kleiner Schrittweite, proportional zu $\frac{1}{\lambda^{[k]}}$ ausgeführt.


### Newton Verfahren als Methode zur Bestimmung von Nullstellen
Ursrpünglich wurde das Newton Verfahren nicht als Optimierungsverfahren erfunden, sondern als Methode um nichtlineare Gleichungen zu lösen. Das Lösen nichtlinearer Gleichungen ist aber dasselbe wie die Nullstellen von Funktionen zu bestimmen. Nullstellenprobleme sind Probleme der Form $\v g (\v x)=\v 0$, wobei $\v g:\R^n\rightarrow\R^n$ eine vektorwertige Funktion ist (historisch wurden nur Polynomfunktionen untersucht). Die Iterationsvorschrift für das Nullstellenproblem lautet

$$
\v x^{[k+1]}=\v x^{[k]}-\nabla \v g(\v x^{[k]})^{-1}\v g(\v x^{[k]})
$$

Im Kontext der Optimierung kann man sich das Newton Verfahren als einen Ansatz zum iterativen Lösen der Optimalitätsbedingungen erster Ordnung, $\nabla f(\v x)=\v 0$ vorstellen ($\nabla f(\v x)$ spielt dann die Rolle der Funktion $\v g$). Das erklärt auch das Verhalten des Newton Verfahrens, möglicherweise zu Maxima oder Sattelpunkten zu konvergieren, da die Optimalitätsbedingungen erster Ordnung zwischen diesen ja auch keinen Unterschied machen. Erklärungen zum klassischen Newton Verfahren für Nullstellen findet man z.B. [hier](https://de.wikipedia.org/wiki/Newtonverfahren).
% TODO Ausbauen


## Nachteile des Newton Verfahrens
Wir haben im vorherigen Abschnitt gesehen, wie das Newton-Verfahrens gegenüber Verfahren erster Ordnung ein dramatische beschleunigtes Konvergenzverhalten aufweisen kann. Leider gehen damit einige Nachteile einher, die wir hier noch einmal kurz zusammenfassen.

Auswertung der Hessematrix
: In jedem Schritt müssen alle zweiten Ableitungen ausgewertet werden. Dies sind, da die Hessematrix eine symmetrische $n\times n$-Matrix ist, $n(n+1)/2$ Terme. Bei komplizierten Funktionen stellt das einen erheblichen Mehraufwand pro Iteration dar.

Invertierung der Hessematrix
: In jeder Iteration muss die Hessematrix invertiert werden. Genauer gesagt: es muss ein lineares Gleichungssystem in $n$ Gleichungen und $n$ Variablen gelöst werden. Dies geschieht ebenfalls mit Hilfe numerischer Algorithmen (z.B. der [Cholesky-Zerlegung](https://de.wikipedia.org/wiki/Cholesky-Zerlegung)), deren Rechenaufwand in der Regel kubisch mit der Anzahl der Variablen wächst. Das bedeutet, für die doppelte Anzahl an Variablen entsteht der $2^3=8$-fache Aufwand.

Keine Abstiegsrichtung
: Abseits der Lösung kann es sein, dass die Hessematrix nich positiv definit ist. In diesem Fall ist der Newton-Schritt keine Abstiegs-, sondern eine Aufstiegsrichtung. Man kann den Newton-Schritt dann regularisieren. Dies ist aber mit zusätzlichem Aufwand verbunden und die entstehenden Abstiegsrichtung ähnelt einem (kurzen) Gradientenabstiegsschritt.

Speicherplatz
: Neben dem Rechenaufwand für die Berechnung des Schrittes ist auch der benötigte Speicherplatz nicht zu untersätzen. Beispiel: Die Hessematrix einer Funktion mit $10000$ Variablen besitzt $10000\cdot 10001/2=50005000$ Einträge. Wenn jeder Eintrag $8$ Bytes belegt, wären das etwa $400$ MB. Bei $20000$ Variablen beträgt der Speicherplatzbedarf bereits $1.6$ GB.


## Quasi-Newton Verfahren

### Idee von Quasi-Newton Verfahren
Quasi-Newton Verfahren versuchen, den Vorteil der schnellen Konvergenz von Verfahren zweiter Ordnung beizubehalten, aber dabei die Nachteile zu umgehen. Die Grundidee ist es, eine Approximation der Hessematrix bzw. ihrer Inversen zu konstruieren und diese in jedem Schritt des Abstiegsverfahren basierend auf der vorherigen Iteration zu aktualisieren statt komplett neu zu berechnen.

Wir konzentrieren uns zunächst den ersten der vier Nachteile des Newton-Verfahrens: die Notwendigkeit, zweite Ableitungen auszuwerten, um Krümmungsinformation zu erhalten. Denn wie wir gesehen haben, produziert die Krümmungsinformation bessere Abstiegsrichtungen. Können wir Krümmungsinformation nicht auch bekommen, ohne zweite Ableitungen zu berechnen? Dazu betrachten wir zunächst ein eindimensionales Beispiel, das illustriert, was unter "Krümmung" eigentlich zu verstehen ist. Wir betrachten die Funktion

$$
f(x)=\frac{1}{4}x^4-3x^2-8x
$$

Die Steigung der Sekante an die Funktion $f$, die durch zwei Iterierte $x^{[k]}$ und $x^{[k+1]}$ geht, kann man als Approximation der *Tangentensteigung* im Punkt $x^{[k+1]}$ betrachten, also der ersten Ableitung: 

\begin{align*}
f'(x^{[k+1]})\approx \frac{f(x^{[k+1]})-f(x^{[k]})}{x^{[k+1]}-x^{[k]}}\label{eq:sek1}
\end{align*}

```{figure} ./bilder/sekante1.png
:width: 400px
Sekante an $f(x)$ als Approximation der ersten Ableitung im Punkt $x^{[k+1]}$. 
```

Mit dem gleichen Argument kann man die Steigung der Sekante an die erste Ableitung $f'$ als Approximation der Tangentensteigung der ersten Ableitung im Punkt $x^{[k+1]}$ betrachten, also der zweiten Ableitung:

$$
f''(x^{[k+1]})\approx \frac{f'(x^{[k+1]})-f'(x^{[k]})}{x^{[k+1]}-x^{[k]}}
$$(eq:sek1)

```{figure} ./bilder/sekante2.png
:width: 400px
Sekante an $f'(x)$ als Approximation der zweiten Ableitung im Punkt $x^{[k+1]}$.
```

Wir führen folgende Abkürzungen ein:
\begin{align*}
s^{[k]}&:=x^{[k+1]}-x^{[k]}\\
g^{[k]}&:=f'(x^{[k+1]})-f'(x^{[k]})
\end{align*}

Damit können wir die Gleichung {eq}`eq:sek1` schreiben als:

$$
f''(x^{[k+1]})\approx \frac{g^{[k]}}{s^{[k]}}
$$(eq:sek2)

oder auch 

$$
f''(x^{[k+1]})s^{[k]}\approx g^{[k]}
$$(eq:sek3)

Wir nennen {eq}`eq:sek3` die *Sekantenbedingung*. Der Unterschied zwischen {eq}`eq:sek2` und {eq}`eq:sek3` ist, dass man {eq}`eq:sek3` auch für mehrdimensionale Funktionen formulieren kann:

$$
\nabla^2 f(\v x^{[k+1]})\v s^{[k]}\approx \v g^{[k]}
$$(eq:sek4)

Die zweite Ableitung $\nabla^2 f(\v x^{[k+1]})$ ist nun eine quadratische und symmetrische Matrix, $\v s^{[k]}$ und $\v g^{[k]}$ sind Vektoren. Die Aussage {eq}`eq:sek4` ist also eine Aussage für eine bestimmte *Richtung*, nämlich $\v s^{[k]}$, die Richtung des letzten Schritts.

Diese Sekantenbedingung ist die Grundlage von Quasi-Newton Verfahren und sie führt zu einigen der erfolgreichsten Verfahren für ableitungsbasierte Optimierung. Wir möchten einerseits die Hessematrix einer mehrdimensionalen Funktion $\nabla^2 f$ mit einer Matrix $\v B^{[k]}$ approximieren, andererseits aber $\nabla^2 f$ nicht berechnen. Wir fordern von unserer Approximation, dass sie die Krümmung wenigstens in eine Richtung $\v s^{[k]}$ approximiert. Dies ist eine Näherung für die zweite Ableitung in dieser Richtung. Wir wollen also, dass

$$
\v B^{[k+1]}\v s^{[k]}=\v g^{[k]},
$$

wobei $\v s^{[k]}=\v x^{[k+1]}-\v x^{[k]}$ der Schritt und $g^{[k]}:=\nabla f(x^{[k+1]})^T-\nabla f(x^{[k]})^T$ die Differenz der Gradienten (als Spaltenvektor) ist.

Zusammenfassend: Wir suchen eine Matrix $\v B^{[k+1]}$, für die gilt:
1. $\v B^{[k+1]}$ erfüllt die Sekantenbedingung $\v B^{[k+1]}\v s^{[k]}=\v g^{[k]}$
2. $\v B^{[k+1]}$ ist symmetrisch, wie die Hessematrix
3. $\v B^{[k+1]}$ ist positiv definit, damit Abstieg garantiert ist.

Da eine symmetrische $n\times n$-Matrix mehr Einträge, also Freiheitsgrade hat als die Anzahl dieser Bedingungen, gibt es viele Matrizen, die alle diese Bedingungen erfüllen, genauer gesagt: unendlich viele.

### Das DFP-Update
Die Idee des *Davidon-Fletcher-Powell-Updates* *(DFP-Update)* ist es, die neue Approximation $\v B^{[k+1]}$ als diejenige Matrix zu wählen, die die drei Bedingungen oben erfüllt und die am *nächsten* an der aktuellen Approximation $\v B^{[k]}$ liegt, d.h. 

$$
\v B^{[k+1]} = \argmin{} \norm{\v B-\v B^{[k]}}
$$

Das $\argmin{B}$ bedeutet: $\v B^{[k+1]}$ soll aus allen Matrizen $\v B$, die die drei Bedingungen oben erfüllen, diejenige sein, für die der Ausdruck $\norm{\v B-\v B^{[k]}}$ minimal wird. Je nachdem, welche Matrixnorm man hier benutzt, erhält man unterschiedliche Hessematrix Approximationen als Lösung dieses Problems. Für die Frobenius-Norm (quadriere alle Einträge der Matrix, bilde die Summe und ziehe die Wurzel -- also genauso wie die Euklidische Norm für Vektoren funktioniert) kann man theoretisch beweisen, dass dies für folgende Matrix $\v B^{[k+1]}$ der Fall ist (der Einfachheit halber lassen wir auf der rechten Seite das Superscript $^{[k]}$ weg, d.h. $\v B:=\v B^{[k]}, \v s=\v s^{[k]}, \v g=\v g^{[k]}$):

$$
\v B^{[k+1]}=\left( \I - \frac{\v g\v s^T}{\v g^T\v s}\right)\v B
\left( \I - \frac{\v s\v g^T}{\v g^T\v s}\right)+\frac{\v g\v g^T}{\v g^T\v s}
$$(eq:dfp)

Bevor wir in die Details dieser kompliziert anmutenden Formel eintauchen, stellen wir fest, dass die Berechnung von $\v B^{[k+1]}$ nur auf drei Größen basiert:
1. Die aktuelle Approximation der Hessematrix $\v B:=\v B^{[k]}$.
2. Die Differenz der Gradienten aus der aktuellen und der vorherigen Iteration: $\v g=\v g^{[k]}=\nabla f(\v x^{[k+1]})^T-\nabla f(\v x^{[k]})^T$.
3. Die Differenz der Iterierten aus der aktuellen und der vorherigen Iteration (der Schritt): $\v s^{[k]}=\v x^{[k+1]}-\v x^{[k]}$.

Dies ist eine weitere zentrale Idee von Quasi-Newton Verfahren: die Verwendung von *Update-Formeln* für die Berechnung der Approximation der Hessematrix, die nur Größen verwenden, die ohnehin in der akuellen Iteration verfügbar sind. Die Update-Formeln sehen zwar kompliziert aus, der Rechenaufwand ist aber relativ gering. Schauen wir uns die einzelnen Elemente der Berechnung einmal genauer an:
- $\v g^T\v s$ ist ein Skalar, der durch die Multiplikation des Zeilenvektors $\v g^T$ mit dem Spaltenvektor $\v s$ entsteht.  $\v g^T\v s$ ist ein Spezialfall eines *inneren Produktes*
- Die Ausdrücke $\v g\v s^T$, $\v s\v g^T$ und $\v g\v g^T$ sind sogenannte *äußere Produkte*: Ein Spaltenvektor multipliziert mit einem Zeilenvektor ergibt ein Matrix vom Rang 1.
- Schließlich bezeichnet $\I$ noch die $n\times n$ Einheitsmatrix.

Die Matrix $\v B=\v B^{[k]}$ wird also von links und rechts mit einer Matrix multipliziert und anschließend wird eine weitere Rang 1-Matrix $\frac{\v g\v g^T}{\v g^T\v s}$ addiert. 

Es stellt sich heraus, dass die Update Formel einen weiteren Vorteil gegenüber der exakten Hessematrix hat: Statt einer Approximation der Hessematrix kann man auch eine Approximation der *Inversen* der Hessematrix vorhalten und updaten.
Mit der [Sherman-Morrison-Woodbury-Formel](https://de.wikipedia.org/wiki/Sherman-Morrison-Woodbury-Formel) kann man die Formeln analytisch umformulieren und erhält folgende Formel für die Approximation der Inversen $\v A^{[k+1]}=(\v B^{[k+1]})^{-1}$:

$$
\v A^{[k+1]}=\v A-\frac{\v A \v g\v g^T \v A}{\v g^T\v A \v g}+\frac{\v s \v s^T}{\v g^T \v s}
$$(eq:dfp-inv)

Damit wäre auch der zweite Nachteil des Newton-Verfahrens, die Notwendigkeit, in jeder Iteration eine Matrix zu invertieren, behoben. 

Eine Updateformel ist natürlich noch kein fertiger Algorithmus. Bevor wir uns ein komplettes Quasi-Newton Verfahren anschauen, schauen wir uns noch eine zweite Update-Formel an. Das DFP-Update wurde zuerst von W. C. Davidon entdeckt[^fn:davidon] und 1960 unabhängig von Fletcher und Powell beschrieben. Der Erfolg des Verfahrens führte zu einer verstärkten Forschungsaktivität im Bereich der Quasi-Newton Methoden. Im Jahre 1970 entdeckten die vier Autoren Broyden, Fletcher, Goldfarb und Shanno schließlich unabhängig(!) voneinander[^fn:bfgs] das bis heute erfolgreichste und meistgenutzte Quasi-Newton Update. 

[^fn:davidon]: *William Davidon: Variable metric method for minimization. In: Argonne National Laboratory (Hrsg.): A.E.C. Research and Development Report. ANL-5990, 1959.*

[^fn:bfgs]: 
    *Charles G. Broyden: The convergence of a class of double-rank minimization algorithms. In: Journal of the Institute of Mathematics and Its Applications. Band 6, 1970, S. 76–90, doi:10.1093/imamat/6.1.76.*
    
    *Roger Fletcher: A New Approach to Variable Metric Algorithms. In: Computer Journal. Band 13, Nr. 3, 1970, S. 317–322, doi:10.1093/comjnl/13.3.317.*
    
    *Donald Goldfarb: A Family of Variable Metric Updates Derived by Variational Means. In: Mathematics of Computation. Band 24, Nr. 109, 1970, S. 23–26, doi:10.1090/S0025-5718-1970-0258249-6.*
    
    *David F. Shanno: Conditioning of quasi-Newton methods for function minimization. In: Mathematics of Computation. Band 24, Nr. 111, Juli 1970, S. 647–656, doi:10.1090/S0025-5718-1970-0274029-X.*

### Das BFGS-Update
Das *Broyden-Fletcher-Goldfarb-Shanno-Update* *(BFGS-Update)* lässt sich auf ähnlichem Wege herleiten wie das DFP-Update. Statt von der Sekantenbedingung $\v B^{[k+1]}\v s^{[k]}=\v g^{[k]}$ auszugehen, formuliert man die Sekantenbedingung um

\begin{align*}
\v B^{[k+1]}\v s^{[k]}&=\v g^{[k]}\\ \Leftrightarrow (\v B^{[k+1]})^{-1}\v B^{[k+1]}\v s^{[k]}&=(\v B^{[k+1]})^{-1}\v g^{[k]}
\end{align*}

Mit der Kurzform $\v A^{[k+1]}=(\v B^{[k+1]})^{-1}$ erhält man die äquivalente Form der Sekantenbedingung $\v A^{[k+1]}\v g^{[k]}=\v s^{[k]}$. Ein ähnliches Argument wie beim DFP Update -- die Approximation soll die äquivalente Sekantenbedingung erfüllen, symmetrisch sein und möglichst nahe bei der aktuellen Approximation liegen -- führt zum BFGS Update. Wie beim DFP-Update kann man entweder eine Approximation der Hessematrix $\v B^{[k+1]}$ oder der Inverse $\v A^{[k+1]}$ vorhalten. Die Formeln lauten:

$$
\v B^{[k+1]}=\v B-\frac{\v B \v s\v s^T \v B}{\v s^T\v B \v s}+\frac{\v g \v g^T}{\v s^T \v g}
$$(eq:bfgs)

für die Approximation der Hessematrix und

$$
\v A^{[k+1]}=\left( \I - \frac{\v s\v g^T}{\v s^T\v g}\right)\v A
\left( \I - \frac{\v g\v s^T}{\v s^T\v g}\right)+\frac{\v s\v s^T}{\v s^T\v g}
$$(eq:bfgs-inv)

für ihre Inverse. Beim Vergleich der Formeln {eq}`eq:bfgs-inv` und {eq}`eq:dfp` bzw. {eq}`eq:bfgs` und {eq}`eq:dfp-inv` fällt auf, dass DFP-Update und BFGS-Update *dual* zueinander sind. Man erhält das eine aus dem anderen, indem man die Buchstaben $\v A$ und $\v B$ sowie $\v s$ und $\v g$ miteinander vertauscht.

Eine weitere wichtige Eigenschaft der beiden Update-Formeln ist die Tatsache, dass es *Rang-2 Updates* sind: Die ursprüngliche Approximation $\v B^{[k]}$ wird modifiziert, indem zwei Rang-1-Matrizen (äußere Produkte von Vektoren) als "Korrekturterme" addiert werden. Die rekursive Definition bedeutet auch, dass man mit einer Matrix vollen Ranges starten muss. Häufig nimmt man hier eine skalierte Einheitsmatrix oder auch die (dann einmalig auszuwertende) exakte Hessematrix.

Es gibt viele weitere Rang-2-Updates, die ähnlich funktionieren wie das DFP und das BFGS-Update. Das BFGS-Update wird am häufigsten verwendet, da es (empirisch) die besten Resultate liefert, d.h. die besten Abstiegsrichtungen. Das vollständige *BFGS-Verfahren* sieht wie folgt aus:

````{prf:algorithm} BFGS Verfahren
:label: alg:bfgs
Gegeben: 
: Differenzierbare Funktion $f:\R^n\rightarrow\R$.

Gesucht: 
: Lokales Minimum von $f$.

**Algorithmus**:

Starte mit initialer Schätzung $\v x^{[0]}$ und $\v A^{[0]}$, setze $k=0$.

Für $k=0,1,2,\dots$:
1. Überprüfe, ob $\v x^{[k]}$ die **Abbruchbedingung** erfüllt. 
    - Falls ja: Abbruch mit Lösung $\v x^{[k]}$
    - Falls nein: gehe zu Schritt 2.
2. Bestimme **Abstiegsrichtung** $\v d^{[k]}$ durch
    \begin{align*}
    \v d^{[k]}=-\v A{[k]}^{-1}\nabla f(\v x^{[k]})^T
    \end{align*}
3. Bestimme **Schrittweite** $\alpha^{[k]}$ durch Liniensuche.
4. Berechne neue **Iterierte** $\v x^{[k+1]}=\v x^{[k]}+\alpha^{[k]}\v d^{[k]}$. 

   Setze
    \begin{align*}
    \v s^{[k]}&=\alpha^{[k]}\v d^{[k]}\\
    \v g^{[k]}&=\nabla f(\v x^{[k]})^T-\nabla f(\v x^{[k+1]})^T
    \end{align*}
5. Berechne neue Approximation der Inversen der Hessematrix $\v A^{[k+1]}$ aus $\v A^{[k]}, \v s^{[k]}$ und $\v g^{[k]}$ mit dem **BFGS-Update**.
````

Anmerkungen zu dem Verfahren:
- Wenn im ersten Schritt für $\v A^{[0]}$ die Einheitsmatrix $\I$ gewählt wird, entspricht der erste Schritt im Verfahren einem Gradientenabstieg.
- Durch eine geeignete Liniensuche (backtracking Liniensuche) kann man erreichen, dass $\v A^{[k+1]}$ immer positiv definit ist, wenn $\v A^{[k]}$ positiv definit war.
- Die Folge $\v A^{[k]}$, $k=0,1,2,\dots$ konvergiert nicht unbedingt gegen die echte Hessematrix, d.h. im Grenzfall erhält man nicht unbedingt das Newton Verfahren.

Wir schauen uns das Verfahren anhand eines numerischen Beispiels an.
````{prf:example}
Es soll die Funktion $f(x_1,x_2)=x_1^2+0.5x_2^2+3$ minimiert werden. Der Gradient von $f$ ist $\nabla f(x_1,x_2)=2x_1+x_2$. Wir zeigen den ersten Schritt des BFGS-Verfahrens.

Der Startwert für die Iterierte sei $\v x^{[0]}=\bmats 1\\2\emats$ und der Startwert für die Hessematrix Approximation sei die Einheitsmatrix $\v A^{[0]}=\bmats 1&0\\0&1\emats$. Der Einfachheit halber nehmen wir an, das $\alpha^{[k]}=1$. 

$k=0$
: - Abstiegsrichtung bestimmen: 
    \begin{align*}
    \v d^{[0]}=-\v A^{[0]}\nabla f(1,2)^T=-\bmat 1&0\\0&1\emat\bmat 2\\2\emat=\bmat -2\\-2\emat
    \end{align*}

  - Nächste Iterierte:
    \begin{align*}
    \v x^{[1]} &= \v x^{[0]}+\v d^{[0]}=\bmat -1\\0 \emat\\
    \v s^{[0]} &= \bmat -2\\ -2\emat\\
    \v g^{[0]} &= \nabla f(-1,0)^T-\nabla f(1,2)^T=\bmat -2\\0\emat -\bmat 2\\2 \emat=\bmat -4\\-2\emat
    \end{align*}

  - BFGS Update (denken Sie sich das Superscript $^{[0]}$ dazu):
    \begin{align*}
    \v A^{[1]}=\left( \I - \frac{\v s\v g^T}{\v s^T\v g}\right)\v A
\left( \I - \frac{\v g\v s^T}{\v s^T\v g}\right)+\frac{\v s\v s^T}{\v s^T\v g}
    \end{align*}
    Mit $\v s^T\v g = (-2)(-4)+(-2)(-2)=12$ ergibt sich
    \begin{align*}
    \v A^{[1]}&=\left( \bmat 1&0\\0&1\emat - \frac{1}{12}\bmat 8&4\\8&4\emat\right)\bmat 1&0\\0&1\emat
\left( \bmat 1&0\\0&1\emat - \frac{1}{12}\bmat 8&4\\8&4\emat\right)+\frac{1}{12}\bmat 4&4\\4&4\emat\\
    &=\frac{1}{9}\bmat 5&-1\\-1&11\emat
    \end{align*}

$k=1$
: - Abstiegsrichtung bestimmen:
    \begin{align*}
    \v d^{[1]}=-\v A^{[1]}\nabla f(-1,0)^T=-\frac{1}{9}\bmat 5&-1\\-1&11\emat\bmat -2\\0\emat=\frac{1}{9}\bmat 10\\-2\emat
    \end{align*}
  - usw.
````

Das BFGS-Verfahren behebt drei der vier Nachteile des Newton-Verfahrens (Auswertung der Hessematrix, Invertierung der Hessematrix, positive Definitheit) und tatsächlich ist das BFGS-Verfahren für viele Optimierungsprobleme eine gute Wahl. Es braucht meist mehr Iterationen als das Newton-Verfahren. Auch die theoretischen Konvergenzeigenschaften sind etwas schlechter als beim Newton-Verfahren, es konvergiert *superlinear*. Allerdings ist es oft trotzdem schneller, da eine Iteration wesentlich weniger aufwendig ist. Es ist außerdem erheblich schneller als ein Gradientenabstieg, da bereits ein wenig Krümmungsinformation (wie sie durch das BFGS-Update reflektiert wird) ausreicht, um bessere Iterierte zu erzeugen und mehr Fortschritt in Richtung der Lösung zu erzielen.


### Limited-memory BFGS
Ein Nachteil des Newton-Verfahrens wird durch das normale BFGS-Update jedoch nicht beseitigt, nämlich dass man die gesamte Hessematrix(-approximation) bzw. deren Inverse speichern muss. Für große Optimierungsprobleme ist der Speicherbedarf alles andere als vernachlässigbar. So benötigt man für ein Optimierungsproblem mit $25,000$ Variablen ca. $25,000 \times 25,000 \times 8$ Byte $=5$ Gigabyte Speicherplatz (oder etwa die Hälfte, wenn nur die obere Dreiecksmatrix gespeichert wird).

Die Idee des *Limited-memory BFGS-Verfahrens* (*L-BFGS-Verfahren*) ist es, nur Krümmungsinformation aus den letzten $m$ Iterationen zu verwenden, wobei $m$ nicht zu groß gewählt wird, etwa $m=20$. Die Motivation dahinter ist, dass die Krümmungsinformation an dem Punkt, an dem das Verfahren vor mehr als $m$ Iterationen war, nicht mehr relevant für die aktuelle Iteration ist, da die Funktion in der Umgebung der aktuellen Iteration wahrscheinlich ganz anders gekrümmt ist. Den Begriff *memory* kann man hier auch mit dem Wort *Gedächtnis* übersetzen. Wie hilft uns das bei unserem anderen *memory*-Problem, nämlich dem *Speicherplatz*-Problem?

Zunächst ist klar, das die vollständige Krümmungsinformation der letzten $m$ Iterationen implizit in den Vektoren $\v s^{[k-i]}, \v g^{[k-i]}$, $i=1,\dots,m$ steckt. Das Ziel des L-BFGS-Verfahrens ist, anstatt der gesamten Matrix nur diese $2m$ Vektoren zu speichern, die das BFGS-Update *implizit* repräsentieren. Wie können wir aber die Hessematrix $\v A^{[k]}$ benutzen, ohne sie explizit aus den Vektoren $\v s^{[k-i]}$ und $\v g^{[k-i]}$ aufzubauen?

Wenn wir uns {prf:ref}`alg:bfgs` anschauen, stellen wir fest, dass das Verfahren die Matrix $\v A^{[k]}$ nur benötigt, um den Schritt zu berechnen:

$$
\v d^{[k]}=-\v A^{[k]}\nabla f(\v x^{[k]})^T
$$

Wir brauchen also nicht die Matrix $\v A^{[k]}$, sondern Matrix-Vektor Produkte  $\v A^{[k]}f(\v x^{[k]})^T$. Dies kann man tatsächlich nur mittels inneren Produkten und Summen von Vektoren erreichen. Für die Details dieses Algorithmus sei auf die Literatur verwiesen[^fn:l-bfgs]. Zusammenfassend: Man kann das Matrix-Vektor Produkt mit der BFGS-Approximation $\v A^{[k]}f(\v x^{[k]})^T$ berechnen, ohne die BFGS-Approximation $\v A^{[k]}$ zu kennen. Es reicht aus, die Vektoren $\v s^{[k]}$  und $\v g^{[k]}$ aus den letzten $m$ Iterationen zu speichern. Dadurch wird Speicherplatz gespart.

[^fn:l-bfgs]: Algorithm 7.4 (S. 177) in J. Nocedal, und S. J. Wright. Numerical Optimization. 2nd ed. Springer Series in Operations Research. New York: Springer, 2006.

Damit können wir den vollständigen L-BFGS Algorithmus skizzieren:

````{prf:algorithm} Limited-memory BFGS Verfahren
:label: alg:lbfgs
Gegeben: 
: Differenzierbare Funktion $f:\R^n\rightarrow\R$.

Gesucht: 
: Lokales Minimum von $f$.

**Algorithmus**:

Gegeben: $m>0$. Starte mit initialer Schätzung $\v x^{[0]}$, setze $k=0$.

Für $k=0,1,2,\dots$:
1. Überprüfe, ob $\v x^{[k]}$ die **Abbruchbedingung** erfüllt. 
    - Falls ja: Abbruch mit Lösung $\v x^{[k]}$
    - Falls nein: gehe zu Schritt 2.
2. Wähle initiale Approximation der Hessematrix $\v A_0^{[k]}$.
2. Bestimme **Abstiegsrichtung**
    \begin{align*}
    \v d^{[k]}=-\v A{[k]}^{-1}\nabla f(\v x^{[k]})^T
    \end{align*}
    durch "matrixfreies" Matrix-Vektor Produkt mit der BFGS-Approximation der Inversen der Hessematrix. Benutze dazu die Vektorpaaren $\{\v s^{[k-i]},\v g^{[k-i]}\}$, $i=1,\dots,m$.
3. Bestimme **Schrittweite** $\alpha^{[k]}$ durch Liniensuche.
4. Berechne neue **Iterierte** $\v x^{[k+1]}=\v x^{[k]}+\alpha^{[k]}\v d^{[k]}$. 
5. Falls $k>m$: Lösche Vektorpaar $\{\v s^{[k-m]},\v g^{[k-m]}\}$ aus dem Speicher.
6. Setze
    \begin{align*}
    \v s^{[k]}&=\alpha^{[k]}\v d^{[k]}\\
    \v g^{[k]}&=\nabla f(\v x^{[k]})^T-\nabla f(\v x^{[k+1]})^T
    \end{align*}
    und füge $\{\v s^{[k]},\v g^{[k]}\}$ zum Speicher hinzu.
````
Anmerkungen:
- Schritt 2: Da man das Update in jedem Schritt ja aus den letzten $m$ Iterationen neu aufbaut, kann man auch in jedem Schritt eine andere initiale Hessematrix-Approximation wählen.
- In den ersten $m$ Iterationen produzieren BFGS und L-BFGS die gleichen Iterierten (bei gleicher Wahl der $\v A_0^{[k]}=\v A^{[0]}$). Danach unterscheiden Sie sich, da im BFGS Update immer noch Spuren von allen Iterationen vorhanden sind, während das L-BFGS Update diese explizit nicht berücksichtigt (die entsprechenden Vektoren $\v s^{[k-m]}, \v g^{[k-m]}$ werden gelöscht).

L-BFGS ist für viele unbeschränkte Optimierungsprobleme das Mittel das Wahl. Es ist
- Effizient in der Laufzeit
- Effizient im Speicherbedarf
- Relativ robust, es müssen nur wenige Hyperparameter getunt werden
- Es sind gute Implementierungen verfügbar, z.B. in [scipy](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-lbfgsb.html).


## Zusammenfassung der Verfahren erster und zweiter Ordnung
In den vergangenen beiden Kapiteln haben wir eine ganze Reihe von Verfahren zur Minimierung von differenzierbaren Funktionen kennengelernt. Alle Verfahren haben folgende Gemeinsamkeiten:

1. Sie finden *lokale* Minima von Funktionen. Das Suchen eines *globalen* Minimums nicht-konvexer Funktionen ist eine wesentlich schwierigere Aufgabe. Stand heute kann das in vertretbarer Zeit nur für Funktionen mit wenigen dutzend Variablen geleistet werden. Ein pragmatischer Ansatz, die vorgestellten Verfahren zu verbessern, ist der *multi-start* Ansatz: man startet das Verfahren mehrmals von unterschiedlichen Startwerten und hofft, dass es zu unterschiedlichen Minima konvergiert. Unter diesen wählt man das das beste aus.

2. Für viele der Verfahren kann theoretisch bewiesen werden, dass sie konvergieren. In der Praxis kann aber doch noch einiges schief gehen: zum einen ist nie gesagt nach *wie vielen* Schritten die Verfahren konvergieren, zum anderen rechnet man in der Regel mit endlicher Präzision, d.h. numerische Rundungsfehler können dazu führen, dass ein Verfahren in der Praxis nicht konvergiert.

3. Alle Verfahren arbeiten erzeugen eine Folge von *Iterierten*, d.h. Vektoren $\v x^{[0]}, \v x^{[1]}, \v x^{[2]},\dots$. Die nächste Iterierte wird aus der vorherigen mit einer *Abstiegsrichtung* $\v d^{[k]}$ mutlipliziert mit einer skalaren *Schrittweite* $\alpha^{[k]}$ gewonnen: $\v x^{[k+1]}=\v x^{[k]}+\alpha^{[k]}\v d^{[k]}$. Den Unterschied $\v x^{[k+1]}-\v x^{[k]}$ nennt man auch *Schritt*.

4. Alle Verfahren benötigen neben dem Funktionswert an einer beliebigen Stelle auch den Wert der Ableitung (erste und/oder zweite) an einer beliebigen Stelle.

Die folgende Tabelle gibt eine Übersicht über die vorgestellten Verfahren

| Name    |  Abstiegsrichtung  |  Schrittweitensteuerung | Vorteile | Nachteile |
| :--- | ---| ---| ---| --- |
| Gradientenabstieg   |  $\v d^{[k]}$$=-\nabla f(\v x^{[k]})^T$  | - Konstant<br>- Dämpfung<br>- Liniensuche    | - Einfach zu implementieren<br>- Einfach zu verstehen| - Langsame Konvergenz da oft schlechte Abstiegsrichtung<br>- Zick-Zack-Verhalten<br>- Kriechverhalten in flachen Gegenden| 
| Gradientenabstieg <br> mit Momentum  |  $\v d^{[k]}$$=\beta \v d^{[k-1]}-\nabla f(\v x^{[k]})^T$  | - Konstant<br>- Dämpfung<br>- Liniensuche    | Zick-Zack- und Kriechverhalten wird abgemildert| - Evtl. keine gute Abstiegsrichtung<br>- Evtl. zu viel Momentum in der Nähe der Lösung | 
| Normalisierter <br>Gradientenabstieg  |  $\v d^{[k]}$$=-\frac{\nabla f(\v x^{[k]})^T}{\norm{\nabla f(\v x^{[k]})}}_2$  | - Konstant<br>- Dämpfung<br>- Liniensuche    | Kriechverhalten wird abgemildert| Alle sonstigen Nachteile des Gradientenabstiegs | 
| Newton-Verfahren  |  $\v d^{[k]}$$=-\nabla^2f(\v x^{[k]})^{-1}\nabla f(\v x^{[k]})^T$  | Nicht notwendig    | Lokal sehr schnelle Konvergenz | - Auswertung der Hessematrix in jedem Schritt <br> - Invertierung der Hessematrix in jedem Schritt <br> - Speicherplatzbedarf <br> - Evtl. keine Abstiegsrichtung  | 
| BFGS-Verfahren  |  $\v d^{[k]}$$=-\v A^{[k]}\nabla f(\v x^{[k]})^T$  | Liniensuche    | - Lokal schnelle Konvergenz <br> - Einfache Berechnung der Approximation der Inversen der Hessematrix <br> - Abstiegsrichtung garantiert  | Speicherplatzbedarf bei großen Problem | 
| L-BFGS-Verfahren  |  $\v d^{[k]}$$=-\v A^{[k]}\nabla f(\v x^{[k]})^T$  | Liniensuche    | - Lokal (oft) schnelle Konvergenz <br> - Einfache Berechnung der Approximation der Inversen der Hessematrix <br> - Abstiegsrichtung garantiert <br> - Geringer Speicherplatzbedarf | | 
