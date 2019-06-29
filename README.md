# MoodSpotter
Projektarbeit zu Mobile und ubiquitäre Systeme (MUS)

Projekt-Team: Tom Hacker, Verena Teufl

## Projektbeschreibung
### Problembeschreibung
Es ist allgemein bekannt, dass Musik einen starken Einfluss auf das emotionale Befinden von Personen hat. Jedoch ist das Finden von zur Stimmung passender Musik nicht immer so einfach sowie oftmals aufwendig oder nicht möglich. Häufig wird auch einfach nur darauf „vergessen“, wie sehr die Musik die Stimmung beeinflussen kann, und deshalb kommt keine zur Stimmung passende oder gar keine Musik zum Einsatz. Obwohl meist an denselben Plätzen Musik gehört wird (Auto, Wohnzimmer, Arbeitsplatz, Lokale, etc.), gibt es keinen Weg die Musik mit wenig Aufwand an die Stimmung anzupassen. Gerade beim Autofahren wäre eine vollautomatische Stimmungserkennung und daraufhin die Anpassung der Musik von Nutzen. So könnten brenzliche Situationen im Straßenverkehr schon im Vorhinein vermieden werden. Indem bei Aufregung beruhigende und bei Müdigkeit aufputschende Musik gespielt wird.

### Lösungsansatz
Zur Lösung des oben genannten Problems wird MoodSpotter entwickelt. Auf einem Raspberry Pi mit zusätzlichem Kamera-Modul werden in regelmäßigen Abständen Bilder aufgenommen. Mithilfe der Microsoft Cognitive Services werden die Emotionen der auf dem Bild befindlichen Personen ermittelt. Aufgrund der erhaltenen Informationen werden über die Spotify-API Lieder herausgesucht, die den gewünschten Effekt erzielen könnten. Die Spotify-API bietet Informationen zur Geschwindigkeit, Lebhaftigkeit und auch zur Stimmung eines Lieds. Mithilfe dieser Informationen, und den durch die Microsoft Cognitive Services API werden Lieder ermittelt, die zur aktuellen Stimmung der Person(en) vor der Kamera passen. Die ermittelten Lieder werden über Message-Oriented-Middleware einer Webanwendung übermittelt, wodurch eine Art Queue simuliert wird. Die Webanwendung spielt diese Musik ab, und ermöglicht Nutzerfeedback in Form von Like beziehungsweise Dislike. 


## Architektur

<p align="center">
  <img src="images/Architecture.JPG" width="80%"/>
</p>


Der grundlegende Aufbau von MoodSpotter lässt sich von obigem Diagramm ablesen.
Die Struktur lässt sich dabei am besten anhand der Benutzung von MoodSpotter erklären. Sie läuft wie folgt ab.

1. Die Kamera des Raspberry Pi nimmt ein Foto auf. Dieses Foto wird mittels REST an die *Microsoft Cloud API* geschickt und dort evaluiert. 

2. Aufgrund der Ergebnisse bestimmt der Raspberry Pi Zielmetriken für Lieder. Diese Metriken werden der Spotify API übergeben, welche zu ihnen passende Lieder ermittelt.

3. Die URIs der erhaltenen Lieder werden an RabbitMQ geschickt. Der MoodSpotterOnline-Microservice bekommt sie von RabbitMQ übermittelt und speichert sie zwischen. Abschließend ruft der Web-Client das nächste zu spielende Lied vom Microservice ab, und spielt es im Browser.

## Technische Umsetzung

### Raspberry Pi
Das Kernstück von MoodSpotter ist der Raspberry Pi. Er nimmt die Bilder auf, spricht die APIs an und übernimmt das berechnen der Ziel-Liedmetriken.

#### Setup
Als Betriebssystem wird Raspian verwendet. Das Kameramodul wird am dafür vorgesehenen Anschluss installiert. Anschließend musste das Kamera-Modul in den Einstellungen noch aktiviert werden. //TODO: WO??
Nachdem Moodspotter beim Starten des Raspberry Pis sofort starten soll, wurde der Pfad zum einstiegspunkt in der Datei */etc/rc.local* hinterlegt.
Dadurch wird das Programm im Boot-Prozess gestartet. 
Damit der Raspberry Pi mit den APIs und mit RabbitMQ kommunizieren kann, muss er außerdem in einem Netzwerk mit Internetzugriff sein. Um dies durchzuführen wurde er eingangs an einen Bildschirm, und an Tastatur und Maus angeschlossen.

#### Allgemeines
Der Einstiegspunkt von MoodSpotter am Raspberry Pi befindet sich in der Datei *MoodSpotter.py*.
Hier werden zunächst die drei wichtigen Komponenten MoodCamera, MoodDetector und SpotifyConnector initialisiert.
Tritt beim Initialisieren der Kamera kein Fehler auf, so wird das main_loop gestartet, welches die Unterschiedlichen Komponenten steuert.

Mit jedem durchlauf werden also das zuvor geschossene Bild geladen. Mit diesem Bild werden die MS Cognitive Services angesprochen.
Der boolean der Funktion *ms_get_image_data()* sagt dabei aus, ob das Bild Gesichter enthält. Trifft dies zu, so wird auf Spotify nach passenden Lieder gesucht und 30 Sekunden gewartet.
Wurde kein Gesicht gefunden, so wird lediglich 5 Sekunden gewartet und Spotify nicht nach Liedern durchsucht.
Zum Abschluss wird das nächste Foto geschossen, bevor die Schleife von vorne beginnt.
```python
def main_loop():
    while True:
        img_bytes = camera.get_image_bytes()
        if moodDetector.ms_get_image_data(img_bytes):
            spotifyConnector.browse_for_mood(moodDetector.currentMood)
            sleep(30)
        else:
            sleep(5)
        camera.take_photo()
```


#### Kameramodul
Beschreibung und Code

#### Microsoft Cognitive Services
Die Face-API der Microsoft Cognitive Services dient zum erkennen von Gesichtern in Bildern. Neben allgemeneinen Informationen zum Gesicht, beispielsweise den Abständen zu Gesichtsmerkmalen, können auch kompliziertere Informationen ermittelt werden. Möglich sind beispielsweise das Geschlecht, ungefähre Alter, getragene Accessoires, von der Person getragenes Make-Up, bis zur Stimmung der Person.

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



#### Spotify-API
Spotify bietet viele verschiedene Endpoints zur Nutzung seiner Services, sowie zum Abfragen des von Spotify gebotenen Inhalts.
Mölich sind unter anderem Abfragen zu Liedern, Alben, Interpreten oder auch Nutzern. Auch das externe Steuern von mit Spotify verbundenen Geräten ist möglich. 
Die Authorisierung erfolgt mittels OAuth2, der manche Endpoints ist auch ohne Login möglich.

MoodSpotter nutzt den Browse-Endpoint der API. Dieser ermittelt anhand von Seed-Liedern dazu passende Lieder. Zusätzlich können unterschiedliche Lied-Metriken angegeben werden, die die erwarteten Ergebnisse in eine Richtung leiten oder einschränken sollen.

* target_speed:
* target

Als Antwort liefert Spotify eine durch einen Parameter festgelegte Menge an Liedern (oder weniger, bei restriktiven Abfragen).
Die Informationen zu den Liedern enthalten unter anderem Name des Liedes, Name des Albums, Interpreten, einen Link zum Starten des Liedes. Für MoodSpotter ist besonders die übermittelte eindeutige URI wichtig, anhand ihrer kann jede andere Anwendung dieses Lied abfragen.


#### RabbitMQ
Publishen der Message, URI wird gesendet - Code


### RabbitMQ Message-Broker
Nur kurz dass wir einen online Server verwenden
Beschreibung der Exchange und Queue


### Microservice 'MoodSpotterOnline'
Mittels Thorntail, kann in Docker gestartet werden. Ist Subscriber vom RabbitMQ Message Broker, hat intern eine eigene Queue. Bietet API für MoodSpotter-Web, um das nächste Lied zu holen.


### Web-Anwendung 'MoodSpotterWeb'
#### Allgemein
Umsetzung von Angular App, mit Java Scripts 

#### Spotify Playback SDK
Java Script Library, 


#### Kommunikation mit 'MoodSpotterOnline'
REST, HttpClient


#### Abspielen des Songs (Informationen zum Song)
Abspielen wird über Spotify API erreicht, Informationen zum Song über status

#### User-Interface


## Ergebnisse
Bilder aus Präsentation

ev. wie man das Projekt noch weiter ausbauen könnte 


Die Face-API der Microsoft Cognitive Services dient zum erkennen von Gesichtern in Bildern. Neben allgemeneinen Informationen zum Gesicht, beispielsweise den Abständen zu Gesichtsmerkmalen, können auch kompliziertere Informationen ermittelt werden. Möglich sind beispielsweise das Geschlecht, ungefähre Alter, getragene Accessoires, von der Person getragenes Make-Up, bis zur Stimmung der Person.
* sadness
Für MoodSpotter relevant sind insbesonders die ermittelten Informationen zur Stimmung der Person wichtig. Sie wird in sieben wichtige Stimmungen eingeteilt, zurückgegeben werden Prozentewerte, die insgesamt die Stimmung beschreiben.
Spotify bietet viele verschiedene Endpoints zur Nutzung seiner Services, sowie zum Abfragen des von Spotify gebotenen Inhalts.