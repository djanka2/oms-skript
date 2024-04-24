(sec:zeitdiskret)=
# Zeitabhängige Probleme

Wir betrachten in diesem Kapitel Probleme, bei denen sich die Entscheidungsmöglichkeiten über einen gewissen Zeithorizont erstrecken. Wir betrachten folgendes Beispiel:

(subsec:energiespeicher)=
## Ein Energiespeicherproblem
Ein Unternehmen kann gut vorhersagen, wann es wieviel Strom benötigt. Das Unternehmen bezieht den Strom durch einen Versorger. Der Strompreis ändert sich über die Zeit, sei vorher aber bekannt. Zusätzlich hat das Unternehmen einen Batteriespeicher installiert. So kann das Unternehmen Strom in die Batterie einspeichern, wenn der Strompreis niedrig ist und den Strom wieder ausspeichern und selbst verbrauchen, wenn der Strom teuer ist. Das Unternehmen möchte den Batteriespeicher optimal nutzen.

```{figure} ./bilder/BeispielBatterie1.png
:name: fig:Batterie1
:width: 600px
```

Ein gängiges Vorgehen bei dieser Problemklasse ist die *Zeitdiskretisierung*: Die Zeit wird in gleichlange Zeitscheiben eingeteilt. Innerhalb einer Zeitscheibe werden alle Werte als konstant angenommen. Je kürzer die Zeitscheiben sind, desto genauer wird das Problem modelliert. Mit höherer Detailtreue steigt aber auch der Rechenaufwand um das Modell zu lösen.

Für die Modellierung wählen wir Zeitscheiben von einer Stunde Länge. Die Modellierungsgenauigkeit orientiert sich in diesem Fall am Strompreis. Dieser ändert sich jede Stunde und die zeitabhängige Abrechnung erfolgt in dieser Auflösung.

Wir nutzen unsere bewährte Vorgehensweise und modellieren nacheinander Problemdaten und Indexmengen, Entscheidungen, Zielfunktion und Nebenbedingungen.

### Problemdaten und Indexmengen
Es sind folgende Daten gegeben:
- Ein betrachteter Zeithorizont von einem Tag, gegeben als 24 einstündige Zeitperioden $H=\{1,2, \ldots, 24\}$.
- Der Verbrauch $d_t$ im Zeitintervall $t\in H$. 
- Der Strompreis $p_t$ im Zeitintervall $t\in H$.
- Die Kapazität $s_{max}$ des installierten Batteriespeichers.  
- Der initiale Füllstand $s_0$ des installierten Batteriespeichers.

### Entscheidungsvariablen
Wir nutzen folgende Entscheidungsvariablen
- Den Strombezug $k_t$ vom Netzbetreiber im Zeitintervall $t\in H$.
- Die Einspeicherung $s^+_t$ in den Batteriespeicher im Zeitintervall $t\in H$.
- Die Ausspeicherung $s^-_t$ aus dem Batteriespeicher im Zeitintervall $t\in H$.
- Den Speicherstand $s_t$ im Zeitintervall $t\in H$.

Die Variablen müssen für jedes Zeitintervall $t$ eingeführt werden. In diesem Beispiel sind das insgesamt $4\cdot24=96$ Variablen.

### Zielfunktion
Die Stromkosten sollen minimiert werden. Diese ergeben sich durch den aktuellen Preis multipliziert mit der Menge des gekauften Stroms zu jedem Zeitpunkt:

$$
\min_{s_t,s_t^-,s_t^+,k_t} \quad    \sum_{t=1}^{24}p_tk_t
$$

### Nebenbedingungen
Für jede Zeitperiode müssen neben den vier Variablen ($s_t,s_t^-,s_t^+,k_t$) zwei Gleichungen eingeführt werden. Es handelt sich um sog. *Bilanzgleichungen*, die die zeitliche Veränderung des Speicherstandes sowie die Deckung des Bedarfes zu jedem Zeitpunkt beschreiben. Die Modellierung kann wie folgt zusammengefasst werden:

```{figure} ./bilder/BeispielBatterie2.png
:name: fig:Batterie2
:width: 800px
```

Die Beispielinstanz hat also $2\cdot24=48$ Gleichungsnebenbedingungen.

Des Weiteren ist der Speicherstand $s_t$ durch die Obergrenze $s_{max}$ beschränkt und sowohl Speicherstand als auch eingekaufter Strom können nicht negativ sein. Insgesamt ergibt sich in kurzer Schreibweise:
\begin{alignat*}{5}
\min_{s_t,s_t^-,s_t^+,k_t} & \quad  &   \sum_{t=1}^{24}p_tk_t &          & & \\[4mm]
\text{s.t. } & & k_t - s_t^+ + s_t^-  & =  & \quad d_t & \quad\quad & & \forall t= 1, \ldots, 24 \\[2mm]
& & s_{t-1} + s_t^+ - s_t^-  & = & s_t & & & \forall t= 1, \ldots, 24 \\[3mm]
& & s_t & \leq & \quad s_{max} & && \forall t= 1, \ldots, 24. \\
& & s_t & \geq & \quad 0 & && \forall t= 1, \ldots, 24. \\
& & k_t & \geq & \quad 0 & && \forall t= 1, \ldots, 24.
\end{alignat*}

Das Ergebnis einer Beispielrechnung ist

```{figure} ./bilder/BeispielBatterie3.png
:name: fig:Batterie3
:width: 500px

Ergebnis zeitabhängiges lineares Optimierungsproblem.
```

## Ein Problem mit zeitlich gekoppelten Bedingungen
Um mit dem Konzept der zeitabhängigen Modellierung vertraut zu werden, betrachten wie ein weiteres Beispiel. Nehmen Sie an, Sie sind der Besitzer einer Eisdiele. Sie möchten festlegen, in welchem Zeitraum Sie nächstes Jahr geöffnet haben. Folgende Informationen sind relevant:
Sie planen in Tagen. Die Eisdiele kann prinzipiell an allen 365 Tagen im Jahr geöffnet sein.
Die Eisdiele eröffnet einmal im Jahr, ist dann durchgehend jeden Tag geöffnet, bis sie wieder
schließt. Die Eisdiele kann kein zweites Mal im gleichen Jahr eröffnen.
Für jeden Tag $t$, den die Eisdiele geöffnet hat, kennen Sie den erwarteten Gewinn $e_t$ durch
den Verkauf der Eiskugeln. Für jeden Tag, den die Eisdiele geöffnet hat, entstehen Personalkosten $k$ unabhängig von
der Wahl des Tages. Die Eisdiele hat jedes Jahr am 31.12. geschlossen.

Das Problem kann wie folgt zusammengefasst werden:

```{figure} ./bilder/eisdiele.png
:name: fig:eisdiele
:width: 600px
```

Gesucht ist ein ganzzahliges lineares Programm, das die Öffnungstage der Eisdiele finanziell optimal festlegt.

### Problemdaten und Indexmengen
Der Zeithorizont umfasst die Tage eines Jahres, also 

$$
H=\{1,2,\dots,365\}
$$

Gegeben sind die folgenden Daten:
- Erwarteter Gewinn $e_t, t\in H$
- Personalkosten $k$


### Entscheidungsvariablen
Wir nutzen die Entscheidungsvariablen

$$
    d_t=\left\{\begin{array}{rl}
        1 & \text{, Eisdiele ist an Tag }t\text{ geöffnet.} \\
        0 & \text{, Eisdiele ist an Tag }t\text{ geschlossen.}
        \end{array}\right.,\quad \forall t \in H
$$

Um später die Nebenbedingungen formulieren zu können, benötigen wir noch folgende Variablen

$$
    f_t=\left\{\begin{array}{rl}
        1 & \text{, Falls  } t\text{ der Eröffnungstag ist.} \\
        0 & \text{, sonst.}
        \end{array}\right.,\quad \forall t \in H
$$

Außerdem benutzen wir den festen Wert

$$
  d_0=0
$$

um die Situation an Silvester des Vorjahres zu beschreiben.

### Zielfunktion
Wir möchten den Gewinn maximieren. Der Gewinn für einen Tag $t$, an dem die Eisdiele geöffnet ist, ist gegeben durch $e_t-k$. Die Zielfunktion, die den Gesamtgewinn beschreibt, ist also gegeben durch

$$
  \max_{d_t,f_t} \quad    \sum_{t\in H}(e_t-k)d_t
$$

### Nebenbedingungen
Es muss sichergestellt werden, dass die Eisdiele nur einmal im Jahr öffnen bzw. schließen kann. Dies können wir logisch so formulieren:

"Wenn die Eisdiele an Tag $t-1$ geschlossen ist (also $d_{t-1}=0$), muss sie am Tag $t$ auch geschlossen sein $d_t=0$ oder sie muss eröffnen $f_t=1$."

Übersetzt in Formeln (siehe {ref}`subsec:logikVariablen`):

$$
  1-d_{t-1}\leq 1-d_t + f_t 
$$
bzw.

$$
  d_{t}\leq d_{t-1} + f_t 
$$

Weiterhin darf die Eisdiele nur einmal im Jahr öffnen:

$$
  \sum_{t\in H}f_t=1
$$

und an Silvester muss sie geschlossen sein, also $d_{365}=0$.


## Unsicherheiten in Optimierungsmodellen
Zeitabhängige Optimierungsprobleme sind ein guter Anlass, um ein allgemeines Problem von Optimierungsmodellen zu diskutieren. Nehmen wir noch einmal das Beispiel {ref}`subsec:energiespeicher`. In dem Beispiel gehen wir (bzw. der Löser) davon aus, dass wir den Strombedarf $d_1,d_2,\dots,d_{24}$ und den Strompreis $p_1,p_2,\dots,p_{24}$ für die nächsten 24 Stunden *genau* kennen und berechnen auf Basis dieser Annahme die optimale Lösung. Natürlich ist die Annahme, den Strompreis, den Strombedarf, das Wetter, den Aktienkurs oder die Lottozahlen von nächster Woche im Voraus *genau* zu kennen, falsch. Der Löser sieht aber die Unsicherheit in den Annahmen nicht; für ihn sind die Problemdaten lediglich feste Zahlen (man spricht auch von *deterministischer* Optimierung). Obwohl diese Beobachtung beinahe trivial ist, halten wir sie doch an prominenter Stelle fest:

````{important}
Die optimale Lösung eines *mathematischen Modells* ist nicht unbedingt die optimale Lösung des modellierten *realen Problems*. Das liegt daran, dass das Modell die Wirklichkeit nicht perfekt abbildet. Die Güte der Lösung hängt davon ab, wie groß und von welcher Art die Abweichungen von Modell und Wirklichkeit sind.
````

Typische Beispiele für deutliche Abweichungen von Modell und Wirklichkeit in Optimierungsmodellen:
- Zeitreihen, in denen Vorhersagen über die Zukunft gemacht werden, z.B. wie oben erwähnt Preise, Nachfragen, Wetter. 
- Vereinfachte mathematische Zusammenhänge. Z.B. geht beim Ein- und Ausspeichern in bzw. aus der Batterie elektrische Energie verloren (in Form von Wärme). Die Bilanzgleichung wird also nicht exakt stimmen. Wie viel Energie verloren geht, könnte auch wiederum von der Umgebungstemperatur, dem Alter der Batterie oder ihrem Füllstand abhängen.
- Bei Schedulingproblemen wird davon ausgegangen, dass man die Länge einer Aufgabe vorher kennt. Wie gut diese Annahme ist, hängt stark vom Anwendungsfall ab: Während die Annahme "Backzeit für Brot: 50 Minuten" bei der Produktionsplanung einer Großbäckerei wohl recht gut zutrifft, sind die Zeiten für bestimmte Arbeitsschritte z.B. im Bergbau sehr schwer abzuschätzen. Wie lange es dauert, eine gewisse Menge Fels abzutragen, hängt extrem von der Beschaffenheit des Felses, der Zuverlässigkeit der Maschinen und der Fähigkeit der Arbeiter:innen ab.

Was also tun? Ist angesichts dieser Unzulänglichkeiten lineare Optimierung nicht komplett nutzlos? Nein. (Gemischt-ganzzahlige) lineare Programmierung ist ein seit Jahrzehnten in der Industrie etabliertes Werkzeug, um praktisch relevante Planungs- und Entscheidungsprobleme zu lösen. In vielen Fällen sind die Modellfehler klein genug, so dass sie ignoriert werden können oder so dass die berechnete optimale Lösung des Modells zwar nicht ganz die optimale Lösung des modellierten Problems ist, aber eben doch ziemlich dicht dran -- und in jedem Fall besser als die Lösung, die ein Mensch ganz ohne mathematische Modell hervorgebracht hätte.

Eine Methode mit Modellfehlern -- man sagt auch *Unsicherheiten* -- umzugehen ist, ein MILP nicht nur einmal zu lösen, sondern mehrmals, und zwar zu unterschiedlichen Zeitpunkten. Dabei werden stets die aktuellsten Problemdaten mit einbezogen. Einen systematischen Ansatz, der auf dieser Idee basiert, beschreiben wir im nächsten Abschnitt. Darüber hinaus gibt es auch viele unterschiedliche Ansätze, bei denen man versucht, Unsicherheiten zu quantifizieren und mit Hilfe stochastischer Modelle abzubilden. Diese werden in dieser Vorlesung nicht behandelt.


### Sequenzielle Optimierung auf rollierendem Zeitfenster
Speziell für den Fall von zeitabhängigen Problemen, die man als MILP formulieren kann, bietet sich folgender Ansatz an, der sich relativ einfach umsetzen lässt und im Wesentlichen ohne Stochastik auskommt. Um ihn zu illustrieren, benutzen wir das Energiespeicherproblem. Wir nehmen zunächst an, dass der Strombedarf im Voraus bekannt ist, aber dass für den Preis $p_t$ nur eine 24-Stunden-Vorhersage[^VorhersageML] vorhanden ist. Der Ansatz ist aber auch auf alle anderen zeitabhängigen Probleme und weitere Unsicherheiten anwendbar.

Als erstens nehmen wir eine Änderung an der Notation des betrachteten Zeitintervalls vor: Oben haben wir das Zeitintervall von 24 Stunden durch die Zeitpunkte $t=1,2,\dots,24$ beschrieben, d.h. zum Zeitpunkt der Berechnung befinden wir uns am Zeitpunkt $t=0$ (oder davor). Allgemeiner: wenn wir die Berechnung zu irgendeinem Zeitpunkt $t=\tau$ ausführen, wären die Zeitpunkte der 24-Stunden-Vorschauperiode $t=\tau+1, \tau+2,\dots,\tau+24$. Wir machen die (realistische) Annahme, dass wir zu jedem Zeitpunkt $\tau$ eine aktualisierte 24-Stunden-Vorhersage für den Strompreis erhalten. Das bedeutet insbesondere, dass es für einen Zeitpunkt im Laufe der Zeit unterschiedliche Vorhersagen gibt (nämlich insgesamt 24 Stück).


```{figure} ./bilder/price_forecasts.png
:name: fig:forecasts
:width: 600px

Preis-Forecasts die an unterschiedlichen Zeitpunkten $\tau$ gemacht wurden.
```


Wir müssen diese unterschiedlichen Vorhersagen unterscheiden. Dafür führen wir einen zweiten Zeitindex ein, der beschreibt, an welchem Zeitpunkt die Vorhersage gemacht wurde. Die Größe 

$$
  p_{\tau, \tau+t},\quad t=1,\dots,24
$$ 

bedeutet: der vorhergesagte Preis für den Zeitpunkt $\tau+t$ basierend auf der Vorhersage zum Zeitpunkt $\tau$. Der Buchstabe $\tau$ bezeichnet also die real ablaufende Zeit, in der neue Vorhersagen eintreffen und die Berechnungen gestartet werden, während $t$ weiterhin die vorausschauende, diskretisierte Zeit im MILP bezeichnet (wie zu Anfang des Kapitels eingeführt).

Die Strategie, die wir nun verfolgen, um das Energiespeicherproblem zu lösen, lässt sich wie folgt skizzieren: Wir befinden uns am Zeitpunkt $\tau=0$. Wir benutzen die aktuelle 24-Stunden-Preisvorhersage $p_{0,0+t}, t=1,\dots,24$, um damit das erste MILP zu generieren. Mit zweitem Zeitindex $\tau$ lautet es

\begin{alignat*}{5}
\min_{s_{0,t},s_{0,t}^-,s_{0,t}^+,k_{0,t}} & \quad  &   \sum_{t=1}^{24}p_{0,t}k_{0,t} &          & & \\[4mm]
\text{s.t. } & & k_{0,t} - s_{0,t}^+ + s_{0,t}^-  & =  & \quad d_{0,t} & \quad\quad & & \forall t= 1, \ldots, 24 \\[2mm]
& & s_{0,t-1} + s_{0,t}^+ - s_{0,t}^-  & = & s_{0,t} & & & \forall t= 1, \ldots, 24 \\[3mm]
& & s_{0,t} & \leq & \quad s_{max} & && \forall t= 1, \ldots, 24. \\
& & s_{0,t} & \geq & \quad 0 & && \forall t= 1, \ldots, 24. \\
& & k_{0,t} & \geq & \quad 0 & && \forall t= 1, \ldots, 24.
\end{alignat*}

 Wir lösen das MILP und bezeichnen die optimale Lösung mit
\begin{align*}
    s_{0,t}^{\star},s_{0,t}^{-\star},s_{0,t}^{+\star},k_{0,t}^{\star},\quad t=1,\dots,24 
\end{align*}
Bis hierher haben wir nur die Situation aus Abschnitt {ref}`subsec:energiespeicher` beschrieben, nur mit einem zusätzlichen Zeitindex.

Wenn wir das Problem in der Praxis lösen, würden wir nun damit beginnen, die Lösung umzusetzen, d.h. wir setzen die Entscheidung um, die durch die optimale Lösung des MILPs für den *ersten* Zeitschritt repräsentiert wird
\begin{align*}
s_{0,1}^{\star},s_{0,1}^{-\star},s_{0,1}^{+\star},k_{0,1}^{\star}
\end{align*}
Nun schreitet die Zeit voran, d.h. aus $\tau=0$ wird $\tau=1$. Von unserer Data Science Abteilung erhalten wir eine neue 24-Stunden-Preisvorhersage $p_{1,1+t}, t=1,\dots,24$. Nun stellen wir das zweite MILP auf mit der aktualisierten Vorhersage als Problemdaten und lösen es:

\begin{alignat*}{5}
\min_{s_{1,1+t},s_{1,1+t}^-,s_{1,1+t}^+,k_{1,1+t}} & \quad  &   \sum_{t=1}^{24}p_{1,1+t}k_{1,1+t} &          & & \\[4mm]
\text{s.t. } & & k_{1,1+t} - s_{1,1+t}^+ + s_{1,1+t}^-  & =  & \quad d_{1,1+t} & \quad\quad & & \forall t= 1, \ldots, 24 \\[2mm]
& & s_{1,t} + s_{1,1+t}^+ - s_{1,1+t}^-  & = & s_{1,1+t} & & & \forall t= 1, \ldots, 24 \\[3mm]
& & s_{1,1} & = & \quad s_{0,1}^{\star} & && \forall t= 1, \ldots, 24. \\
& & s_{1,1+t} & \leq & \quad s_{max} & && \forall t= 1, \ldots, 24. \\
& & s_{1,1+t} & \geq & \quad 0 & && \forall t= 1, \ldots, 24. \\
& & k_{1,1+t} & \geq & \quad 0 & && \forall t= 1, \ldots, 24.
\end{alignat*}

*Wichtig*: Alle Werte, die sich auf die Vergangenheit beziehen (also z.B. $s_{1,1}$), sind jetzt keine Optimierungsvariablen mehr (wir können ja die Vergangenheit nicht mehr ändern), sondern feste Werte. Insbesondere ist der initiale Lagerbestand für das neue MILP $s_{1,1} = s_{0,1}^{\star}$.

Aus der Lösung dieses MILP verwenden wir wieder nur den Teil, der sich auf die nächste Zeitperiode, in dem Fall $\tau=2$ bezieht, nämlich:
\begin{align*}
s_{1,2}^{\star},s_{1,2}^{-\star},s_{1,2}^{+\star},k_{1,2}^{\star}
\end{align*}
Nun schreitet die Zeit wieder voran, d.h. aus $\tau=1$ wird $\tau=2$, wir erhalten eine neue Vorhersage, stellen das dritte MILP auf, lösen es, implementieren den ersten Zeitschritt der Lösung und so weiter. Als Lösung erhalten des Optimierungsproblems nehmen wir von jedem gelösten MILP den ersten Zeitschritt:

$$
s_{0,1}^{\star},s_{0,1}^{-\star},s_{0,1}^{+\star},k_{0,1}^{\star},\\
s_{1,2}^{\star},s_{1,2}^{-\star},s_{1,2}^{+\star},k_{1,2}^{\star},\\
s_{2,3}^{\star},s_{2,3}^{-\star},s_{2,3}^{+\star},k_{2,3}^{\star},\\
\vdots\\
s_{23,24}^{\star},s_{23,24}^{-\star},s_{23,24}^{+\star},k_{23,24}^{\star}.
$$

Wir halten fest:
- Um das Energiespeicherproblem zu lösen, lösen wir eine Serie von 24 MILPs, die sich in den Problemdaten (nämlich der jeweils aktuellen 24-Stunden-Preisvorhersage) unterscheiden
- Von jeder Lösung nutzen wir nur den Teil, der sich auf die nächste Zeitperiode bezieht, also $s_{\tau,\tau+1}^{\star},s_{\tau,\tau+1}^{-\star},s_{\tau,\tau+1}^{+\star},k_{\tau,\tau+1}^{\star}$ für $\tau=1,\dots,24$. Der Rest der Lösung wird nicht verwendet!
- Der Grundgedanke ist, dass so für eine Entscheidung immer die aktuellsten (und damit in der Regel besten) Vorhersagedaten verwendet werden.
- Ein solches Problem wird auch als *sequenzielles Entscheidungsproblem* bezeichnet, ein Problem der Form "Entscheidung, Information, Entscheidung, Information, ...". 

````{prf:algorithm} Sequenzielle Optimierung auf rollierendem Zeitfenster
:label: alg:mpc

Gegeben: 
: Zeitdiskretisiertes gemischt-ganzzahliges lineares Optimierungsproblem auf einem Zeithorizont $t=1,\dots,T$ mit Optimierungsvariablen $\v x_t$, Problemdaten $\v p_t$ und Zielfunktion
: \begin{align*}
  \sum_{t=1}^T \v c_t^T\v x_t,
  \end{align*}
: wobei die Vektoren $\v c_t$ Teil der Problemdaten $\v p_t$ sind für $t=1,\dots,T$.
: Folge von Vorhersagen bzw. Schätzungen für die Problemdaten, die zu den Zeitpunkten $\tau=0,1,\dots,T-1$ bekannt werden. Bezeichnung $\v p_{\tau,\tau+t}, t=1,\dots,T$

Gesucht: 
: Optimale Entscheidungen $\bar{\v x}^{\star}_{\tau}$ (die jeweils zum Zeitpunkt $\tau-1$ berechnet werden).

**Algorithmus**:
Für $\tau=0,1,\dots,T-1$: 
1. Wähle aktuelle Vorhersage als Problemdaten: 
    \begin{align*}
  \v p_t=\v p_{\tau,\tau+t},t=1,\dots,T.
  \end{align*}
1. Löse MILP mit Problemdaten $\v p_t$, erhalte Lösung 
    \begin{align*}
  \v x^{\star}_{\tau,\tau+t}:=\v x^{\star}_t,t=1,\dots,T.
  \end{align*}
1. Behalte ersten Zeitschritt der MILP Lösung: 
    \begin{align*}
    \bar{\v x}^{\star}_{\tau+1}=\v x^{\star}_{\tau,\tau+1}.
  \end{align*}

Die Vektoren $\bar{\v x}^{\star}_{\tau}, \tau=1,\dots,T$ enthalten die Lösung des Problems.
````
% Wenn Problem unzulässig: wie man es "zulässig" macht, muss aus Problem kommen (Energiespeicher: Ein/Ausspeichern ändern, mehr/weniger beziehen, demand nicht erfüllen. Oder Mischung aus allem). In jedem Fall: äußert sich in geändertent Startzuständen (nicht nur geänderten Problemdaten)

[^VorhersageML]: Die Vorhersagen werden ihrerseits auch mit einem mathematische Modell gemacht, z.B. einem Zeitreihenmodell oder einem Machine Learning Modell. Zeitabhängige Optimierungsprobleme sind schöne Beispiele für das Zusammenspiel zwischen Machine Learning und Optimierung. Das Machine Learning Modell liefert mit seinen Vorhersagen die Problemdaten für das Optimierungsmodell.

Dieser und ähnliche Ansätze sind in der industriellen Praxis weit verbreitet. Hier noch einige Anmerkungen dazu:
- Das in {prf:ref}`alg:mpc` beschriebene Schema ist in den Ingenieurswissenschaften als *modellprädiktive Regelung* (engl: model predictive control (MPC)) bekannt und wird dort vor allem zur Steuerung von technischen Prozessen verwendet.
- Der allgemeine Begriff für Verfahren, mit denen man sequenzielle Entscheidungsprobleme unter Unsicherheiten löst lautet *Policy*. {prf:ref}`alg:mpc` ist ein Beispiel für eine Policy.
- Da das Zeitfenster immer für eine feste Zeitperiode in die Zukunft geht, reicht es natürlich über den Zeithorizont $t=1,\dots,T$ im ursprünglichen Problem hinaus. Sollte das nicht funktionieren, da der Prozess z.B. eine feste Endzeit hat, so kann das Zeitfenster auch in jedem Schritt verkleinert werden (das letzte MILP besteht dann nur noch aus einem Zeitschritt).
- In vielen Anwendungen sind Vorhersagen für die nahe Zukunft sehr gut und werden schlechter, je weiter sie in der Zukunft liegen. Falls die Vorhersage auch für den ersten Zeitschritt $\tau+1$ falsch ist, kann es passieren, dass die vom Löser berechnete Lösung (physikalisch) unzulässig ist. Am Beispiel des Energiespeicherproblems wäre das der Fall, wenn die Vorhersage für den Strombedarf ungenau ist. Dann wäre die Bilanzgleichung $k_1^{\star} - s_1^{+\star} + s_1^{-\star}= d_1$ nicht erfüllt, was bedeutet, dass entweder der Bedarf nicht gedeckt würde (Stomausfälle) oder zu mehr als 100\% gedeckt wäre (zu viel Strom im Netz, was zu Schäden an der Infrastruktur führen kann). In der Realität müssten dann eine oder mehrere der Variablen $k_1^{\star}, s_1^{+\star}, s_1^{-\star}$ angepasst werden. 
- Die Lösung $\bar{\v x}^{\star}_{\tau}$ wird zwar auf Basis von optimalen Lösungen von MILPs konstruiert, sie ist aber selbst *keine* optimale Lösung des übergeordneten sequenziellen Entscheidungsproblems (eine sog. optimale Policy). In vielen Fällen ist diese "optimale Policy" aber eher theoretischer Natur, d.h. sie lässt sich nicht so ohne weiteres berechnen. 


### Evaluation der Lösung
Wir haben nun eine konkrete Vorgehensweise beschrieben, wie man mit Unsicherheiten in den Problemdaten umgehen kann, indem man eine Folge von MILPs löst. Wie gut ist dieses Vorgehen? Dies lässt sich nur a posteriori (also im Nachhinein) bewerten. Wir stellen dafür die Zielfunktion des MILP, die aus den tatsächlichen Problemdaten besteht (z.B. den Strompreisen).

Seien $\v p_{\tau}, \tau=1,\dots,T$ die tatsächlichen Problemdaten und $\v c_{\tau}, \tau=1,\dots,T$ der Teil der Problemdaten, der in der Zielfunktion verwendet wird. Dann bewerten wir unsere Lösung $\bar{\v x}^{\star}_{\tau}$ mit der Funktion
\begin{align*}
\sum_{\tau=1}^T \v c_{\tau}^T\bar{\v x}^{\star}_{\tau}
\end{align*}
Wichtig: Diese Funktion ist zum Zeitpunkt der Optimierung nie vollständig bekannt, weil man ja nicht in die Zukunft sehen kann. Aber wir können mit diesem Wert die Lösung $\bar{\v x}^{\star}_{\tau}$ mit verschiedenen Policies vergleichen, z.B.
1. ... mit dem theoretischen, aber nicht erreichbaren Optimum, das man a posteriori durch Lösen des MILPs mit Problemdaten $\v p_{\tau}, \tau=1,\dots,T$ erhält.
2. ... mit der Strategie, nur *ein* MILP zu Beginn des Zeithorizonts zu lösen. In der Notation von {prf:ref}`alg:mpc` wäre das
  \begin{align*}
  \sum_{\tau=1}^T \v c_{\tau}^T\v x^{\star}_{0,\tau}
  \end{align*}

Eine *optimale* Policy, also eine optimale tatsächlich (d.h. ohne genaue Kenntnis der Zukunft) durchführbare Strategie lässt sich für praktisch relevante Probleme normalerweise nicht bestimmen. In jedem Fall braucht man mehr Informationen über die statistische Güte der Vorhersagen $\v p_{\tau,\tau +t}$. Sind die Vorhersagen präzise und ändern sich von Zeitschritt zu Zeitschritt nur wenig, so wird man näher am theoretischen Optimum liegen als wenn die Vorhersagen sehr unsicher sind und sich über die Zeit stark ändern.  

%### Parametrisierung der Probleme 
% +Parametersuche / CFA

%## Anwendung: Stromnetzwerk
% TODO
% Projekt 2 SS23
% Übung: Energiespeicher Problem erweitern / modifizieren

%## Anwendung: Kraftwerkeinsatzplanung 
% TODO
%https://www.gurobi.com/jupyter_models/electrical-power-generation/
% oder aus Sudermann

%## Anwendung: Energiespeicherproblem (sequenzielle Optimierung) 
% TODO
% Beispielimplementierung

