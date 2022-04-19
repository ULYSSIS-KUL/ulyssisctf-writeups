# bright-coloured-fish writeup

Als je op Google zoekt naar het bestandstype van de file die je krijgt (`mp3`) samen met de challengenaam (`bright-coloured-fish`) gaan enkele resultaten over de ID3v2 standaard. In die standaard kun je vinden dat `A bright coloured fish` een picture type is. In [dat hoofdstuk](https://id3.org/id3v2.3.0#Attached_picture) staat ook dat een bestand meerdere afbeeldingen kan hebben. Om de flag te vinden moet je alle afbeeldingen uit het bestand halen. Dit kan met behulp van een tool zoals [eyeD3](http://eyed3.nicfit.net/). Een van deze afbeeldingen bevat de flag.
