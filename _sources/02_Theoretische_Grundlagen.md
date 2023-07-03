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

(sec:theo)=
# Grundlagen der nichtlinearen Optimierung
Aufbauend auf dem vorherigen Kapitel führen wir diesem Kapitel die Grundlagen der nichtlinearen Optimierung ein, insbesondere die *Optimalitätsbedingungen*. Diese liegen den Optimierungsverfahren, die wir in dieser Vorlesung betrachten, zugrunde. Als weiteres theoretisches Werkzeug beschäftigen wir uns mit Taylor-Entwicklungen differenzierbarer Funktionen, die zweite wichtige Zutat bei der Herleitung von Optimierungsverfahren. Außerdem schauen wir uns auch schon direkt die einfachste Form des Gradientenverfahrens an. Zunächst aber führen wir einige Grundbegriffe ein. 

## Grundbegriffe
Was ist eigentlich ein Optimierungsproblem? Bei einem Optimierungsproblem besteht die Aufgabe darin, einen Vektor $\v x$ zu suchen, so dass eine Funktion $f(\v x)$, also ein mathematischer Ausdruck, der von $\v x$ abhängt, *minimal* oder *maximal* wird. In der Mathematik gibt es eine standardisierte Form um Optimierungsprobleme zu spezifizieren.
````{prf:definition} Optimierungsproblem
Ein *Optimierungsproblem* ist ein Problem der Form
\begin{align*}
\min_{\v x\in D\in\R^n} f(\v x)
\end{align*}
Dabei nennen wir 
- $D\subseteq \R^n$ den *Definitionsbereich*,
- $f:\R^n\rightarrow \R$ die *Zielfunktion* (manchmal auch *Kostenfunktion*, speziell im maschinellen Lernen auch *Verlustfunktion*)
- den Vektor $x\in\R^n$ die *(Optimierungs-)Variablen* (im Kontext des maschinellen Lernens oft auch *Parameter*, *Koeffizienten* oder *Gewichte*)
````
Wir nehmen in dieser Vorlesung an, dass $f$ *stetig differenzierbar* ist. Dies ist in der Praxis, gerade im Bereich des maschinellen Lernens, nicht immer erfüllt, soll uns aber hier nicht weiter stören. Weiterhin möchten wir annehmen, dass es bei der Wahl des Vektors $\v x$ keine Einschränkungen gibt, d.h. der Bereich $D$, in dem wir nach einer Lösung suchen, soll der gesamte $\R^n$ sein.  

````{note} Minimierung vs. Maximierung
Per Konvention schauen wir uns nur Minimierungsprobleme an, d.h. eine Funktion soll so *klein* wie möglich sein. Haben wir es doch einmal mit einem Maximierungsproblem zu tun, also $\max_{\v x\in D\in\R^n} f(\v x)$, so können wir genausogut das Minimierungsproblem $\min_{\v x\in D\in\R^n} f(\v x)$ betrachten.
````

Wir haben nun schon von einer *Lösung* des Problems gesprochen, ohne präzise zu sagen, was das überhaupt sein soll. Man unterscheidet dabei zwischen lokalen und globalen Lösungen. Hier die Definitionen:
````{prf:definition} Globale und lokale Minima
:label: def:minmax

Ein Punkt $\v x^{\star}\in D$ heißt *globales Minimum* von $f$ oder *globale Lösung* des Minimierungsproblems, falls $f(\v x)\geq f(\v x^{\star})$ für *jeden* Vektor $\v x\in \R^n$.

Ein Punkt $\v x^{\star}\in D$ heißt *lokales  Minimum* von $f$ oder *lokale Lösung* des Minimierungsproblems, falls $f(\v x)\geq f(\v x^{\star})$ für *jeden* Vektor $\v x$ in einer Umgebung von $\v x^{\star}$. 

Wenn ein Minimierungsproblem keine globale Lösung besitzt, nennt man es *unbeschränkt*.
````
Wie groß diese "Umgebung" ist, ist nicht weiter spezifiziert. Die Aussage bedeutet lediglich, dass es eine solche gibt. Mathematisch exakter kann man das auch so formulieren:
Wir definieren für eine Zahl $\varepsilon>0$ die Menge $U_{\varepsilon}(\v x^{\star})$ als $\varepsilon$-Kugel um $\v x^{\star}$, formell $U_{\varepsilon}(\v x^{\star})=\{\v x\in\R^n :\ \norm{\v x^{\star}}-\v x\}<\varepsilon \}$. Ein Vektor $\v x^{\star}$ ist ein lokales Minimum, wenn es eine Zahl $\varepsilon>0$ gibt, so dass $f(\v x)\geq f(\v x^{\star})$ für *jeden* Vektor $\v x\in U_{\varepsilon}$

````{prf:example} Lokale und globale Minima
Die folgenden Beispiele zeigen, dass eine Funktion weder lokale noch globale Minima haben muss. Wenn es welche gibt, kann es auch sein, dass es mehrere gibt. 

Kein Minimum (unbeschränktes Problem)
: $f(x)=x$
```{figure} ./bilder/minima3.png
:width: 400px
```

Ein lokales Minimum, das gleichzeitig das globale Minimum ist
: $f(x)=x^2$
```{figure} ./bilder/minima5.png
:width: 400px
```

Ein lokales und ein globales Minimum
: $f(x)=\frac{1}{4}x^4-\frac{1}{3}x^3-x^2+2$
```{figure} ./bilder/minima4.png
:width: 400px
```

Unendliche viele globale (und lokale) Minima 
: $f(x)=\sin(x)$
```{figure} ./bilder/minima2.png
:width: 400px
```

Unendliche viele lokale Minima, kein globales Minimum (unbeschränktes Problem)
: $f(x)=\sin(x) + 0.3x$
```{figure} ./bilder/minima1.png
:width: 400px
```

Unendliche viele lokale Minima, ein globales Minimum
: $f(x)=\sin(x)+ 0.3|x|$
```{figure} ./bilder/minima6.png
:width: 400px
```

````

Nachdem wir nun die Grundbegriffe der Optimierung kennen, wenden wir uns als nächstes den Optimalitätsbedingungen und der Grundidee der Gradientenverfahren zu. Wir schauen uns alle Konzepte zunächst im univariaten, d.h. eindimensionalen Fall an, da dieser leichter zu verstehen ist. 
Danach wiederholen wir das Ganze für den allgemeinen multivariaten Fall (d.h. Vektoren statt Zahlen). Ich hoffe, dass man dadurch viele Parallelen zum (anschaulichen) eindimensionalen Fall erkennt und dass der mehrdimensionale Fall dadurch etwas eingängiger ist.


## Eindimensionale Optimierungsprobleme

### Optimalitätsbedingungen für univariate Funktionen
Wir starten mit einigen Beispielen, um die (hoffentlich bekannten) Prinzipien der Extremwertberechnung von eindimensionalen Funktionen wieder ins Gedächtnis zu rufen. Eine zentrale Rolle spielen dabei die *kritischen Punkte* einer Funktion.
````{prf:definition} Kritischer Punkt
Ein kritischer Punkt $x^*$ einer differenzierbaren Funktion $f:\R\rightarrow\R$ ist ein Wert $x\in\R$, so dass gilt $f'(x^*)=0$. 
````
Man sagt auch: an einem kritischen Punkt verschwindet die Ableitung.

Wir betrachten das Optimierungsproblem
\begin{align*}
\min_{x\in\R} f(x)=x^2-2x+3
\end{align*}
```{figure} ./bilder/parabel_min.png
:width: 400px
```
Das globale Minimum dieser Funktion ist $x=1$. Man findet es, indem man die Ableitung von $f$ berechnet und deren Nullstelle berechnet: $f'(x)=2x-2=0\Leftrightarrow x=1$. Da die Ableitung die Tangentensteigung an der Funktion angibt, bedeutet das: An der Stelle $x=1$ ist die Tangentensteigung $0$, also genau die Zahl, die die Grenze zwischen einer negativen und einer positiven Tangentensteigung ist.

Allerdings gilt das auch für die Ableitung der Funktion $g(x)=-f(x)=-x^2+2x-3$:
```{figure} ./bilder/parabel_max.png
:width: 400px
```
Offenbar ist die Nullstelle der Ableitung von $g$, $x=1$, eine *Maximum* der Funktion $g$.
%````
Als weiteres Beispiel betrachten wir die Funktion $h(x)=x^3$:
```{figure} ./bilder/sattelpunkt.png
:width: 400px
```
Es gilt: $h'(x)=3x^2=0$ für $x=0$. $x=0$ ist weder eine Maximum noch ein Minimum der Funktion $h$. Einen solchen Punkt nennt man *Sattelpunkt*[^fn:Sattelpunkt].
[^fn:Sattelpunkt]: Warum die Sattelpunkte heißen, wird im mehrdimensionalen Fall klar.

Damit haben wir drei einfache Beispiele gefunden, die die Arten kritischer Punkte einer Funktion repräsentieren. Ein kritischer Punkt einer differenzierbaren Funktion ist entweder ein
- Minimum,
- Maximum oder
- Sattelpunkt

Die Frage, um welche Art von kritischen Punkten es sich handelt wird oft durch die zweite Ableitung beantwortet. Diese quantfiziert die *Krümmung* einer Funktion (d.h. die Änderungsrate der Tangentensteigung). Für die Beispiele $f$ und $g$:
- $f''(x)=2 > 0$, d.h. die Krümmung ist überall (damit auch im kritischen Punkt $x=1$) *positiv*. Bei $x=1$ liegt ein Minimum vor.
- $g''(x)=-2 < 0$, d.h. die Krümmung ist überall (damit auch im kritischen Punkt $x=1$) *negativ*. Bei $x=1$ liegt ein Maximum vor.
- Leider kann man aus $h''(x)=0$ nicht folgern, dass ein Sattelpunkt vorliegt. Die zu untersuchenden Bedingungen sind etwas kleinteiliger, und wir kümmern uns hier nicht weiter darum. 

Wir haben nun an einem Beispiel veranschaulicht, was ganz allgemein für differenzierbare Funktionen gilt.
````{prf:theorem} Optimalitätsbedingungen für lokale Extrema, eindimensionaler Fall
:label: thm:OB1

Eine univariate Funktion $f:\R\rightarrow\R$ besitzt ein lokales Minimum (bzw. Maximum) bei $x=x_0$, wenn folgende Bedingungen erfüllt sind:
1. Notwendige Bedingung 1. Ordnung:
\begin{align*}
f'(x_0)=0
\end{align*}
2. Hinreichende Bedingung 2. Ordnung:
\begin{align*}
&f''(x_0)>0\quad \text{(Minimum) bzw.}\\
&f''(x_0)<0\quad \text{(Maximum)}
\end{align*}
````
Falls $f'(x_0)=0$ und $f''(x_0)=0$, so muss die Art des kritischen Punktes auf anderem Wege identifiziert werden. Es kommen dabei alle Arten von kritischen Punkten in Frage. Bei folgenden Beispielen sind an der Stelle $x=0$ die erste und zweite Ableitung $0$, also $f_i'(0)=f_i''(0)=0$:
- $f_1(x)=x^3$ hat an der Stelle $x=0$ einen Sattelpunkt.
- $f_2(x)=x^4$ hat an der Stelle $x=0$ ein Minimum.
- $f_3(x)=-x^4$ hat an der Stelle $x=0$ ein Maximum.

````{prf:example} Bestimmung von Extremwerten
:label: ex:kurvendiskussion
Wir bestimmen die Minima und Maxima der Funktion
\begin{align*}
f(x)=\frac{1}{4}x^4-\frac{1}{3}x^3-x^2+2
\end{align*}
```{figure} ./bilder/local_global.png
:width: 400px
```
- Nullstelle der ersten Ableitung berechnen:  
\begin{align*}
f'(x)=x^3-x^2-2x=x(x+1)(x-2)=0
\end{align*} Aus der Faktordarstellung folgt: Die erste Ableitung hat Nullstellen bei $x=-1$, $x=0$ und $x=2$. Dies sind alle kritischen Punkte der Funktion.

- Vorzeichen der zweiten Ableitung an den kritischen Punkten prüfen:
\begin{align*}
f''(x)=3x^2-2x-2\\
f''(-1)>0,\quad f''(0)<0,\quad f''(2)>0
\end{align*}Nach Satz {prf:ref}`thm:OB1` sind die Punkte $x=-1$ und $x=2$ Minima der Funktion und $x=0$ ein Maximum.

- Funktionswerte der Minima berechnen um globales Minimum zu bestimmen:
\begin{align*}
f(-1)=\frac{19}{12},\quad f(2)=-\frac{2}{3}
\end{align*}
Da der Funktionswert bei $x=2$ kleiner ist als bei $x=-1$ und die Funktion für $x<-1$ und $x>2$ gegen $\infty$ geht, ist das Minimum der Funktion $-\frac{2}{3}$. Es wird bei $x=2$ angenommen.
````

````{note}
Die Optimalitätsbedingungen in {prf:ref}`thm:OB1` beziehen sich nur auf *lokale* Minima und Maxima. Es gibt leider keine derartigen Bedingungen die ausschließlich für *globale* Minima und Maxima beliebiger Funktionen gelten. Bei manchen Funktionen kann man die Frage nach global vs. lokal allerdings auf anderem Weg beantworten: Wenn die zweite Ableitung eine Funktion überall $>0$ ist (z.B. bei $f(x)=x^2$), so ist jedes lokale Minimum gleichzeitig ein globales Minimum. Man nennt die Funktion dann auch *konvex*. Diese praktische Eigenschaft diskutieren wir in {ref}`sec:konvex` für allgemeine mehrdimensionale Funktionen.
````

Die Optimalitätsbedingungen in 1D kann man sich grafisch gut veranschaulichen. Ihre Gültigkeit erscheint plausibel. Das reicht uns aber nicht. Wir möchten (bzw. ich möchte, dass sie) ein tieferes Verständnis erlangen, warum die Bedingungen gelten. Das erreichen wir mit der gefürchteten [Taylorreihe](https://xkcd.com/2605/).

### Taylor-Formel für univariate Funktionen
Viele differenzierbare Funktionen können mittels *Taylorpolynomen* approximiert werden. Die Approximation bezieht sich dabei immer auf einen bestimmten (aber beliebigen) Punkt $x_0$, den sog. *Entwicklungspunkt* 

````{prf:definition} Taylorpolynom
Für eine differenzierbare Funktion $f$, einen Punkt $x_0$ und eine Zahl $n$ definieren wir das *Taylorpolynom* $n$-ten Grades als
\begin{align*}
T_n(x)& = \sum_{i=0}^{n} \frac{f^{(i)}(x_0)}{i!}(x-x_0)^i\\
&=f(x_0)+f'(x_0)(x-x_0)+\frac{f''(x_0)}{2}(x-x_0)^2+\frac{f'''(x_0)}{6}(x-x_0)^3+\cdots+
\frac{f^{(n)}(x_0)}{n!}(x-x_0)^n
\end{align*}
$f^{(i)}$ bezeichnet hier die $i$-te Ableitung von $f$.
````
Unter bestimmten Umständen konvergiert diese Summe sogar in einer Umgebung des Entwicklungspunktes $x_0$ (d.h. $x$ sollte nicht zu weit weg von $x_0$ liegen), wenn man $n$ gegen unendlich laufen lässt. Wenn das der Fall ist, gilt sogar oft[^fn:Taylor]
\begin{align*}
f(x)=\sum_{i=0}^{n} \frac{f^{(i)}(x_0)}{i!}(x-x_0)^i
\end{align*}
Dies nennt man dann die *Taylorreihe* der Funktion $f$.

In dieser Vorlesung sind wir aber vor allem an den Taylorpolynomen interessiert, also den Polynomen, die entstehen, wenn man die Reihe nach dem $n$-ten Glied abbricht. Taylorpolynome werden in vielen Anwendungen verwendet, um Funktionen zu approximieren. Viele Algorithmen in der Optimierung lassen sich mit ihrer Hilfe herleiten und analysieren.

Wir schauen uns zunächst einige Beispiele für Taylorpolynome an.
````{prf:example} Polynom
Wir betrachten das Taylorpolynom $n$-ten Grades der Funktion $f(x)=x^2-2x+3$ um den Entwicklungspunkt $x_0=1$.
\begin{align*}
T_n(x) &= \sum_{i=0}^{n} \frac{f^{(i)}(1)}{i!}(x-1)^i\\
        &=f(1)+f'(1)(x-1)+\frac{f''(1)}{2}(x-1)^2+\frac{f'''(1)}{3}(x-1)^3+\cdots\\
        &=2+0(x-1)+(x-1)^2+0(x-1)^3+0\cdots\\
        &=x^2-2x+3
\end{align*}
Da $f$ eine quadratische Funktion ist, sind alle Ableitungen ab der 3. Ableitung 0.Das Taylorpolynom entwickelt um den Punkt $x_0=1$ ist einfach die Funktion selbst. 

Das gilt allgemein für Polynome $n$-ten Grades: Alle Terme der Ordnung $>n$ sind 0, das Taylorpolynom $n$-ten Grades ist gleich dem Polynom.
````

````{prf:example} Natürlicher Logarithmus
Wir betrachten das Taylorpolynom $n$-ten Grades der Funktion $f(x)=\ln(x)$ um den Entwicklungspunkt $x_0=1$.
\begin{align*}
T_n(x)& &= \sum_{i=0}^{n} \frac{f^{(i)}(1)}{i!}(x-1)^i\\
        &=\ln(1)+\frac{1}{1}(x-1)-\frac{1}{2}(x-1)^2+\frac{2!}{3!}(x-1)^3-\frac{3!}{4!}(x-1)^4+\frac{4!}{5!}(x-1)^5\pm\cdots\\
        &=\sum_{i=0}^n \frac{-(x-1)^{i+1}}{i+1}
\end{align*}
Für $n\rightarrow \infty$ konvergiert diese Reihe im Bereich $0<x\leq2$. Wenn wir die Reihe nach endlich vielen Gliedern abbrechen, liefert sie eine Approximation des natürlichen Logarithmus im Bereich zwischen $0$ und $2$.
````
```{figure} ./bilder/taylor_ln.png
:width: 400px

Taylor-Polynome verschiedener Ordnung als Approximation des natürlichen Logarithmus im Intervall $(0,2]$. Quelle: https://commons.wikimedia.org/w/index.php?curid=11233446
```
Die Taylorpolynome sehen zunächst etwas umständlich aus und Sie fragen sich vielleicht, warum man statt eines schönen, kompakten Ausdruckes wie z.B. $\ln(x)$  so komplizierte Formeln benutzen sollte. Stellen Sie sich dazu folgendes vor: Jemand bittet Sie, den natürlichen Logarithmus an der Stelle $1.5$ ohne elektronische Hilfsmittel zu berechnen. Wie gehen Sie vor?

Antwort: mit Hilfe eines Taylorpolynoms! Zwar muss man sehr viele Schritte rechnen, aber jeder einzelne dieser Schritte ist elementar (Addition, Multiplikation, Division, Ableitungen bestimmen). Tatsächlich macht der Taschenrechner intern genau das: er wertet die ersten Summanden der Taylorreihe aus.

Die Approximationseigenschaft der Taylorpolynome fassen wir in folgendem Satz zusammen:
````{prf:theorem} Satz von Taylor
Sei $n\geq 1$ eine natürliche Zahl und sei die Funktion $f:\R\rightarrow\R$ $n$ Mal differenzierbar an einem Punkt $x_0$. Dann existiert eine Funktion $h_n:\R\rightarrow\R$, so dass
\begin{align*}
f(x)=f(x_0)+f'(x_0)(x-x_0)+\frac{f''(x_0)}{2}(x-x_0)^2+\cdots+
\frac{f^{(n)}(x_0)}{n!}(x-x_0)^n + h_n(x)(x-x_0)^n
\end{align*}
und
\begin{align*}
\lim_{x\rightarrow x_0} h_n(x)=0
\end{align*}
````
Zwei (etwas salopp formulierte) Einsichten aus diesem Satz:
1. Je näher der Auswertungspunkt $x$ am Entwicklungspunkt $x_0$ liegt, desto besser ist die Approximation, da $h_n(x)$ gegen $0$ geht, wenn $x$ gegen $x_0$ geht.
2. Die Beiträge höherer Ordnung werden immer (betrags-)kleiner, d.h. immer "unwichtiger". Dafür sorgt zum einen der Term $n!$ im Nenner. Zum anderen ist, wenn $x$ nahe bei $x_0$ ist, der Term $x-x_0$ sehr klein und damit wird der Term $(x-x_0)^n$ umso kleiner, je größer $n$ ist.

Zusammengefasst: eine Funktion ist "in der Nähe von $x_0$" ungefähr gleich ihrem Taylorpolynom: $f(x)\approx T_n(x)$. Im einfachsten Fall kann also mit Hilfe des Taylor-Polynoms erster Ordnung eine grobe Approximation von jeder differenzierbaren Funktion berechnet werden, also $f(x)\approx T_1(x)=f(x_0)+f'(x_0)(x-x_0)$. Die Approximation wird unzuverlässiger, je weiter $x$ von $x_0$ entfernt ist.

[^fn:Taylor]: Gegenbeispiel: : $f(x)=\begin{cases}
\exp⁡(−1/x^2),\quad &\text{falls } x\neq 0,\\ 0\quad &\text{falls } x=0\end{cases}$. Die Taylorreihe konvergiert auf keiner Umgebung von $x_0=0$ gegen die Funktion, siehe [hier](https://de.wikipedia.org/wiki/Taylorreihe#Eine_Funktion,_die_in_einer_Entwicklungsstelle_nicht_in_eine_Taylorreihe_entwickelt_werden_kann). 

### Kritische Punkte und Taylorentwicklung
Um zu verstehen, warum die hinreichende Bedingung an die zweite Ableitung gilt, betrachten wir die Taylorentwicklung um einen kritischen Punkt $x_0$. Wir schreiben das Argument $x$ als $x=x_0+d$, also als Abstand zum Entwicklungspunkt. Das ist eine übliche Schreibweise, wenn man mit Taylorpolynomen rechnet, denn dadurch kann man den Ausdruck $(x-x_0)$ durch $x-x_0=(x_0+d)-x_0=d$ ersetzen, wodurch die Formel etwas übersichtlicher wird.

Mittels Taylorapproximation ist also der Funktionswert in der Umgebung eines kritischen Punktes $x_0$:
\begin{align*}
f(x_0+d)\approx f(x_0)+\underbrace{f'(x_0)}_{=0}d+\frac{f''(x_0)}{2}d^2+\frac{f'''(x_0)}{6}d^3
\end{align*}
$d$ kann hier positiv oder negativ sein, aber $d^2$ ist immer positiv. Wenn nun $\frac{f''(x_0)}{2}>0$ (hinreichende Bedingung für ein Minimum aus {prf:ref}`thm:OB1`), so ist $f(x_0+d)>f(x_0)$, wenn $d$ klein genug ist, also der Auswertungspunkt $x$ nahe genug bei $x_0$ ist. Warum? Weil für kleine $d$ der nachfolgende Terme mit $d^3$ *noch* kleiner wird. Man kann immer erreichen, dass der Term \frac{f''(x_0)}{2}d^2 größer ist als der nachfolgende Term mit $d^3$. Das gilt erst recht, wenn man weitere Terme höherer Ordnung dazu nimmt, also $d^4$, $d^5$, usw. 

Die Aussage $f(x_0+d)>f(x_0)$ für alle Punkte in einer Umgebung von $x_0$ (also alle "ausreichend kleinen Werte" von $d$) bedeutet aber gerade, dass $f(x_0)$ ein lokales Minimum ist, nach {prf:ref}`def:minmax`. 

Diese Untersuchung mit Hilfe der Taylorentwicklung zeigt, warum die hinreichende Bedingung gültig ist. Für lokale Maxima gilt das analog, wenn man in der Argumentation $\frac{f''(x_0)}{2}>0$ durch $\frac{f''(x_0)}{2}<0$ ersetzt.

Wenn die zweite Ableitung weder positiv noch negativ ist, also $f''(x_0)=0$, so müssen Terme höherer Ordnung betrachtet werden, um herauszufinden, ob ein Minimum oder ein Maximum vorliegt. Ist $f'''(x_0)\neq 0$, so liegt ein Sattelpunkt vor, da das Vorzeichen von $\frac{f'''(x_0)}{6}d^3$ wechselt, je nachdem ob $d$ positiv oder negativ ist. Ist $f'''(x_0)=0$, so kann man mit Hilfe des Vorzeichens von $f''''(x_0)$ entscheiden ob ein Minimum ($f''''(x_0)>0$) oder Maximum ($f''''(x_0)<0$) vorliegt.


## Gradientenabstieg für univariate Funktionen
Kehren wir zurück zu unserer ursprünglichen Aufgabe: wir möchten das Minimierungsproblem
\begin{align*}
\min_{x\in\R} f(x)
\end{align*}
für eine beliebige differenzierbare Funktion $f$ lösen. Im Beispiel {prf:ref}`ex:kurvendiskussion` haben wir dafür per Hand *alle* Nullstellen bestimmt. Anschließend haben wir unter den lokalen Minima dasjenige mit dem kleinsten Funktionswert als globales Minimum ausgezeichnet (dafür mussten wir uns noch überlegen, dass die Funktion an ihren Grenzen immer größer wird, so dass sie nach unten beschränkt ist). 

Dieses Vorgehen ist leider nur in speziellen Fällen möglich. Im Allgemeinen lassen sich Nullstellen beliebiger Funktionen nicht analytisch bestimmen. Beispiel: Um die Kritischen Punkte von $f(x)=x^2\ln(x)-x$ zu bestimmen, müsste man 
\begin{align*}
f'(x)=2x\ln(x)+x-1=0
\end{align*}
nach $x$ auflösen. Dies ist nicht möglich (versuchen Sie's mal...). 

Es gibt iterative Verfahren, mit denen man die Gleichung approximativ lösen kann, z.B. das Newtonverfahren, das wir uns in {ref}`sec:newton` genauer anschauen. Allerdings besteht das Problem, dass man möglicherweise ein Maximum oder einen Sattelpunkt statt eines Minimums findet.

Wir bedienen uns stattdessen sogenannter *Abstiegsverfahren*: Man näher sich einem Minimum an, indem man eine Folge von Punkten konstruiert, bei denen man sicherstellt, dass der Funktionswert immer kleiner wird. Der prototypische Vertreter dieser Abstiegsverfahren ist der *Gradientenabstieg*, auch genannt Verfahren des steilsten Abstiegs/steepest descen oder gradient descent.
Wir schauen uns zunächst die Grundform dieses Algorithmus an, der uns dieses Semester an vielen Stellen begegnen wird. Zur Notation: hier und im Rest der Vorlesung indizieren wir die Iteration mit einem Superskript in eckigen Klammern: $^{[k]}$. Jede Größe (Skalar, Vektor, Matrix), an der Sie ein $^{[k]}$ sehen, kann sich von Iteration zu Iteration ändern. $x^{[k]}$ bezeichnet also den Wert $x$ während der Iteration $k$.

````{prf:algorithm} Gradientenabstieg für univariate Funktionen
Gegeben: 
: Differenzierbare Funktion $f:\R\rightarrow\R$.
: Folge von Schrittweiten $\alpha^{[k]}$, für $k=0,1,2,\dots$.

Gesucht: 
: Lokales Minimum von $f$.

**Algorithmus**:
1. Starte mit initialer Schätzung $x^{[0]}$, setze $k=0$.
2. Für $k=0,1,2,\dots$:
    - Berechne neue Iterierte $x^{[k+1]}=x^{[k]}-\alpha^{[k]}f'(x^{[k]})$.
    - Erhöhe $k$ um $1$.
    - Falls Abbruchbedingung erfüllt, beende Algorithmus mit Lösung $x^{[k]}$.
````
Hier ergeben sich sofort zwei Fragen:
1. Wie wählt man die Folge von Schrittweiten $\alpha^{[k]}$?
2. Was ist die Abbruchbedingung?

Bevor wir uns diesen widmen, schauen wir uns ein Beispiel für den Gradientenabstieg an, um zu verstehen, wie die Iteration funktioniert.

Ziel ist es, das Minimum der Funktion $f(x)=x^2\ln(x)+x-1$ zu bestimmen:
```{figure} ./bilder/gd_beispiel.png
:width: 400px
```
Das globale Minimum liegt bei $x^*=1$ mit dem Funktionswert $f(x)=-1$. Im Minimum hat die Ableitung $f'(x)=2x\ln(x)+x-1$ eine Nullstelle, d.h. $f'(1)=0$.

Der Einfachheit halber wählen wir die Schrittweite $\alpha^{[k]}$ konstant $\alpha^{[k]}=0.1$ in jeder Iteration $k$. Als Startwert für die Iterationen wählen wir $x^{[0]}=2$. Die Berechnung der Iterationen funktioniert wie folgt:

| $k$       | $x^{[k]}$ |
|:---       |:---       |
| $0$       | $2$       |
| $1$       | $2-0.1\cdot f'(2)=1.62$       |
| $2$       | $1.62-0.1\cdot f'(1.62)=1.40$       |
| $3$       | $1.40-0.1\cdot f'(1.40)=1.26$       |
| $\vdots$       | $\vdots$       |
| $15$       | $1.003$       |

In diesem Beispiel ist man nach $15$ Iterationen schon recht nah an der Lösung $x^*=1$. Auch klar: Wenn man einen anderen Startwert oder eine andere Schrittweite wählt, erhält man eine andere Folge von Iterationen. Hier ein Beispiel mit $\alpha^{[k]}=0.5$:

| $k$       | $x^{[k]}$ |
|:---       |:---       |
| $0$       | $2$       |
| $1$       | $2-0.5\cdot f'(2)=0.11$       |
| $2$       | $0.11-0.5\cdot f'(0.11)=0.8$       |
| $3$       | $0.8-0.1\cdot f'(0.8)=1.07$       |
| $\vdots$       | $\vdots$       |
| $9$       | $1.001$       |

Beobachtung: Wenn wir die Schrittweite vergrößern, machen wir schneller Fortschritte in Richtung der Lösung. Nach 9 Iterationen beträgt die Differenz zur (normalerweise unbekannten) optimalen Lösung nur noch $0.001$.

In folgendem Code ist ein einfaches Gradientenverfahren implementiert, das ein Minimum der Funktion $f(x)=x^2\ln(x)+x-1$ sucht. In jeder Iteration werden $x^{[k]},f(x^{[k]})$ und $f'(x^{[k]})$ ausgegeben. Des weiteren wird die Historie der $x^{[k]}$-Werte zurückgegeben und visualisiert.
 
```{code-cell} ipython3
import numpy as np
import seaborn as sns
sns.set_style("darkgrid")

def f(x):
    """ Function to minimize """
    return x**2*np.log(x)-x

def df(x):
    """ Derivative of the function to minimize """
    return 2*x*np.log(x)+x-1

def gd(func, derv, alpha, x0, n_steps):
    """ Perform n_steps iterations of gradient descent with steplength alpha and print iterates """
    print(" k     x           f(x)        f'(x)")
    print(f"{0:2} {x0:10.4f}, {func(x0):10.4f}, {derv(x0):10.4f}")
    x_history = [x0]
    x = x0
    for k in range(n_steps):
        dx = derv(x)
        x = x - alpha * dx
        print(f"{k+1:2} {x:10.4f}, {func(x):10.4f}, {dx:10.4f}")
        x_history.append(x)

    return x_history

x_history = gd(func=f, derv=df, alpha=0.1, x0=2.0, n_steps=15)

x = np.linspace(0.01,2,100)
sns.lineplot(x=x,y=f(x))
sns.lineplot(x=x_history, y=f(x_history), marker="o", sort=False)
```

### Abbruchbedingungen
Woher wissen wir, dass wir nahe genug an der Lösung sind und wir das Verfahren abbrechen können? Antwort: Man weiß es nie ganz sicher. Gängige Abbruchbedingungen sind:

1. Abbruch nach einer vorgegebenen Anzahl von Iterationen oder nach Ablauf einer vorgegebenen Zeit.
2. Die Ableitung der Zielfunktion $|f'(x^{[k+1]})|$ ist "klein", z.B. $<10^{-6}$.
3. Die Änderung der Iterierten $|x^{[k+1]}-x^{[k]}|$ ist "klein", z.B. $<10^{-6}$.
4. Die Änderung der Zielfunktion $|f(x^{[k+1]})-f(x^{[k]})|$ ist "klein", z.B. $<10^{-6}$.

Keine dieser Abbruchbedingungen ist ideal. Wir greifen diese Diskussion in {ref}`sec:gradientenverfahren` auf.
%:tags: [hide-input]


%Generell ist zu beachten, dass reelle Zahlen im Computer nur mit endlicher Genauigkeit dargestellt werden können. Ein Ausdruck ist also nie "genau gleich Null", sondern immer nur bis auf die unvermeidliche Maschinengenauigkeit, normalerweise $\varepsilon\approx 10^{-16}$.

### Divergenz des Gradientenabstiegs
In der Tat kann es schon bei einfachen Problemen vorkommen, dass der Gradientenabstieg *divergiert*. Wir betrachten die Funktion $f(x)=x^4-32x$
```{figure} ./bilder/gd_beispiel_divergenz.png
:width: 400px
```
Die erste Ableitung ist $f'(x)=4x^3-32$ und das globale Minimum wird bei $x=2$ angenommen. Wir wählen als Startwert $x^{[0]}=3$ und als Schrittweite wieder  $\alpha^{[k]}=0.1$. Die Iterationen des Gradientenabstiegs sind dann wie folgt (der Code ist der gleiche wie oben):
```{code-cell} ipython3
:tags: [hide-input]
import numpy as np
import seaborn as sns
sns.set_style("darkgrid")

def f(x):
    """ Function to minimize """
    return x**4-32*x

def df(x):
    """ Derivative of the function to minimize """
    return 4*x**3-32

def gd(func, derv, alpha, x0, n_steps):
    """ Perform n_steps iterations of gradient descent with steplength alpha and print iterates """
    print(" k     x           f(x)        f'(x)")
    print(f"{0:2} {x0:10.4f}, {func(x0):10.4f}, {derv(x0):10.4f}")
    x_history = [x0]
    x = x0
    for k in range(n_steps):
        dx = derv(x)
        x = x - alpha * dx
        print(f"{k+1:2} {x:10.4f}, {func(x):10.4f}, {dx:10.4f}")
        x_history.append(x)

    return x_history

x_history = gd(func=f, derv=df, alpha=0.1, x0=3.0, n_steps=15)

x = np.linspace(-2,4,100)
sns.lineplot(x=x,y=f(x))
sns.lineplot(x=x_history, y=f(x_history), marker="o", sort=False)
```

Was ist hier passiert? Die Iterierten $x^{[k]}$ entfernen sich rasend schnell von der Lösung, nach wenigen Iterationen ist der Funktionswert zu groß und kann nicht mehr angezeigt werden.

Dieses Verhalten nennt man *Divergenz*. Verantwortlich dafür normalerweise ein zu große Schrittweite. Wenn wir z.B. $\alpha^{[k]}=0.01$, konvergiert das Verfahren innerhalb weniger Iterationen zur Lösung $x=2$:
```{code-cell} ipython3
:tags: [hide-input]
import numpy as np
import seaborn as sns
sns.set_style("darkgrid")

def f(x):
    """ Function to minimize """
    return x**4-32*x

def df(x):
    """ Derivative of the function to minimize """
    return 4*x**3-32

def gd(func, derv, alpha, x0, n_steps):
    """ Perform n_steps iterations of gradient descent with steplength alpha and print iterates """
    print(" k     x           f(x)        f'(x)")
    print(f"{0:2} {x0:10.4f}, {func(x0):10.4f}, {derv(x0):10.4f}")
    x_history = [x0]
    x = x0
    for k in range(n_steps):
        dx = derv(x)
        x = x - alpha * dx
        print(f"{k+1:2} {x:10.4f}, {func(x):10.4f}, {dx:10.4f}")
        x_history.append(x)

    return x_history

x_history = gd(func=f, derv=df, alpha=0.01, x0=3.0, n_steps=15)

x = np.linspace(-2,4,100)
sns.lineplot(x=x,y=f(x))
sns.lineplot(x=x_history, y=f(x_history), marker="o", sort=False)
```

### Warum funktioniert der Gradientenabstieg?
Mittels der Approximation durch Taylorpolynome kann man verstehen, warum der Gradientenabstieg manchmal funktioniert und manchmal nicht. Dazu vergleichen wir die Funktionswerte $f(x^{[k]})$ und $f(x^{[k+1]})$. Wir würden erwarten, dass $f(x^{[k+1]})$ kleiner ist als $f(x^{[k]})$, dass also durch den Schritt ein Abstieg erzielt wird.

Die Iterationsvorschrift des Gradientenabstiegs lautet
\begin{align*}
f(x^{[k+1]}) = f(x^{[k]})-\alpha^{[k]}f'(x^{[k]})=x^{[k]}+d^{[k]}
\end{align*}
Wir bezeichnen mit $d^{[k]}=x^{[k+1]}-x^{[k]}$ ganz allgemein den Schritt in Iteration $k$.

Wir approximieren nun $f(x^{[k+1]})$ durch das Taylorpolynom erster Ordnung um den Entwicklungspunkt $x^{[k]}$:
\begin{align*}
f(x^{[k+1]})=f(x^{[k]}+d^{[k]})&\overset{\color{red}{(1)}}{\approx} f(x^{[k]})+d^{[k]}f'(x^{[k]}) \\
&=f(x^{[k]})-\alpha^{[k]}(f'(x^{[k]}))^2 < f(x^{[k]})
\end{align*}
Dieser Schluss gilt allerdings nur, wenn die Approximation $\color{red}{(1)}$ nicht zu ungenau ist (d.h. die Terme aus der Taylorreihe, die man weggelassen hat, fallen nicht zu sehr ins Gewicht). Man kann das theoretisch garantieren, indem man $\alpha^{[k]}$ klein genug wählt.
Das Dilemma, vor dem man bei der Wahl der Schrittweite steht ist folgendes:
- Wenn die Schrittweite $\alpha^{[k]}$ zu klein ist, ist der Fortschritt in Richtung Lösung gering. Der Gradientenabstieg braucht sehr viele Schritte.
- Wenn die Schrittweite $\alpha^{[k]}$ zu groß ist, ist kein Abstieg mehr garantiert, da die Approximation durch ein Taylorpolynom erster Ordnung (nichts anderes ist der Gradientenabstieg) zu ungenau ist. In der Folge kann das Verfahren divergieren.

### Zusammenfassung
Die numerische Lösung von eindimensionalen Optimierungsproblemen mittels  Gradientenabstieg zeigt bereits viele wichtige Merkmale, die uns auch beim Lösen von höherdimensionalen Optimierungsproblemen begegnen werden. Wir fassen diese kurz zusammen:
1. Lokale Minima von differenzierbaren Funktionen werden über die Optimalitätsbedingungen (siehe {prf:ref}`thm:OB1`) charakterisiert.
2. Die Optimalitätsbedingungen können (außer in besonderen Fällen) nicht analytisch aufgelöst werden, weshalb man iterative Verfahren, wie z.B. den Gradientenabstieg verwendet.
3. Für feste Schrittweite konvergiert der Gradientenabstieg im Allgmeinen nicht.
4. Falls der Gradientenabstieg konvergiert, dann zu einem lokalen Minimum. Zu welchem, hängt von Startwert und Schrittweite ab und lässt sich in der Regel nicht steuern.

Als nächstes werden wir uns alle behandelten Konzepte für multivariate Funktionen $f:\R^n\rightarrow \R$ anschauen. 


## Mehrdimensionale Optimierungsprobleme
Wir betrachten nun allgemeine, mehrdimensionale Optimierungsprobleme der Form
\begin{align*}
\min_{\v x\in D\in\R^n} f(\v x)
\end{align*}
mit einer differenzierbaren Funktion $f:\R^n\rightarrow \R$. Der erste Unterschied zum eindimensionalen Fall, der ins Auge fällt, ist, dass die ersten Ableitungen Vektoren sind, die zweiten Ableitungen (Hesse-)Matrizen. Man muss also genau aufpassen, welche Summen und Produkte überhaupt definiert sind. 

%Mit Blick auf das Gradientenverfahren gibt es außerdem nicht mehr nur zwei Richtungen ("links und rechts"), in denen man nach einem Abstieg der Funktion suchen kann, sondern unendlich viele: in der $\R^2$-Ebene kann man von einem Punkt aus 

````{note}
Es ist nicht sinnvoll Funktionen $\v f:\R^n\rightarrow\R^m$ (für $m>1$) zu optimieren, da nicht klar wäre, wie man ein Minimum im Bildraum $\R^m$ überhaupt definiert (wann ist ein Vektor größer oder kleiner als ein anderer Vektor?).
````


### Optimalitätsbedingungen für multivariate Funktionen
Wir betrachten nun eine Funktion $f:\R^n\rightarrow \R$ und möchten untersuchen, ob an der Stelle $\v x_0$ ein Extremwert vorliegt. Dazu untersuchen wir die Ableitung der Funktion in eine beliebige *Richtung* $\v a\in\R^n$. Wenn wir uns das z.B. im $\R^2$ vorstellen, wäre das eine Kurve, die auf der durch den Funktionsgraphen definierten, dreidimensionalen Fläche liegt. Eine Gerade die durch $\v x_0$ verläuft, läßt sich darstellen durch die Gleichung:
\begin{align*}
	\v x=\v x_0+t\v a,\quad t\in \R
\end{align*}
Die Punkte auf der Geraden kann man nun in die Funktionsgleichung von $f$ einsetzen und enthält dadurch die Kurve 
\begin{align*}
	g(t)=f(\v x_0+t\v a),
\end{align*}
also eine Funktion, die nur noch von einer Variablen $t\in\R$ abhängt (machen sie sich klar, dass es sich bei der Funktion $g$ um eine Funktion $g:\R\rightarrow\R$ handelt). Diese Konstruktion hatten wir uns schon bei der Definition der {ref}`sec:richtung` angeschaut.  

Die Überlegung ist nun folgende: wenn die Funktion $f$ an der Stelle $\v x_0$ ein Extremum hat, müssen auch alle Kurven die auf der durch $f$ definierten Fläche durch $\v x_0$ verlaufen, dort ein Extremum haben. Der Funktionswert von $g$ für $t=0$ ist gleich dem Funktionswert von $f$ bei $\v x_0$: $g(0)=f(\v x_0+0\cdot \v a)=f(\v x_0)$.

Wenn die Kurve $g$ bei $t=0$ ein Extremum hat, so muss ihre Ableitung hier gleich $0$ sein, d.h. $g'(0)=0$. Die Ableitung von $g(t)$ können wir wiederum mit Hilfe der Kettenregel bestimmen:
\begin{align}
	&g'(0) = \derv{f}{\v x}(\v x_0)\cdot \v a=\nabla f(\v x_0)\cdot \v a = \sum_{i=j}^{n}\derv{f}{x_j}(\v x_0)a_j.
\end{align}
Wir hatte die Richtung $\v a$ beliebig gewählt, d.h. dieser Ausdruck muss für *alle* $\v a$ gleich null sein. Das ist aber nur der Fall, wenn alle partiellen Ableitungen an der Stelle $\v x_0$ gleich null sind. Mit anderen Worten:



````{prf:theorem} Notwendige Bedingung für lokale Extrema, mehrdimensionaler Fall
An einem lokalen Minimum oder Maximum $\v x_0$ einer differenzierbaren Funktion $f:\R^n\rightarrow\R$ muss der Gradient verschwinden, d.h. es muss gelten:
\begin{align*}
    \nabla f (\v x_0) = \bmat  
        \derv{f}{x_1}(\v x_0) & \cdots & \derv{f}{x_n}(\v x_0)
    \emat   = \v 0
\end{align*}
````
Wenn wir uns erinnern, dass der Gradient in die Richtung des steilsten Anstiegs zeigt, bedeutet dieser Satz anschaulich: Am Gipfel ist man, wenn es nicht mehr weiter nach oben geht.

Wie im Fall einer Variablen schauen wir uns auch im Falle mehrerer Variablen die höheren Ableitungen an um zu entscheiden, ob es sich um ein Minimum oder ein Maximum handelt. Dafür betrachten wir wieder die Kurve $g$ und bilden die zweite Ableitung mit Hilfe der Kettenregel:
\begin{align}
	g''(t)&=\frac{\textup{d}}{\textup{d}t}\left(\derv{f}{\v x}(\v x_0+t\v a)\derv{(\v x_0+t\v a)}{t}\right)\\
	&=\frac{\textup{d}}{\textup{d}t}\left(\derv{f}{\v x}(\v x_0+t\v a)\cdot \v a\right)=\\
	&=\left(\dervquad{f}{\v x}(\v x_0+t\v a)\cdot \v a\right)^T\v a
\end{align}
Ausgewertet an der Stelle $t=0$ ergibt sich
\begin{align*}
	g''(0)=\v a^T\dervquad{f}{\v x}(\v x_0)\cdot \v a.
\end{align*}
Für ein Minimum muss nun der Ausdruck $a^T\dervquad{f}{\v x}(\v x_0)\cdot \v a>0$ sein und zwar für jeden beliebigen Vektor $\v a$. Diese Eigenschaft der Hessematrix hat auch einen speziellen Namen.

````{prf:definition} Definitheit von Matrizen
Eine quadratische Matrix $\v A\in\R^{n\times n}$ heißt 
- *positiv definit*, falls $\v x^T\v A\v x>0$,
- *positiv semidefinit*, falls $\v x^T\v A\v x\geq0$,
- *negativ definit*, falls $\v x^T\v A\v x<0$,
- *negativ semidefinit*, falls $\v x^T\v A\v x\leq0$,
für jeden Vektor $\v x\R^n$ mit $\v x\neq \v 0$.
````
Diese Eigenschaft von Matrizen nennt man \emph{positiv definit}. Analog liegt ein Maximum vor, falls $\v a^T\dervquad{f}{\v x}(\v x_0)\cdot \v a<0$ gilt und die Eigenschaft der Matrix  nennt man *negativ definit*. Definitheit von symmetrischen Matrizen kann man auch über ihre Eigenwerte definieren.
````{prf:theorem}
Sei $\v A$ eine symmetrische Matrix. $\v A$ ist genau dann positiv bzw. negativ definit, wenn alle Eigenwerte positiv bzw. negativ sind.
````

Insgesamt könenn wir die Optimalitätsbedingungen in folgendem Satz zusammenfassen:
````{prf:theorem} Optimalitätsbedingungen für lokale Extrema, mehrdimensionaler Fall
:label: thm:OBn
Sei $f:\R^n\rightarrow\R$ eine zweimal stetig differenzierbare Funktion. Dann gilt für einen Punkt $\v x_0\in\R$:
- Ist $\nabla f(\v x_0)=0$ und $\nabla^2 f(\v x_0)$ ist positiv definit, so hat $f$ bei $\v x_0$ ein lokales Minimum.
- Ist $\nabla f(\v x_0)=0$ und $\nabla^2 f(\v x_0)$ ist negativ definit, so hat $f$ bei $\v x_0$ ein lokales Maximum.
````

Zur Erinnerung: die notwendigen und hinreichenden Bedingungen für lokale Minima bzw. Maxima in *einer* Dimension sind (siehe {prf:ref}`thm:OB1`):
- Ist $f'(x_0)=0$ und $f''(x_0)>0$, so hat $f$ bei $x_0$ ein lokales Minimum.
- Ist $f'(x_0)=0$ und $f''(x_0)<0$, so hat $f$ bei $x_0$ ein lokales Maximum.

Man mache sich die Gemeinsamkeiten und Unterschiede zu den eben hergeleiteten Bedingungen in {prf:ref}`thm:OBn` klar. Knapp zusammengefasst:

| Eine Dimension  | Mehrere Dimensionen |
|:--- |:---
| erste Ableitung gleich $0$            | alle partiellen ersten Ableitungen gleich $0$ |
| zweite Ableitung positiv    | zweite Ableitung positiv definit    |

 
````{prf:example} Quadratische Funktion
:label: ex:quadratic
Wir betrachten die Funktion
\begin{align*}
f(x,y)=x^2+y^2+xy+3x-1
\end{align*}
Der Gradient ist
\begin{align*}
\nabla f(x,y)=\left(2x+y+3,\ 2y+x\right)
\end{align*}
Um einen kritischen Punkt zu berechnen, müssen das lineare Gleichungssystem $\nabla f(x,y)=\v 0$ lösen:
\begin{align*}
2x+y+3 &=0\\
 x+2y    &=0\\
\end{align*}
Auflösen ergibt $x=-2$, $y=1$.

Nun überprüfen wir die Definitheit der Hessematrix:
\begin{align*}
\nabla^2 f(x,y) = \bmat   2 & 1 \\ 1 & 2\emat  
\end{align*}
Die Eigenwerte sind $1$ und $3$. Damit ist die Hessematrix positiv definit und hat an der Stelle $(x,y)=(-2,1)$ ein Minimum. 
````
In {ref}`sec:multivariate_Funktionen` wurde erwähnt, dass sich jede quadratische Funktion schreiben läßt als
\begin{align*}
f(x_1,x_2,\dots,x_n)=\frac{1}{2}\v x^T\v A\v x+\v b^T\v x+c.
\end{align*}
Für das vorherige Beispiel wäre das:
\begin{align*}
f(x,y)=\frac{1}{2}(x,y) \bmat  2 & 1\\ 1 & 2\emat   \bmat  x\\y\emat  +(3,0) \bmat  x\\y\emat  +(-1),
\end{align*}
Der Vorteil dieser Darstellung ist, dass man aus ihr direkt den Gradienten und die Hessematrix ablesen kann. Der Gradient lautet
\begin{align*}
\nabla f(x_1,x_2,\dots,x_n) = \v A\v x + b
\end{align*}
im Beispiel also
\begin{align*}
\nabla f(x,y) = \bmat  2 & 1\\ 1 & 2\emat   \bmat  x\\y\emat  + \bmat  3\\0\emat   
\end{align*}
Die Hessematrix ist die Matrix $\v A$.

Betrachten wir ein weiteres (nicht-quadratisches) Beispiel
````{prf:example} 
Wir betrachten die Funktion
\begin{align*}
f(x,y)=x(y-1)+x^3
\end{align*}
Der Gradient ist
\begin{align*}
\nabla f(x,y)=\left(y-1+3x^2,\ x\right)
\end{align*}
Um einen kritischen Punkt zu berechnen, müssen das nichtlineare Gleichungssystem $\nabla f(x,y)=\v 0$ lösen:
\begin{align*}
y-1+3x^2 &=0\\
 x &=0\\
\end{align*}
Also ist $(0,1)^T$ kritischer Punkt.

Nun überprüfen wir die Definitheit der Hessematrix:
\begin{align*}
\nabla^2 f(x,y) = \bmat   6x & 1 \\ 1 & 0\emat  
\end{align*}
Diese müssen wir am kritischen Punkt $(0,1)^T$ auswerten:
\begin{align*}
\nabla^2 f(x,y) = \bmat   0 & 1 \\ 1 & 0\emat  
\end{align*}
Die Eigenwerte sind $1$ und $-1$. Damit ist die Hessematrix weder positiv definit noch negativ definit. Der kritische Punkt ist damit weder ein Minimum noch ein Maximum.
````
Zur Veranschauliching hier die Graph der Funktion mit dem kritischen Punkt:
```{code-cell} ipython3
:tags: [hide-input]
import plotly.graph_objects as go
import numpy as np

x = np.linspace(-2,2,100)
y = np.linspace(-2,4,100)
X,Y = np.meshgrid(x,y)
z = X*(Y-1) + X**3

fig = go.Figure(go.Surface(x=x,y=y,z=z, colorscale="Blues", showscale=False))
fig.update_layout( autosize=True, height=500,
                  margin=go.layout.Margin(l=0, r=0, b=0, t=0))

# Kritischer Punkt (x,y)=(0,1)
x = np.array([0])
y = np.array([1])
z = x*(y-1) + x**3
fig.add_trace(go.Scatter3d(x=x,y=y,z=z, mode="markers", line=dict(width=5)))
```
Den Fall, dass sowohl positive als auch negative Eigenwerte auftreten (die Matrix also *indefinit* ist), gibt es im univariaten Fall nicht (die "Hessematrix" ist dort ja nur eine $1\times 1$ "Matrix", hat also nur einen Eigenwert, nämlich den Wert selbst). Im Mehrdimensionalen Fall bedeutet eine indefinite Hessematrix, dass ein *Sattelpunkt* vorliegt---ein kritischer Punkt, der weder ein Minimum noch ein Maximum ist.

````{prf:remark} Sattelpunkt
Besitzt die Hessematrix einer differenzierbaren Funktion $f:\R^n\rightarrow \R$ an einem kritischen Punkt sowohl positive als auch negative Eigenwerte, so ist dieser Punkt ein *Sattelpunkt*.
````

Es lohnt sich (auch im Hinblick auf die Optimierungsverfahren, die wir uns in den nächsten Kapiteln anschauen), sich etwas mehr mit der Hessematrix zu beschäftigen. Die zweite Ableitung für eindimensionale Funktion beschreibt die *Krümmung* der Funktion. Tatsächlich tut die Hessematrix das auch---nämlich die Krümmung der Funktion in Richtung der Eigenvektoren!

Beispiel: Wir betrachten die Funktion $f(x,y)=x^2-y^2$. Die Hessematrix ist
\begin{align*}
\bmat   2&0\\0&-1\emat  
\end{align*}
Die Eigenwerte sind $+2$ und $-2$, die zugehörigen Eigenvektoren sind z.B. $\bmat  1\\0\emat  $ und $\bmat  0\\1\emat  $.
Der Graph der Funktion sieht wie folgt aus:

```{code-cell} ipython3
:tags: [hide-input]
import plotly.graph_objects as go
import numpy as np

x = np.linspace(-2,2,100)
y = np.linspace(-2,2,100)
X,Y = np.meshgrid(x,y)
z = X**2 - Y**2

fig = go.Figure(go.Surface(x=x,y=y,z=z, colorscale="Blues", showscale=False))
fig.update_layout( autosize=True, height=500,
                  margin=go.layout.Margin(l=0, r=0, b=0, t=0))

# Eigenvektor a=(1,0)
a1 = 1
a2 = 0
# Argument t der Kurve läuft von -2 bis 2
t = np.linspace(-2,2,100)
x = t*a1
y = t*a2
z = x**2 - y**2
# x,y,z enthält jetzt die Koordinaten der Kurve f(0+t*a). 
fig.add_trace(go.Scatter3d(x=x,y=y,z=z, mode="lines", line=dict(width=5), name="Richtung (1,0)"))

# Eigenvektor a=(0,1)
a1 = 0
a2 = 1
# Argument t der Kurve läuft von -2 bis 2
t = np.linspace(-2,2,100)
x = t*a1
y = t*a2
z = x**2 - y**2
# x,y,z enthält jetzt die Koordinaten der Kurve f(0+t*a). 
fig.add_trace(go.Scatter3d(x=x,y=y,z=z, mode="lines", line=dict(width=5), name="Richtung (0,1)"))
```
In rot und grün sind die Schnitte durch den Funktionsgraph entlang der Eigenvektoren dargestellt:
- Entlang des Eigenvektors $\bmat  1\\0\emat  $ ($x$-Achse) zum Eigenwert $+2$ hat die Funktion *positive* Krümmung.
- Entlang des Eigenvektors $\bmat  0\\1\emat  $ ($y$-Achse) zum Eigenwert $-2$ hat die Funktion *negative* Krümmung.
Die Hessematrix ist indefinit, und da der Graph der Funktion aussieht wie ein Reitsattel, nennt man einen solchen kritischen Punkt Sattelpunkt.


(sec:konvex)=
### Konvexität
Weiter oben haben wir den Begriff des lokalen Minimums eingeführt. Ein Nachteil des Gradientenabstiegs ist, dass er (wenn überhaupt) nur zu einem lokalen Minimum konvergiert. Wenn man Glück hat, ist dies auch das globale Minimum, aber dessen kann man sich in der Regel nicht sicher sein. 

Wie gravierend ist das Problem mit Nebenminima in höheren Dimensionen? Um uns der Frage zu nähern, betrachten wir noch einmal die Funktion aus {prf:ref}`ex:kurvendiskussion`:
\begin{align*}
f(x)=\frac{1}{4}x^4-\frac{1}{3}x^3-x^2+2
\end{align*}
```{figure} ./bilder/local_global.png
:width: 400px
```
Die kritischen Punkte sind $\{-1,0,2\}$, das sind die Nullstellen der ersten Ableitung $f'(x)=x^3-x^2-2x=x(x+1)(x-2)$.
Wir konstruieren nun eine zweidimensionale Funktion $F:\R^2\rightarrow \R$ als Summe von "Instanzen" von $f$:
\begin{align*}
F(x,y)=\frac{1}{4}(x^4+y^4)-\frac{1}{3}(x^3+y^3)-x^2-y^2+4
\end{align*}
```{code-cell} ipython3
:tags: [hide-input]

import plotly.graph_objects as go
import numpy as np

x = np.linspace(-1.5,2.5,100)
y = np.linspace(-1.5,2.5,100)
X,Y = np.meshgrid(x,y)
z = 1/4*(X**4 + Y**4) - 1/3*(X**3+Y**3) - X**2 - Y**2 + 4

fig = go.Figure(go.Surface(x=x,y=y,z=z, colorscale="Blues", showscale=False))
fig.update_layout( autosize=True, height=300,
                  margin=go.layout.Margin(l=0, r=0, b=0, t=0))
```
Die Funktion $F$ ist *separabel* bezüglich ihrer Variablen, d.h. $\derv{F}{x}$ hängt nicht von $y$ ab und $\derv{F}{y}$ hängt nicht von $x$ ab:
\begin{align*}
\nabla F(x,y)=(x^3-x^2-2x,\ y^3-y^2-2y)
\end{align*}
Man kann sich leicht überlegen, dass damit jede der neun möglichen Kombinationen aus $\{-1,0,2\}\times \{-1,0,2\}$ ein kritischer Punkt von $F$ ist. In diesem Fall sind es vier Minima, ein Maximum und vier Sattelpunkte.

Würde man nun nicht nur zwei Instanzen von $f$ addieren, sondern mehr, sagen wir $d$, würde man eine Funktion mit $3^d$ kritischen Punkten erhalten. Beispiel: Für $d=10$ hätte man eine Funktion $F:\R^{10}\rightarrow\R$, die 59049 kritische Punkte hat!

Die Anzahl der Nebenminima kann sehr schnell unerwartet groß werden. Im Allgemeinen sind die Anzahl und Struktur lokaler Minima schwer festzustellen. Es gibt allerdings Funktionen, die höchsten *einen* kritischen Punkt besitzen, der dann auch ein Minimum sein muss (man muss ihn allerdings noch finden), nämlich die strikt konvexen Funktionen.

````{prf:definition} Konvexe Menge
Eine Menge $D\subseteq \R^n$ heißt *konvex*, falls bei zwei Punkten aus $D$ stets auch deren gesamte Verbindungsstrecke zu $D$ gehört. In Formeln: 
\begin{align*}
\lambda \v x + (1-\lambda)\v y\in D\quad \forall \v x,\v y \in D \text{ und } \lambda\in (0,1)
\end{align*}
$\lambda$ ist eine reelle Zahl. Wenn $\lambda$ zwischen $0$ und $1$ variiert, werden die Punkte auf der Verbindungsstrecke durchlaufen.
````
Hier Beispiele für konvexe und nicht-konvexe Mengen:
```{figure} ./bilder/konvex.png
:width: 400px
```
Auch ist z.B. der gesamte Raum $\R^n$ eine konvexe Menge. Damit können wir den Begriff der konvexen Funktion definieren:
````{prf:definition} Konvexe Funktion
Sei $D\subseteq\R^n$ eine konvexe Menge. Eine Funktion heißt *konvex*, falls
\begin{align*}
f(\lambda \v x+(1-\lambda)\v y) \leq \lambda f(\v x)+(1-\lambda)f(\v y)\quad \forall \v x, \v y\in D \text{ und } \lambda\in (0,1)
\end{align*}
````
Anschaulich bedeutet diese Definition, dass eine Funktion konvex ist, wenn ihr Funktionsgraph zwischen zwei Punkte nie oberhalb der Verbindungsstrecke liegt.
````{note}
Konvexe Funktionen müssen nicht unbedingt differenzierbar sein.
````
Hier einige Beispiel konvexer und nicht-konvexer Funktionen:
```{figure} ./bilder/konvexe_funktionen.png
```
Was bringt uns das? Folgender Satz erklärt die wichtige Bedeutung des Begriffes der Konvexität in der mathematischen Optimierung.
````{prf:theorem}
:label: thm:konvex
Wenn eine Funktion *strikt konvex* ist, d.h. es gilt
\begin{align*}
f(\lambda \v x+(1-\lambda)\v y) {\color{red}<}\lambda f(\v x)+(1-\lambda)f(\v y)\quad \forall \v x, \v y\in D \text{ und } \lambda\in (0,1),
\end{align*}
so besitzt sie nur ein lokales Minimum, welches gleichzeitig das globale Minimum der Funktion ist.
````

Es besteht folgende Beziehung zwischen der Konvexität und der Hessematrix einer Funktion:
````{prf:theorem}
:label: thm:konvex2
Sei $D\subseteq \R^n$ konvex und $f:\R^n\rightarrow \R$ zweimal stetig differenzierbar. Dann gilt:
1. $f$ ist genau dann eine konvexe Funktion, wenn ihre Hessematrix auf ganz $D$ positiv semidefinit ist, also alle ihre Eigenwerte $\geq 0$ sind.
2. Wenn die Hessematrix sogar überall positiv definit ist, also alle ihre Eigenwerte $>0$ sind, so ist $f$ *strikt konvex*.
````
````{note}
Die Umkehrung der zweiten Aussage von {prf:ref}`thm:konvex` gilt nicht: So ist z.B. $f(x)=x^4$ zwar strikt konvex, aber ihre Hessematrix ist nur positiv semidefinit.
````
{prf:ref}`thm:konvex` und {prf:ref}`thm:konvex2` stellen also folgendes sicher: Wenn man von einer differenzierbaren Funktion nachweisen kann, dass ihre Hessematrix über positiv definit ist, so hat diese Funktion genau ein lokales (und gleichzeitig globales) Minimum.

Beispiele: 
1. Lineare Funktionen sind konvex (aber nicht strikt konvex). Sie besitzen kein Minimum sondern sind unbeschränkt.
2. Quadratische Funktionen: $f(\v x)=\frac{1}{2}\v x^T \v A\v x+\v b^T\v x+ c$ hat die Hessematrix $\v H(\v x)=\v A$. $f$ besitzt ein eindeutiges Minimum, wenn $A$ positiv definit ist. Wenn $A$ indefinit ist, ist die Funktion unbeschränkt auf $\R^n$.


### Taylor-Formel für multivariate Funktionen
Auch von der Taylorformel gibt es eine mehrdimensionale Version. Wir schauen uns das Taylor-Polynom zweiter Ordnung an. In der Nähe eines Punktes $\v x_0$ gilt für eine stetig partiell differenzierbare Funktion $f:\R^n\rightarrow \R$:
\begin{align*}
f(\v x)=f(\v x_0 + \v d)\approx \underbrace{f(\v x_0)}_{\text{Skalar}} + \underbrace{\nabla f(\v x_0)}_{\text{Vektor}}\v d + \frac{1}{2}\v d^T\underbrace{\nabla^2 f(\v x_0)}_{\text{Matrix}}\v d
\end{align*}
Zum Vergleich noch einmal das Taylorpolynom zweiter Ordnung für eine *univariate* Funktion $g:\R\rightarrow \R$:
\begin{align*}
g(x)=g(x_0 + d)\approx \underbrace{g(x_0)}_{\text{Skalar}} + \underbrace{g'(x_0)}_{\text{Skalar}}d + \frac{1}{2}\underbrace{g''(x_0)}_{\text{Skalar}}d
\end{align*}
Man sieht bei der mehrdimensionalen Taylorformel, wie die Ableitungen höherer Ordnung jeweils eine "Dimension" dazugewinnen (Skalar -> Vektor -> Matrix). Die Objekte mit drei und mehr Indizes (also ab der dritten Ableitung) nennt man *Tensoren*. Das Ganze kann man sich etwa so vorstellen:
```{figure} ./bilder/linear_dogs.jpg
[Quelle: Karl Stratos](https://karlstratos.com/#drawings)
```

Diese Tensoren bilden mehrere Vektoren (im Falle der Taylorformel sind das die $\v d$) auf einen Skalar ab. Für die erste und zweite Ableitung wird das durch die übliche Matrix-Vektor Multiplikation bewerkstelligt.
Ab der dritten Ableitung müsste man drei Vektoren $\v d$ geeignet an den Tensor "dranmultiplizieren" um ein Skalar als Funktionswert zu erhalten (man müsste natürlich noch definieren, wie das genau funktioniert). Wir bleiben hier bei Taylor-Polynomen zweiter Ordnung, in denen Gradient und Hessematrix vorkommen.

````{prf:example}
Wir approximieren die Funktion 
\begin{align*}
f:\R^2\rightarrow \R$\\
f(x,y)=\sin x + y^2
\end{align*}
im Punkt $(\pi,1)$ durch Taylor-Polynome erster und zweiter Ordnung.

Dazu berechnen wir zunächst den Gradienten und die Hessematrix:
\begin{align*}
    \nabla f(x,y) &= (\cos x, 2y)\\
    \nabla^2 f(x,y)&=\bmat  
        -\sin x & 0\\0 & 2
    \emat  
\end{align*}
Dann werten wir $f$, $\nabla f(x,y)$ und $\nabla^2 f(x,y)$ im Punkt $(\pi,1)$ aus:
\begin{align*}
    f(\pi,1) &= 1\\
    \nabla f(\pi,1) &= (-1, 2)\\
    \nabla^2 f(\pi,1)&=\bmat  
        0 & 0\\0 & 2
    \emat  
\end{align*}
Um das Taylor-Polynom erster Ordnung im Punkt $(\pi,1)$ zu berechnen, setzen wir zunächst:
\begin{align*}
    \bmat  
        x \\ y
    \emat  &=\bmat  
    \pi \\ 1
    \emat  +\bmat  
    d_1 \\ d_2
    \emat  
\end{align*}
Dieser Schritt ist nicht unbedingt nötig, sie können auch stattdessen auf der rechten Seite mit dem Vektor $\bmat  
        x \\ y
    \emat  -\bmat  
    \pi \\ 1
    \emat  $ rechnen, das ist dann von der Notation etwas länger. 
    
Damit können wir das Taylor-Polynom erster Ordnung wie folgt schreiben:
\begin{align*}
        T_1\left( \bmat  
            \pi \\ 1
        \emat  +\bmat  
        d_1 \\ d_2
    \emat   \right)&=f(\pi,1)+\nabla f(\pi,1)\bmat  
    d_1 \\ d_2
    \emat  \\&=1+(-1, 2)\bmat  
    d_1 \\ d_2
    \emat  =1-d_1+2d_2\\&=1-(x-\pi)+2(y-1)=2y-x+\pi-1
\end{align*}
Das Taylor-Polynom zweiter Ordnung im Punkt $(\pi,1)$ lautet:
\begin{align*}
    T_2\left( \bmat  
        \pi \\ 1
    \emat  +\bmat  
        d_1 \\ d_2
    \emat   \right)&=f(\pi,1)+\nabla f(\pi,1)\bmat  
        d_1 \\ d_2
    \emat  +\frac{1}{2}\bmat  
    d_1 & d_2
    \emat  \nabla^2 f(\pi,1)\bmat  
        d_1 \\ d_2
    \emat  \\&=1+(-1, 2)\bmat  
        d_1 \\ d_2
    \emat  +\frac{1}{2}\bmat  
    d_1 & d_2
    \emat  \bmat  
    0 & 0\\0 & 2
    \emat  \bmat  
    d_1 \\ d_2
    \emat  \\
    &=1-d_1+2d_2+d_2^2=2y-x+\pi-1+(y-1)^2=y^2-x+\pi
\end{align*}
````


%### Lineare Approximation und totale Differenzierbarkeit

Noch mehr als im eindimensionalen wirken die Taylor-Polynome auf den ersten Blick etwas "sperrig" und kompliziert. Ich möchte noch deshalb noch einmal explizit auf ihre Bedeutung und den Zusammenhang mit dem Begriff der Differenzierbarkeit eingehen. 

Schauen wir uns noch einmal ein allgemeines Taylor-Polynom erster Ordnung an:
\begin{align*}
f(\v x)=f(\v x_0 + \v d)\approx f(\v x_0) + \nabla f(\v x_0)\v d
\end{align*}

Die Approximationseigenschaft, also die Tatsache, dass das Taylorpolynom erster Ordnung eine bessere Approximation an die Funktion ist, je näher man das Polynom am Entwicklungspunkt betrachtet, ist ein Spezialfall des Satzes von Taylor für mehrdimensionale Funktionen:
````{prf:theorem} Satz von Taylor (Speziafall)
Es sei die Funktion $f:\R^n\rightarrow\R$ stetig partiell differenzierbar an einem Punkt $\v x_0$. Dann existiert eine Funktion $h:\R^n\rightarrow\R$, so dass
\begin{align*}
f(\v x)=f(\v x_0)+\nabla f(\v x_0)(\v x-\v x_0)+ h(\v x)(\v x-\v x_0)
\end{align*}
und
\begin{align*}
\lim_{\v x\rightarrow \v x_0} h(\v x)=0
\end{align*}
````
Was sagt dieser Satz nun eigentlich aus? Er sagt aus, dass jede differenzierbare Funktion $f$, so kompliziert sie auch sein mag, sich lokal so verhält wie eine lineare Funktion. Nehmen Sie z.B. an, dass $f$ eine Verlustfunktion für ein Modell im maschinellen Lernen ist, sagen wir ein tiefes neuronales Netz. Die Funktion gibt für einen Eingabevektor von Gewichten den Verlust (Fehler) auf einem gegebenem Datensatz  zurück. Diese Funktion ist immens kompliziert. Sie können Sie weder auf ein Blatt Papier aufschreiben (das wäre viel zu lang) noch können Sie sie sinnvoll visualisieren, d.h. Sie haben keine Ahnung wie sich diese Funktion verhält. Das einzige, was sie tun können, ist, die Funktion---und ihre Ableitung!---punktweise auszuwerten, d.h. für einen bestimmten Vektor von Eingabedaten bekommen Sie einen Funktionswert und den Gradientenvektor zurückgegeben. Der Satz von Taylor sagt: Das genügt, um in einer kleinen Umgebung eine beliebig gute Approximation an $f$ zu bekommen! Die Approximation lautet: 
\begin{align*}
f(\v x)\approx \underbrace{f(\v x_0)}_{\text{Zahl}} + \underbrace{\nabla f(\v x_0)}_{\text{Zeilenvektor}}\overbrace{(\v x - \v x_0)}^{\text{Spaltenvektor}}
\end{align*}

Das ist das Wesen der Differenzierbarkeit von mehrdimensionalen Funktionen. Wir hatten die partielle Differenzierbarkeit als Verallgemeinerung der eindimensionalen Ableitung eingeführt (partielle Differenzierbarkeit = eindimensionale Ableitung für jede der Variablen). Daneben gibt es noch einen etwas stärkeren Begriff, nämlich den der *totalen* Differenzierbarkeit. Deren (mathematisch etwas unsaubere) Definition geht so:

````{prf:definition} Totale Differenzierbarkeit
Eine Funktion $f:\R^n\rightarrow \R$ heißt in einem Punkt $x_0$ *total differenzierbar* (oder einfach nur *differenzierbar*), wenn sie in einer Umgebung des Punktes durch eine lineare Funktion approximiert werden kann.

\begin{align*}
f(\v x)=f(\v x_0)+\v g^T(\v x-\v x_0)+ h(\v x)(\v x-\v x_0)
\end{align*}
und
\begin{align*}
\lim_{\v x\rightarrow \v x_0} h(\v x)=0
\end{align*}

Den Vektor $\v g\in\R^n$ nennen wir die *Ableitung* von $f$ im Punkt $x_0$.
````

Man führt die Ableitung also nicht mehr über Differenzenquotienten ein, sondern *definiert* einfach "Differenzierbarkeit = linear approximierbar". 

Die totale Differenzierbarkeit behebt auch den "Schönheitsfehler" der partiellen Differenzierbarkeit, dass partiell differenzierbare Funktionen nicht immer stetig sind (siehe {prf:ref}`ex:partiell-unstetig`). Total differenzierbare Funktionen sind nämlich immer stetig. Es gilt:
\begin{align*}
\text{Stetig partiell differenzierbar} \Rightarrow \text{total differenzierbar} \Rightarrow \text{stetig}
\end{align*}

````{note}
Die Komponenten der totalen Ableitungen (wenn sie denn existieren) berechnet man ganz genauso wie die partiellen Ableitungen. Das ist kein fundamental anderer Differenzierbarkeitsbegriff, er ist nur ein wenig strikter und wird anders eingeführt.
````

(sec:gd-preview)=
## Preview: Gradientenabstieg für multivariate Funktionen
Wir haben nun alles beisammen, um den Gradientenabstieg analog zum eindimensionalen Fall beschreiben zu können. Wir müssen lediglich die Ableitung $f'$ durch ihre mehrdimensionale Verallgemeinerung, den Gradienten $\nabla f$, ersetzen, außerdem werden aus Zahlen $x$ Vektoren $\v x$.

Die Grundform des Verfahrens ist wie folgt:
````{prf:algorithm} Gradientenabstieg für multivariate Funktionen
:label: alg:gd
Gegeben: 
: Differenzierbare Funktion $f:\R^n\rightarrow\R$.
: Folge von Schrittweiten $\alpha^{[k]}$, für $k=0,1,2,\dots$.

Gesucht: 
: Lokales Minimum von $f$.

**Algorithmus**:
1. Starte mit initialer Schätzung $\v x^{[0]}$, setze $k=0$.
2. Für $k=0,1,2,\dots$:
    - Berechne neue Iterierte $\v x^{[k+1]}=x^{[k]}-\alpha^{[k]}\nabla f(\v x^{[k]})$, $\alpha^{[k]}>0$.
    - Erhöhe $k$ um $1$.
    - Falls Abbruchbedingung erfüllt, beende Algorithmus mit Lösung $\v x^{[k]}$.
````
Auch die Erklärung, warum das Verfahren funktioniert, kann man aus dem univariaten Fall übernehmen. Man begründet es mit der Taylorreihe. Dazu schauen wir uns eine lineare Approximation der Funktion an der aktuellen Iterierten $\v x^{[k]}$ an und argumentieren, dass der Funktionswert an der nächsten Iterierte $\v x^{[k+1]}$ kleiner sein muss, dass also ein Abstieg erzielt wird. Das Taylor-Polynom erster Ordnung, die sog. *Linearisierung* von $f$ zum Entwicklungspunkt $\v x^{[k]}$ ist
\begin{align*}
f(\v x^{[k+1]})=f(\v x^{[k]}+\v d^{[k]})&\approx f(\v x^{[k]})+\nabla f(\v x^{[k]})\v d^{[k]}\\
&=f(\v x^{[k]})-\alpha^{[k]}\nabla f(\v x^{[k]})\nabla f(\v x^{[k]})^T\\
&=f(\v x^{[k]})-\alpha^{[k]}\norm{\nabla f(\v x^{[k]})}^2
\end{align*}
Der Term $\alpha^{[k]}\norm{\nabla f(\v x^{[k]})}^2$ ist aber immer positiv, daher ist $f(\v x^{[k+1]})<f(\v x^{[k]})$. Man muss allerdings sicherstellen, dass $\alpha^{[k]}$ klein genug ist, so dass die Linearisierung gültig ist.

In den nächsten Kapiteln schauen wir uns Details und Modifikationen von Gradientenverfahren an. {prf:ref}`alg:gd` dient dabei als Grundlage. Wir werden einige Varianten dieses Algorithmus in der Vorlesung kennenlernen. 
