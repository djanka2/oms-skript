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
:label: alg:gd_allgemein
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
%TODO Ausbauen


## Quasi-Newton Verfahren

### DFP 

### BFGS

### Limited-memory BFGS

## Zusammenfassung der Verfahren erster und zweiter Ordnung
