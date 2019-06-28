# MoodSpotter
Projektarbeit zu Mobile und ubiquitäre Systeme (MUS).

Projekt-Team: Tom Hacker, Verena Teufl

## Projektbeschreibung
### Problembeschreibung

### Lösungsansatz


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
