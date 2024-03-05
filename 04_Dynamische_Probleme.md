(sec:zeitdiskret)=
# Zeitabhängige Probleme

Wir betrachten in diesem Kapitel Probleme, bei denen sich die Entscheidungsmöglichkeiten über einen gewissen Zeithorizont erstrecken. Wir betrachten folgendes Beispiel:

(subsec:energiespeicher)=
## Energiespeicher
Ein Unternehmen kann gut vorhersagen, wann es wieviel Strom benötigt. Das Unternehmen bezieht den Strom durch einen Versorger. Der Strompreis ändert sich über die Zeit, sei vorher aber bekannt. Zusätzlich hat das Unternehmen einen Batteriespeicher installiert. So kann das Unternehmen Strom in die Batterie einspeichern, wenn der Strompreis niedrig ist und den Strom wieder ausspeichern und selbst verbrauchen, wenn der Strom teuer ist. Das Unternehmen möchte den Batteriespeicher optimal nutzen.

```{figure} ./bilder/BeispielBatterie1.png
:name: fig:Batterie1
:width: 600px
```

Ein gängiges Vorgehen bei dieser Problemklasse ist die *Zeitdiskretisierung*: Die Zeit wird in gleichlange Zeitscheiben eingeteilt. Innerhalb einer Zeitscheibe werden alle Werte als konstant angenommen. Je kürzer die Zeitscheiben sind, desto genauer wird das Problem modelliert. Mit höherer Detailtreue steigt aber auch der Rechenaufwand um das Modell zu lösen.

Für die Modellierung wählen wir Zeitscheiben von einer Stunde Länge. Die Modellierungsgenauigkeit orientiert sich in diesem Fall am Strompreis. Dieser ändert sich jede Stunde und die zeitabhängige Abrechnung erfolgt in dieser Auflösung.

Es sind folgende Daten gegeben:
- Ein betrachteter Zeithorizont $\{1,2, \ldots, 24\}$ von einem Tag.
- Der Verbrauch $d_t$ zum Zeitpunkt $t$. 
- Der Strompreis $p_t$ zum Zeitpunkt $t$.
- Die Kapazität $s_{max}$ des installierten Batteriespeichers.  
- Der initiale Füllstand $s_0$ des installierten Batteriespeichers.
Wir nutzen folgende Entscheidungsvariablen
- Den Strombezug $k_t$ vom Netzbetreiber zum Zeitpunkt $t$.
- Die Einspeicherung $s^+_t$ in den Batteriespeicher zum Zeitpunkt $t$.
- Die Ausspeicherung $s^-_t$ aus dem Batteriespeicher zum Zeitpunkt $t$.
- Den Speicherstand $s_t$ zum Zeitpunkt $t$.
Dies führt zu folgender Modellierung:

```{figure} ./bilder/BeispielBatterie2.png
:name: fig:Batterie2
:width: 600px
```

In kurzer Schreibweise ergibt sich
\begin{alignat*}{5}
\min_{s_t,s_t^-,s_t^+,k_t} & \quad  &   \sum_{t=1}^{24}p_tk_t &          & & \\[4mm]
\text{s.t. } & & k_t - s_t^+ + s_t^-  & =  & \quad d_t & \quad\quad & & \forall t= 1, \ldots, 24 \\[2mm]
& & s_{t-1} + s_t^+ - s_t^-  & = & s_t & & & \forall t= 1, \ldots, 24 \\[3mm]
& & s_t & \leq & \quad s_{max} & && \forall t= 1, \ldots, 24. \\
& & s_t & \geq & \quad 0 & && \forall t= 1, \ldots, 24. \\
& & k_t & \geq & \quad 0 & && \forall t= 1, \ldots, 24.
\end{alignat*}
Wir halten fest: Für jeden Zeitschritt müssen vier Variablen ($s_t,s_t^-,s_t^+,k_t$) und zwei Gleichungen eingeführt werden (sog. *Bilanzgleichungen*). Die Beispielinstanz hat also $4\cdot24=96$ Variablen und $2\cdot24=48$ Gleichungsnebenbedingungen.

Das Ergebnis einer Beispielrechnung ist

```{figure} ./bilder/BeispielBatterie3.png
:name: fig:Batterie3
:width: 500px

Ergebnis zeitabhängiges lineares Optimierungsproblem.
```

%## Anwendung: Stromnetzwerk
% Projekt 2 SS23
% Übung: Energiespeicher Problem erweitern / modifizieren

## Anwendung: Produktionsplanungsproblem
% Projekt 2 SS22

## Anwendung: Kraftwerkeinsatzplanung
%https://www.gurobi.com/jupyter_models/electrical-power-generation/

% Übung: Reinhards Übungen?

## Unsicherheiten in Optimierungsmodellen
Zeitabhängige Optimierungsprobleme sind gute Beispiele dafür, ein allgemeines Problem von Optimierungsmodellen zu diskutieren. Nehmen wir noch einmal das Beispiel {ref}`subsec:energiespeicher`. In dem Beispiel gehen wir (bzw. der Löser) davon aus, dass wir den Strombedarf $d_1,d_2,\dots,d_{24}$ und den Strompreis $p_1,p_2,\dots,p_{24}$ für die nächsten 24 Stunden *genau* kennen und berechnen auf Basis dieser Annahme die optimale Lösung. Natürlich ist die Annahme, den Strompreis, den Strombedarf, das Wetter, den Aktienkurs oder die Lottozahlen von nächster Woche im Voraus *genau* zu kennen, falsch. Der Löser sieht aber die Unsicherheit in den Annahmen nicht; für ihn sind alles nur feste Zahlen (man spricht auch von *deterministischer* Optimierung). Obwohl diese Beobachtung beinahe trivial ist, halten wir sie doch an prominenter Stelle fest:

````{important}
Die optimale Lösung eines *mathematischen Modells* ist nicht unbedingt die optimale Lösung des modellierten realen Problems. Das liegt daran, dass das Modell die Wirklichkeit nicht perfekt abbildet. Die Güte der Lösung hängt davon ab, wie groß und von welcher Art die Abweichungen von Modell und Wirklichkeit sind.
````

Typische Beispiele für deutliche Abweichungen von Modell und Wirklichkeit in Optimierungsmodellen:
- Zeitreihen, in denen Vorhersagen über die Zukunft gemacht werden, z.B. wie oben erwähnt Preise, Nachfragen, Wetter. 
- Vereinfachte mathematische Zusammenhänge. Z.B. geht beim Ein- und Ausspeichern in bzw. aus der Batterie elektrische Energie verloren (in Form von Wärme). Die Bilanzgleichung wird also nicht exakt stimmen. Wie viel Energie verloren geht, könnte auch wiederum von der Umgebungstemperatur, dem Alter der Batterie oder ihrem Füllstand abhängen.
- Bei Schedulingproblemen wird davon ausgegangen, dass man die Länge einer Aufgabe vorher kennt. Wie gut diese Annahme ist, hängt stark vom Anwendungsfall ab: Während die Annahme "Backzeit für Brot: 50 Minuten" bei der Produktionsplanung einer Großbäckerei wohl recht gut zutrifft, sind die Zeiten für bestimmte Arbeitsschritte z.B. im Bergbau sehr schwer abzuschätzen. Wie lange es dauert, eine gewisse Menge Fels abzutragen, hängt extrem von der Beschaffenheit des Felses, der Zuverlässigkeit der Maschinen und der Fähigkeit der Arbeiter:innen ab.

Was also tun? Zunächst einmal: (Gemischt-ganzzahlige) lineare Programmierung ist ein seit Jahrzehnten in der Industrie etabliertes Werkzeug, um praktisch relevante Planungs- und Entscheidungsprobleme zu lösen. In vielen Fällen sind die Modellfehler klein genug, so dass sie ignoriert werden können oder so dass die berechnete optimale Lösung des Modells zwar nicht die optimale Lösung des modellierten Problems ist, aber eben doch ziemlich dicht dran -- und in jedem Fall besser als die Lösung, die ein Mensch ganz ohne mathematische Modell hervorgebracht hätte.

Sind die Modellfehler -- man sagt auch *Unsicherheiten* -- sehr groß, kommen darüber hinaus auch viele unterschiedliche Ansätze zum Einsatz, bei denen man versucht, Unsicherheiten zu quantifizieren und mit Hilfe stochastischer Modelle abzubilden. Diese werden in dieser Vorlesung nicht behandelt.

### Sequentielle Optimierung auf rollierendem Zeitfenster
Speziell für den Fall von zeitabhängigen Problemen, die man als MILP formulieren kann, bietet sich folgender Ansatz an, der sich relativ einfach umsetzen lässt und im Wesentlichen ohne Stochastik auskommt. Um ihn zu illustrieren, benutzen wir wieder das Energiespeicherproblem. Wir nehmen zunächst an, dass der Strombedarf im Voraus bekannt ist, aber dass für den Preis $p_t$ nur eine 24-Stunden-Vorhersage[^VorhersageML] vorhanden ist. Der Ansatz ist aber auch auf alle anderen zeitabhängigen Probleme und weitere Unsicherheiten anwendbar.

Als erstens nehmen wir eine Änderung an der Notation des betrachteten Zeitintervalls vor: Oben haben wir das Zeitintervall von 24 Stunden durch die Zeitpunkte $t=1,2,\dots,24$ beschrieben, d.h. zum Zeitpunkt der Berechnung befinden wir uns am Zeitpunkt $t=0$. Allgemeiner: wenn wir die Berechnung zu irgendeinem Zeitpunkt $t=\tau$ ausführen, wären die Zeitpunkte der 24-Stunden-Vorschauperiode $t=\tau+1, \tau+2,\dots,\tau+24$. Wir gehen davon aus, dass wir zu jedem Zeitpunkt $\tau$ eine aktualisierte 24-Stunden-Vorhersage für den Strompreis erhalten. Das bedeutet insbesondere, dass es für einen Zeitpunkt im Laufe der Zeit unterschiedliche Vorhersagen gibt (nämlich insgesamt 24 Stück).


BILD mit unterschiedlichen Forecasts mit unterschiedlichen Zeithorizonten


Um die verschiedenen Vorhersagen zu unterscheiden, führen wir einen zweiten Zeitindex ein. Die Größe $p_{\tau, \tau+t}$, wobei $t=1,\dots,24$ bedeutet: der vorhergesagte Preis für den Zeitpunkt $\tau+t$ basierend auf der Vorhersage zum Zeitpunkt $\tau$. Der Buchstabe $\tau$ bezeichnet also die real ablaufende Zeit, in der neue Vorhersagen eintreffen und die Berechnungen gestartet werden, während $t$ weiterhin die vorausschauende, diskretisierte Zeit im MILP bezeichnet (wie zu Anfang des Kapitels eingeführt).

Die Strategie, die wir nun verfolgen, um das Energiespeicherproblem zu lösen, lässt sich wie folgt beschreiben: Wir befinden uns am Zeitpunkt $\tau=0$. Wir benutzen die aktuelle 24-Stunden-Preisvorhersage $p_{0,0+t}, t=1,\dots,24$, um damit das erste MILP zu generieren und lösen es. Die optimale Lösung des MILPs bezeichnen wir mit
\begin{align*}
    s_{0,t}^{\star},s_{0,t}^{-\star},s_{0,t}^{+\star},k_{0,t}^{\star},\quad t=1,\dots,24 
\end{align*}
Wir beginnen nun damit, die Lösung umzusetzen, d.h. wir setzen die Entscheidung um, die durch die optimale Lösung des MILPs für den ersten Zeitschritt repräsentiert wird
\begin{align*}
s_{0,1}^{\star},s_{0,1}^{-\star},s_{0,1}^{+\star},k_{0,1}^{\star}
\end{align*}
Nun schreitet die Zeit voran, d.h. aus $\tau=0$ wird $\tau=1$. Wir erhalten nun eine neue 24-Stunden-Preisvorhersage $p_{1,1+t}, t=1,\dots,24$. Nun stellen wir das zweite MILP auf mit der aktualisierten Vorhersage als Problemdaten und lösen es. Aus der Lösung dieses MILP verwenden wir wieder nur den Teil, der sich auf die nächste Zeitperiode, in dem Fall $\tau=2$ bezieht, nämlich:
\begin{align*}
s_{1,2}^{\star},s_{1,2}^{-\star},s_{1,2}^{+\star},k_{1,2}^{\star}
\end{align*}
Nun schreitet die Zeit wieder voran, d.h. aus $\tau=1$ wird $\tau=2$, wir erhalten eine neue Vorhersage, stellen das dritte MILP auf, lösen es, implementieren den ersten Zeitschritt der Lösung und so weiter. 


BILD mit MPC Schema


Wir halten fest:
- Um das Energiespeicherproblem zu lösen, lösen wir eine Serie von 24 MILPs, die sich in den Problemdaten (nämlich der jeweils aktuellen 24-Stunden-Preisvorhersage) unterscheiden
- Von jeder Lösung nutzen wir nur den Teil, der sich auf die nächste Zeitperiode bezieht, also $s_{\tau,\tau+1}^{\star},s_{\tau,\tau+1}^{-\star},s_{\tau,\tau+1}^{+\star},k_{\tau,\tau+1}^{\star}$. Der Rest der Lösung wird nicht verwendet!
- Der Grundgedanke ist, dass so für eine Entscheidung immer die aktuellsten (und damit in der Regel besten) Vorhersagedaten verwendet werden.   

% Policy, sequentielles Entscheidungsproblem. Keine optimale Lösung!

````{prf:algorithm} Sequentielle Optimierung auf rollierendem Zeitfenster
:label: alg:mpc

Gegeben: 
: Zeitdiskretisiertes gemischt-ganzzahliges lineares Optimierungsproblem auf einem Zeithorizont $t=1,\dots,T$ mit Optimierungsvariablen $\v x_t$ und Problemdaten $\v p_t$  
: Folge von Vorhersagen für die Problemdaten, die zu den Zeitpunkten $\tau=0,1,\dots,T-1$ bekannt werden. Bezeichnung $\v p_{\tau,\tau+t}, t=1,\dots,T$

Gesucht: 
: Optimale Entscheidungen $\bar{\v x}^{\star}_{\tau}$ (die jeweils zum Zeitpunkt $\tau-1$ bekannt berechnet werden).

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
- Der allgemeine Begriff für Verfahren, mit denen man sequentielle Entscheidungsprobleme unter Unsicherheiten löst lautet *policy*. {prf:ref}`alg:mpc` ist ein Beispiel für eine policy.
- Da das Zeitfenster immer für eine feste Zeitperiode in die Zukunft geht, reicht es natürlich über den Zeithorizont $t=1,\dots,T$ im ursprünglichen Problem hinaus. Sollte das nicht funktionieren, da der Prozess z.B. eine feste Endzeit hat, so kann das Zeitfenster auch in jedem Schritt verkleinert werden (das letzte MILP besteht dann nur noch aus einem Zeitschritt).
- In vielen Anwendungen sind Vorhersagen für die nahe Zukunft sehr gut und werden schlechter, je weiter sie in der Zukunft liegen. Falls die Vorhersage auch für den ersten Zeitschritt $\tau+1$ falsch ist, kann es passieren, dass die vom Löser berechnete Lösung (physikalisch) unzulässig ist. Am Beispiel des Energiespeicherproblems wäre das der Fall, wenn die Vorhersage für den Strombedarf ungenau ist. Dann wäre die Bilanzgleichung $k_1^{\star} - s_1^+{\star} + s_1^-{\star}= d_1$ nicht erfüllt, was bedeutet, dass entweder der Bedarf nicht gedeckt würde (Stomausfälle) oder zu mehr als 100\% gedeckt wäre (zu viel Strom im Netz, was zu Schäden an der Infrastruktur führen kann). In der Realität müssten dann eine oder mehrere der Variablen $k_1^{\star}, s_1^{+\star}, s_1^{-\star}$ angepasst werden.
- Die Lösung $\bar{\v x}^{\star}_{\tau}$ wird zwar auf Basis von optimalen Lösungen von MILPs konstruiert, sie ist aber selbst *keine* optimale Lösung bzw. optimale policy.

### Evaluation der Lösung 
% Policy, sequentielles Entscheidungsproblem. Keine optimale Lösung!
% Was ist die eigentliche Zielfunktion?
% Wichtig: Lösung ist nicht mehr optimal

%### Parametrisierung der Probleme 
% +Parametersuche

### Anwendung: Energiespeicherproblem (sequentielle Optimierung) 
% Beispielimplementierung

