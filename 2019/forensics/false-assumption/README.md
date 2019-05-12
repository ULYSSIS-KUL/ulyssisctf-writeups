# False assumption

```
We zouden graag weten wat er in het bestand vermeld in de mail hieronder zit. We hebben daarvoor een geheime camera laten installeren, echter was deze alleen op het toetsenbord gericht. Daarmee konden we afleiden dat de gebruikersnaam en wachtwoord de volgende waren:

cqen
oel,qemqf

Echter lijken deze niet te werken, kan je even nakijken wat er mis is? 

From: len
To: mark.xavier
Subject: Secret file

Hi mark,

Here's the sectret file you requested.
Username and password are the usual ones.

Len
```

## Writeup

De fout die hier werd gemaakt is dat de keyboard layout niet degene is die op de video te zien is. Hoe kunnen we dan echter de juiste vinden? Kijken we naar de naam van de persoon naar wie de email gestuurd is dan zien we dat die helemaal niet overeenkomt met de username die hij gebruikt voor de flag te lezen. Op https://en.wikipedia.org/wiki/Keyboard_layout is de eerste layout waarbij de 'c' van AZERTY een 'm' is de Workman layout. Verder komt 'cqen' volledig overeen met 'mark'. We krijgen dan voor het wachtwoord 'proletariat' en kunnen inloggen.
