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

Hier Kurzbeschreibung der einzelnen Komponenten:

## Technische Umsetzung

### Raspberry Pi

#### Allgemein

#### Kameramodul
Beschreibung und Code

#### Microsoft Cognitive Services
Beschreibung der API, Example Response, Auswertung und Code


#### Spotify-API
Seed-Lieder (Metrik Berechnung), API ein bisschen beschreiben, Example Response


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
