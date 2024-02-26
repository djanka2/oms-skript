# Einführung und Grundbegriffe

## Zur mathematischen Notation
Naturgemäß werden Sie in diesem Mathe-Skript mit vielen Symbolen konfrontiert. Um Ihnen den Weg durch diesen algebraischen Dschungel zu erleichtern (was ist Zahl, was ist Vektor, was ist Matrix?), wird in diesem Skript folgende Notation angewendet. 
- **Lateinische Kleinbuchstaben** wie $x$, $y$, $a$ usw. bezeichnen (meist reelle) Zahlen.
- **Fettgedruckte, lateinische Kleinbuchstaben** wie $\v x$, $\v y$, $\v a$ usw. bezeichnen Vektoren im $\R^n$. Deren Komponenten sind reelle Zahlen und werden mit einem Subscript indiziert (und sind nicht fettgedruckt, sind ja Zahlen):
  \begin{align*}
    \v x=\bmat x_1\\x_2\\\vdots\\x_n\emat
  \end{align*}
- **Fettgedruckte, lateinische Großbuchstaben** wie $\m A$, $\m X$, $\m H$ usw. bezeichnen $m\times n$-Matrizen. Deren Einträge (reelle Zahlen) sind die zugehörigen Kleinbuchstaben (nicht fettgedruckt) und werden mit zwei Subscripten indiziert:
  \begin{align*}
    \m A=\bmat a_{11} & a_{12} & \cdots & a_{1n}\\
                a_{21} & \cdots & \cdots & \\
                \vdots &  &      & \vdots\\
                a_{m1} & \cdots & \cdots & a_{mn}\emat
  \end{align*}
- **Griechische Kleinbuchstaben** wie $\alpha$, $\lambda$, $\mu$ usw. bezeichnen reelle Zahlen.
- Iterationszähler in iterativen Verfahren (Gradientenverfahren u.ä.) werden mit einem **Superscript in eckigen Klammern** indiziert: So bezeichnet $\v x^{[k]}$ den Vektor $\v x$ während der $k$-ten Iteration.

## Worum geht es?
Mathematische Optimierung beschreibt verschiedene Techniken und Algorithmen mit dem Ziel, etwas *bestmöglich* zu tun: Entweder für ein gegebenes Problem die *bestmöglichen* Entscheidungen treffen oder für ein System die *bestmöglichen* Parameter zu finden.

Es gibt unzählige Fragestellungen, die man mit Hilfe von mathematischer Optimierung beantworten kann. Hier einige Beispiele:
- Wann sollte eine Aktie am besten gekauft und verkauft werden, um größtmöglichen Gewinn zu erzielen?
- Wie soll in einer chemischen Anlage die Temperatur geregelt werden um mit möglichst wenig Energie möglichst viel Produkt zu erhalten?
- Wie sollten die Parameter eines Machine Learning Modells gewählt werden, so dass der Vorhersagefehler möglichst klein wird?
- Wie sollten Studierende unterschiedlichen Projekten zugeordnet werden, so dass die Präferenzen der Studierenden möglichst gut berücksichtigt werden?
- Welche Personen sollten auf eine Krankheit getestet werden, um die Ausbreitung der Krankheit möglichst gut vorhersagen zu können? Wie soll Impfstoff für eine Krankheit verteilt werden, um die Ausbreitung möglichst gut einzudämmen?
- Was ist die schnellste Route zwischen zwei Punkten in einem Straßennetz?

Um diese Probleme der Mathematik zugänglich zu machen, übersetzen wir sie zunächst in *mathematische Modelle*, d.h. Abstraktionen und Vereinfachungen der Realität. Ein gegebenes Problem aus der echten Welt in ein mathematisches Modell zu überführen ist im Allgemeinen nicht einfach. Dabei gibt es auch nicht *das* eine richtige Modell, denn:

> *All* models are wrong, but some are useful.
>
> George Box (1919-2013), britischer Statistiker 

Ein mathematisches Optimierungsmodell besteht aus folgenden Bestandteilen:

Problemdaten
: Informationen bzw. Rahmenbedingungen des Problems. Dies sind konkrete Zahlenwerte, die sich während der Berechnung der Lösung nicht ändern.

Entscheidungsvariablen
: Was sind die Entscheidungen oder Parameter, die optimal gewählt werden sollen? 

Zielfunktion
: Welche Größe soll minimiert oder maximiert werden?

Constraints
: Welchen Einschränkungen unterliegen unsere Entscheidungen?

Wir schauen uns nun ein Beispiel eines mathematischen Modells anhand einer konkreten Anwendung an.

(sec:production-example)=
### Beispiel: Ein Produktionsplanungsproblem

Eine Chemiefirma betreibt einen Reaktor, der in zwei verschiedenen Modi betrieben werden kann. Die Modi unterscheiden sich z. B. in der Reaktortemperatur oder dem Druck. Je nach gewähltem Modus produziert der Reaktor drei verschiedene Produkte mit folgenden Ausbeuten (in Tonnen pro Tag):

|           | Modus 1        | Modus 2      |
|---------- |-------------:  |-----------:  |
| Produkt A | 5 $t$/Tag      | 10 $t$/Tag   |
| Produkt B | 12 $t$/Tag     | 8 $t$/Tag    |
| Produkt C | 4 $t$/Tag      | 0 $t$/Tag    |

Wir nehmen an, dass sich, egal in welchem Modus produziert wird, ein Nettogewinn (=Verkaufserlöse – variable Kosten) von 2M€/Tag ergibt. Wenn der Reaktor nicht produziert, fallen keine Kosten an. 

Für jedes der Produkte existiert in einem Monat folgende Nachfrage in t: 
|           | Nachfrage/Monat |
|---------- |-------------:   |
| Produkt A | 50 $t$          |
| Produkt B | 72 $t$          |
| Produkt C | 20 $t$          |

Die Nachfrage muss nicht vollständig erfüllt werden, es ist aber auch nicht möglich, mehr als die angegebene Nachfrage zu verkaufen (oder Produkt einzulagern).

Das Planungsproblem lautet nun: an wie vielen Tage pro Monat muss die Firma in Modus 1 bzw. 2 produzieren um ihren Profit zu maximieren?

Wir identifizieren nun die vier Bestandteile Problemdaten, Entscheidungsvariablen, Zielfunktion und Constraints für unser Planungsproblem zu identfizieren.

Problemdaten
: Die Produktausbeuten, die Nachfrage pro Monat und der Profit pro Tag. 

Entscheidungsvariablen:
: - $x_1$: Anzahl Tage, an denen der Reaktor in Modus 1 produziert.
: - $x_2$: Anzahl Tage, an denen der Reaktor in Modus 2 produziert.

Zielfunktion:
: Der Profit soll maximiert werden. Der Profit beträgt 2M€ pro Tag, an denen der Reaktor produziert, also ist der Gesamtprofit $f(x_1,x_2)$ (in M€) gegeben durch $f(x_1,x_2)=2x_1+2x_2$.

Constraints:
: Da nichts eingelagert werden kann, darf die Produktionsmenge für ein Produkt nicht deren Bedarf überschreiten. Dies formulieren wir als Ungleichungen (eine Ungleichung für jedes Produkt):
: \begin{align*}
    5x_1+10x_2&\leq 50\\
    12x_2+8x_2&\leq 72\\
    4x_1+0x_2&\leq 20
  \end{align*}
: Weiterhin darf die Anzahl der Tage nicht negativ sein, sowie die Gesamtanzahl an Tagen, an denen produziert wird, darf nicht größer sein als die Anzahl der Tage im Monat (Vereinfachung: ein Monat hat 30 Tage).
: \begin{align*}
    x_1, x_2 &\geq 0\\
    x_1+x_2&\leq 30\\
  \end{align*}

Das ganze Problem schreiben wir kompakt als

```{math}
:label: eq:prodopt
\begin{alignat}{5}
\max_{x_1, x_2} & \quad  &   2x_1+2x_2 & & & \\[2mm]
\text{s.t. } & &  5x_1+10x_2&\leq 50\\
             & &  12x_1+8x_2&\leq 72\\
             & &  4x_1+0x_2&\leq 20\\
             & &  x_1+x_2&\leq 30\\
             & & x_1, x_2 &\geq 0
\end{alignat}
```
Das $s.t.$ steht für "subject to" also etwa "unter der Bedingung, dass". Eine optimale Lösung des Problems ist $x_1^{\star}=4, x_2^{\star}=3$. Für diese Werte sind alle Ungleichungen erfüllt und die Zielfunktion wird maximal. Der Profit beträgt dann $2\cdot 4 + 2\cdot 3=14$ M€.  

(sec:grundbegriffe)=
## Grundbegriffe der Optimierung
Im Beispiel {eq}`eq:prodopt` hatten wir es mit zwei Entscheidungsvariablen zu tun und einer konkreten Zielfunktion, bei der der Profit maximiert werden sollte. Im Allgemeinen können natürlich beliebig viele Entscheidungsvariablen vorliegen und eine beliebige Funktion dieser Variablen optimiert, d.h. maximiert oder minimiert werden.

Ein allgemeines mathematisches Optimierungsproblem notieren wir wie folgt:

````{prf:definition} Optimierungsproblem
Ein *Minimierungsproblem* ist ein Problem der Form
\begin{align*}
\min_{\v x} f(\v x)\quad \text{s.t. }\v x\in D\subseteq\R^n
\end{align*}
Dabei nennen wir
- den Vektor $\v x\in\R^n$ die *(Optimierungs-)Variablen* (im Kontext des maschinellen Lernens oft auch *Parameter*, *Koeffizienten* oder *Gewichte*)
- $f:\R^n\rightarrow \R$ die *Zielfunktion* (manchmal auch *Kostenfunktion*, speziell im maschinellen Lernen auch *Verlustfunktion*). $f$ ist ein mathematischer Ausdruck in den Optimierungsvariablen $x_1,\dots,x_n$.
- $D\subseteq \R^n$ die *zulässige Menge*.

Analog definiert man ein *Maximierungsproblem* als
\begin{align*}
\max_{\v x} f(\v x)\quad \text{s.t. }\v x\in D\subseteq\R^n
\end{align*}

Der Oberbegriff für Minimierungs- und Maximierungsproblem ist *Optimierungsproblem*.  
````

````{prf:remark} Minimierung oder Maximierung?
Per Konvention schauen wir uns, wenn wir von Optimierungsproblemen reden, nur Minimierungsprobleme an, d.h. eine Funktion soll so *klein* wie möglich sein. Haben wir es doch einmal mit einem Maximierungsproblem zu tun, also 
\begin{align*}
\max_{\v x} f(\v x)\quad \text{s.t. }\v x\in D\subseteq\R^n,
\end{align*} 
so könnten wir es stattdessen genausogut das Minimierungsproblem 
\begin{align*}
\min_{\v x} -f(\v x)\quad \text{s.t. }\v x\in D\subseteq\R^n
\end{align*}
betrachten.
````

Was genau ist die "zulässige Menge $D$"? Im Beispiel {eq}`eq:prodopt` wurde die Menge $D\subset\R^2$ durch verschiedene Ungleichungen repräsentiert. Jeden Punkt, der alle Ungleichungen erfüllt, bezeichnet man als *zulässigen Punkt*. Allgemeiner:

````{prf:definition} Zulässiger Punkt
Jeder Punkt (Vektor) $\v x\in D$ ist ein zulässiger Punkt des Optimierungsproblems
\begin{align*}
\min_{\v x} f(\v x)\quad \text{s.t. }\v x\in D\subseteq\R^n
\end{align*}
````
Bei manchen Problemen ist $D=\R^n$, d.h., jeder Vektor $\v x\in D$ ist zulässig. Diese Probleme nennt man *unrestringierte Probleme*, alle anderen *restringierte Probleme*. Sie unterscheiden sich vor allem in der Wahl der Lösungsverfahren. Eine weiterer Spezialfall liegt dann vor, wenn nur *ganzzahlige* Werte für manche oder alle Variablen zulässig sind. Mit diesen mächtigen (und algorithmisch besonders anspruchsvollen) Bedingungen beschäftigen wir uns im Kapitel {ref}`sec:integer-problems`.

Wir möchten nun noch die Lösungen von Optimierungsproblemen etwas genauer charakterisieren (ohne zu sagen, wie man die Lösungen eigentlich findet). Im Beispiel {eq}`eq:prodopt` hatten wir als Lösung des Optimierungsproblems die Werte $x_1=4, x_2=3$ und den zugehörigen maximalen Profit von $14$ M€ angegeben (ohne zu sagen, wie man darauf kommt). Allgemein benutzen wir folgende Begriffe:

````{prf:definition} Lösung eines Optimierungsproblems
:label: def:loesung

Ein Punkt $\v x^{\star}\in D$ heißt *Optimum*, *Optimalpunkt*, *Lösungspunkt* oder einfach *Lösung* des Minimierungsproblems $\min_{\v x} f(\v x)\quad \text{s.t. }\v x\in D\subseteq\R^n$, wenn $\v x$ zulässig ist und wenn es den kleinsten Zielfunktionswert aller zulässigen Punkte besitzt, also
\begin{align*}
f(\v x^{\star})\leq f(\v x) \text{ für *jeden* zulässigen Vektor $\v x\in D$.}
\end{align*}

Der zugehörige Zielfunktionswert $f(\v x^{\star})\in\R$ heißt *Optimalwert*.
````

Hat jedes Optimierungsproblem (genau) eine Lösung? Gibt es immer zulässige Punkte? Nein, wie man sich leicht anhand der folgenden Beispiele überzeugt:

````{prf:example} Verschiedene Arten von Lösungen

Unbeschränktes Problem
: Die Funktion $f(x)=x$ hat weder ein Minimum noch ein Maximum, da die Funktion beliebig klein oder groß wird.
: ```{figure} ./bilder/minima3.png
  :width: 400px
  ```
: Das Optimierungsproblem $\min_x x$ besitzt daher keine Lösung. Dies ist ein Beispiel für ein *unbeschränktes* Problem.

Unendlich viele Lösungen:
: Die konstante Funktion $f(x)=3$ hat unendlich viele Minima (und Maxima): 
: ```{figure} ./bilder/minima3.png
  :width: 400px
  ```
: Das Optimierungsproblem $\min_x 3$ hat somit unendlich viele Lösungen, die alle den Optimalwert $3$ haben. 

Unzulässiges Problem
: Das Problem
 \begin{alignat}{5}
 \min_{x} & \quad  &   x & & & \\[2mm]
 \text{s.t. } & &  x&\leq 0\\
              & &  x&\geq 1
 \end{alignat}
: besitzt *keinen* zulässigen Punkt und hat daher auch keine Lösung. Dies ist ein Beispiel für ein *unzulässiges* Problem.
````
