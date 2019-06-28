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