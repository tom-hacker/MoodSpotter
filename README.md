MoodSpotter




## Architecture

Insert Diagram here

Der grundlegende Aufbau von MoodSpotter lässt sich von obigem Diagramm ablesen.
Die Struktur lässt sich dabei am besten anhand der Benutzung von MoodSpotter erklären. Sie läuft wie folgt ab.

1. Die Kamera des Raspberry Pi nimmt ein Foto auf. Dieses Foto wird mittels REST an die *Microsoft Cloud API* geschickt und dort evaluiert. 

2. Aufgrund der Ergebnisse bestimmt der Raspberry Pi Zielmetriken für Lieder. Diese Metriken werden der Spotify API übergeben, welche zu ihnen passende Lieder ermittelt.

3. Die URIs der erhaltenen Lieder werden an RabbitMQ geschickt. Der MoodSpotterOnline-Microservice bekommt sie von RabbitMQ übermittelt und speichert sie zwischen. Abschließend ruft der Web-Client das nächste zu spielende Lied vom Microservice ab, und spielt es im Browser.


## Genutzte  APIs
### Microsoft Cognitive Service - Face API
#### Allgemeines
Die Face-API der Microsoft Cognitive Services dient zum erkennen von Gesichtern in Bildern. Neben allgemeneinen Informationen zum Gesicht, beispielsweise den Abständen zu Gesichtsmerkmalen, können auch kompliziertere Informationen ermittelt werden. Möglich sind beispielsweise das Geschlecht, ungefähre Alter, getragene Accessoires, von der Person getragenes Make-Up, bis zur Stimmung der Person.

#### Genutzte Funktionalität
Für MoodSpotter relevant sind insbesonders die ermittelten Informationen zur Stimmung der Person wichtig. Sie wird in sieben wichtige Stimmungen eingeteilt, zurückgegeben werden Prozentewerte, die insgesamt die Stimmung beschreiben.

Folgende Werte werden dabei ermittelt:
* anger
* contempt
* disgust
* fear
* happiness
* neutral
* sadness

//TODO: Links, example query and response

### Spotify API
#### Allgemeines
Spotify bietet viele verschiedene Endpoints zur Nutzung seiner Services, sowie zum Abfragen des von Spotify gebotenen Inhalts.
Mölich sind unter anderem Abfragen zu Liedern, Alben, Interpreten oder auch Nutzern. Auch das externe Steuern von mit Spotify verbundenen Geräten ist möglich. 
Die Authorisierung erfolgt mittels OAuth2, der manche Endpoints ist auch ohne Login möglich.

#### Genutzte Funktionalität
MoodSpotter nutzt die den Browse-Endpoint der API. Dieser ermittelt anhand von Seed-Liedern dazu passende Lieder. Zusätzlich können unterschiedliche Lied-Metriken angegeben werden, die die erwarteten Ergebnisse in eine Richtung leiten oder einschränken sollen.

* target_speed:
* target

Als Antwort liefert Spotify eine durch einen Parameter festgelegte Menge an Liedern (oder weniger, bei restriktiven Abfragen).
Die Informationen zu den Liedern enthalten unter anderem Name des Liedes, Name des Albums, Interpreten, einen Link zum Starten des Liedes. Für MoodSpotter ist besonders die übermittelte eindeutige URI wichtig, anhand ihrer kann jede andere Anwendung dieses Lied abfragen.


## Raspberry Pi
Das Kernstück von MoodSpotter ist der Raspberry Pi. Er nimmt die Bilder auf, spricht die APIs an und übernimmt das berechnen der Ziel-Liedmetriken.

### Setup
Als Betriebssystem wird Raspian verwendet. Das Kameramodul wird am dafür vorgesehenen Anschluss installiert. Anschließend musste das Kamera-Modul in den Einstellungen noch aktiviert werden. //TODO: WO??
Nachdem Moodspotter beim Starten des Raspberry Pis sofort starten soll, wurde der Pfad zum einstiegspunkt in der Datei */etc/rc.local* hinterlegt.
Dadurch wird das Programm im Boot-Prozess gestartet. 
Damit der Raspberry Pi mit den APIs und mit RabbitMQ kommunizieren kann, muss er außerdem in einem Netzwerk mit Internetzugriff sein. Um dies durchzuführen wurde er eingangs an einen Bildschirm, und an Tastatur und Maus angeschlossen.
 

###