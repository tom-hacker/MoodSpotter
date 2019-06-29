# MoodSpotter
Projektarbeit zu Mobile und ubiquitäre Systeme (MUS)

**Projekt-Team:** Tom Hacker und Verena Teufl

## Projektbeschreibung
### Problembeschreibung
Es ist allgemein bekannt, dass Musik einen starken Einfluss auf das emotionale Befinden von Personen hat. Jedoch ist das Finden von zur Stimmung passender Musik nicht immer so einfach sowie oftmals aufwendig oder nicht möglich. Häufig wird auch einfach nur darauf „vergessen“, wie sehr die Musik die Stimmung beeinflussen kann, und deshalb kommt keine zur Stimmung passende oder gar keine Musik zum Einsatz. Obwohl meist an denselben Plätzen Musik gehört wird (Auto, Wohnzimmer, Arbeitsplatz, Lokale, etc.), gibt es keinen Weg die Musik mit wenig Aufwand an die Stimmung anzupassen. Gerade beim Autofahren wäre eine vollautomatische Stimmungserkennung und daraufhin die Anpassung der Musik von Nutzen. So könnten brenzliche Situationen im Straßenverkehr schon im Vorhinein vermieden werden. Indem bei Aufregung beruhigende und bei Müdigkeit aufputschende Musik gespielt wird.

### Lösungsansatz
Zur Lösung des oben genannten Problems wird MoodSpotter entwickelt. Auf einem Raspberry Pi mit zusätzlichem Kamera-Modul werden in regelmäßigen Abständen Bilder aufgenommen. Mithilfe der Microsoft Cognitive Services werden die Emotionen der auf dem Bild befindlichen Personen ermittelt. Aufgrund der erhaltenen Informationen werden über die Spotify-API Lieder herausgesucht, die den gewünschten Effekt erzielen könnten. Die Spotify-API bietet Informationen zur Geschwindigkeit, Lebhaftigkeit und auch zur Stimmung eines Lieds. Mithilfe dieser Informationen, und den durch die Microsoft Cognitive Services API werden Lieder ermittelt, die zur aktuellen Stimmung der Person(en) vor der Kamera passen. Die ermittelten Lieder werden über Message-Oriented-Middleware (konkret RabbitMQ) und einem zusätzlichen Microservice einer Webanwendung übermittelt, wodurch eine Art Song-Queue simuliert wird. Die Webanwendung spielt daraufhin die Musik ab. Dem Benutzer werden Informationen zum gespielten Track angezeigt (z.B. Name, Artist und Album), und ihr/ihm ist es möglich - falls ihr/ihm das aktuelle nicht Lied gefällt - auf den nächsten umzuschalten. Reagiert die/der AnwenderIn auf das Lied biespielsweise "fröhlicher" als zuvor, werden ihr/ihm als übernächte Track entsprechend der Reaktion, welche wiederrum durch den Raspberry Pi ermittelt wurde, angepasste Songs vorgeschlagen.


## Architektur
<p align="center">
  <img src="images/Architecture.JPG" width="80%"/>
</p>

Der grundlegende Aufbau von MoodSpotter wird durch obiges Diagramm dargestellt.
Die Struktur lässt sich dabei am besten anhand der Benutzung von MoodSpotter erklären. Sie läuft wie folgt ab.

1. Die Kamera des Raspberry Pi nimmt ein Foto auf. Dieses Foto wird mittels REST an die *Microsoft Cloud API* geschickt und dort evaluiert. 

2. Aufgrund der Ergebnisse bestimmt der Raspberry Pi Zielmetriken für Lieder. Diese Metriken werden der Spotify API übergeben, welche zu diesen passende Lieder ermittelt.

3. Die URIs der erhaltenen Lieder werden an RabbitMQ geschickt. Der MoodSpotterOnline-Microservice bekommt diese von RabbitMQ übermittelt und speichert sie zwischen. Abschließend ruft der Web-Client das nächste zu spielende Lied vom Microservice ab, und spielt es im Browser.

## Technische Umsetzung

### Raspberry Pi
Das Kernstück von MoodSpotter ist der Raspberry Pi. Er nimmt die Bilder auf, spricht die APIs an und übernimmt das berechnen der Ziel-Liedmetriken.

#### Setup
Als Betriebssystem wird Raspian verwendet. Das Kameramodul wird am dafür vorgesehenen Anschluss installiert. Anschließend musste das Kamera-Modul in den Einstellungen noch aktiviert werden. //TODO: WO??
Nachdem die Anwendung 'Moodspotter' beim Starten des Raspberry Pis sofort starten soll, wurde der Pfad zum Einstiegspunkt in der Datei */etc/rc.local* hinterlegt.
Dadurch wird das Programm im Boot-Prozess gestartet. 
Damit der Raspberry Pi mit den APIs und mit RabbitMQ kommunizieren kann, muss er außerdem in einem Netzwerk mit Internetzugriff sein. Um dies zu konfigurieren wurde er eingangs an einen Bildschirm, und an Tastatur und Maus angeschlossen.

#### Allgemein
Der Einstiegspunkt von MoodSpotter am Raspberry Pi befindet sich in der Datei *MoodSpotter.py*.
Hier werden zunächst die drei wichtigen Komponenten *MoodCamera*, *MoodDetector* und *SpotifyConnector* initialisiert.
Tritt beim Initialisieren der Kamera kein Fehler auf, so wird die *main_loop* gestartet, welche die Unterschiedlichen Komponenten steuert.

Mit jedem Durchlauf werden also das zuvor geschossene Bild geladen. Mit diesem Bild werden die MS Cognitive Services angesprochen.
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
Die Face-API der Microsoft Cognitive Services dient zum Erkennen von Gesichtern in Bildern. Neben allgemeneinen Informationen zum Gesicht, beispielsweise den Abständen zu Gesichtsmerkmalen, können auch kompliziertere Informationen ermittelt werden. Möglich sind beispielsweise das Geschlecht, ungefähre Alter, getragene Accessoires, von der Person getragenes Make-Up, bis zur Stimmung der Person.

Für MoodSpotter relevant sind insbesonders die ermittelten Informationen zur Stimmung der Person wichtig. Jene wird in sieben wichtige Stimmungen eingeteilt, zurückgegeben werden Prozentewerte, die insgesamt die Stimmung beschreiben.

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
Spotify bietet viele verschiedene Endpoints zur Nutzung der angebotenen Services, sowie zum Abfragen des von Spotify gebotenen Inhalts.
Möglich sind unter anderem Abfragen zu Liedern, Alben, Interpreten oder auch Nutzern. Auch das externe Steuern von mit Spotify verbundenen Geräten ist möglich. 
Die Authorisierung erfolgt mittels OAuth2. Jedoch können einige Endpoints auch ohne Login genutzt werden.

MoodSpotter nutzt den Browse-Endpoint der API. Dieser ermittelt anhand von Seed-Liedern dazu passende weitere Tracks. Zusätzlich können unterschiedliche Lied-Metriken angegeben werden, welche die erwarteten Ergebnisse in eine Richtung leiten oder einschränken sollen.

//TODO?
* target_speed:
* target

Als Antwort liefert Spotify eine durch einen Parameter festgelegte Menge an Liedern (oder weniger, bei restriktiven Abfragen).
Die Informationen zu den Liedern enthalten unter anderem den Name des Liedes, Name des Albums, Interpreten und einen Link zum Starten des Liedes in der eigenen Spotify-Weboberfläche (https://open.spotify.com). Für MoodSpotter ist besonders die übermittelte eindeutige URI wichtig, anhand ihrer kann jede andere Anwendung dieses Lied abfragen und daraufhin abspielen.


#### RabbitMQ
//TODO: Publishen der Message, URI wird gesendet - Code


### RabbitMQ Message-Broker
#### Allgemein
Damit das Raspberry Pi Modul und die MoodSpotter-Webanwendung miteinander kommunizieren können, tauschen sich diese über Message-Oriented-Middleware, konkret RabbitMQ aus. Beziehungweise die Webanwendung indirekt, da eigentlich ein zusätzlicher Microservice 'MoodSpotterOnline' Subscriber ist und die erhaltenen Lieder daraufhin der Webanwendung anbietet.

Da sich der Raspberry Pi und der Microservice unter realen Bedingungen in unterschiedlichen Netzwerken befinden, musste, um auf beiden Seiten eine simple Anbindung an den RabbitMQ-Broker zu ermöglich, eine entsprechende Lösung evaluiert werden. Es wurde auf einen Anbieter gesetzt, welcher RabbitMQ-Insatzen (unteranderem gratis) online hostet (https://www.cloudamqp.com/). Dadurch wird der RabbitMQ Message-Broker über eine fixe Web-URL zugänglich, auf welche sich der RaspberryPi und der Microservice (solange diese Internetzugriff haben) verbinden können.

#### Aufbau
Wie schon im Abschnitt zu *Raspberry Pi und RabbitMQ* hervorgeht, gibt es am RabbitMQ-Broker eine vordefinierte Exchange. Jene hat den Namen *songExchange* und ist vom Typ *DIRECT*. 

<p align="center">
  <img src="images/exchange.PNG" width="60%"/>
</p>

Die zu spielendenden Lieder werden an die Queue *songs* geroutet, welche mit dem Routing-Key *songs* an obige Exchange gebunden ist.

<p align="center">
  <img src="images/queue.PNG" width="60%"/>
</p>

<p align="center">
  <img src="images/message.PNG" width="60%"/>
</p>


### Microservice 'MoodSpotterOnline'
#### Allgemein
Der Microservice wurde mittels Java EE und dem Microserivce-Framework 'Thorntail' (https://thorntail.io/) umgesetzt. Dadurch kann dieser Service später überall leichtgewichtigt deployt werden und ist von keinem umgebenden Application-Server abhängig.

#### RabbitMQ und Song-Queue
Der Microservice ist Subscriber der Queue *songs*. Die Logik zum Holen der Songs befindet sich in der Klasse *RabbitMQClient*. 

```java
Connection connection = factory.newConnection();
            Channel channel = connection.createChannel();
            
channel.basicConsume(QUEUE_NAME, true,
        new DefaultConsumer(channel) {
            @Override
            public void handleDelivery(String consumerTag,
                                       Envelope envelope,
                                       AMQP.BasicProperties properties,
                                       byte[] body)
                    throws IOException {
                System.out.print("Message received: ");
                message = new String(body);
                System.out.println("(Spotify-URI) " + message);
                uriQueue.add(message);
            }
        });
```

Logging beim Empfangen einer Nachricht:
<p align="center">
  <img src="images/microservice.PNG" width="60%"/>
</p>


#### REST-Schnittstelle


#### Docker-Deployment
Durch den Einsatz des Microserivce-Framework ist es möglich, den Service in einem Docker-Container laufen zu lassen. Der Doker-Container wird über folgendes *docker-compose.yml* konfiguriert und lässt sich anschließend mit *docker-compose up* hochfahren:



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
