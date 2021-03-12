> ⚠ **Warning:** This README is kept in German because the Weißwurst-Event Management System (WEMS) is meant for a German-speaking audience only. Now that I think about it, it isn't even meant for all German-speakers. Please consult [Weißwurstäquator](https://en.wikipedia.org/wiki/Wei%C3%9Fwurst%C3%A4quator) for more information and to check if this software is applicable in your region.

## Weißwurst-Event Management System (WEMS)
### Einfach zu bedienende Webanwendung zur Verwaltung von Weißwurst-Events bzw. -Treffen.

Wer kennt sie nicht: die langen, langen Excel-Tabellen zur Berechnung des nächsten Weißwurstkönigs. Blickt da überhaupt noch jemand durch? Und: Wo ist da eigentlich die Management-Summary dazu?

Das Django-basierte Weißwurst-Event Management System (kurz WEMS) löst ab sofort all deine Probleme!  
In einer schicken, schlanken Web-UI können du und deine Kollegen Weißwurst-Events eintragen, Teilnahmen protokollieren, den Senf bewerten und automagisch E-Mails erhalten, sobald der nächste dran ist (ja, natürlich mit Fingerzeig!).

[![Screenshot 1](https://raw.githubusercontent.com/ignitedPotato/wems/main/screenshot1_thumb.png)](https://raw.githubusercontent.com/ignitedPotato/wems/main/screenshot1.png)
[![Screenshot 3](https://raw.githubusercontent.com/ignitedPotato/wems/main/screenshot3_thumb.png)](https://raw.githubusercontent.com/ignitedPotato/wems/main/screenshot3.png)
[![Screenshot 2](https://raw.githubusercontent.com/ignitedPotato/wems/main/screenshot2_thumb.png)](https://raw.githubusercontent.com/ignitedPotato/wems/main/screenshot2.png)

Um die Verwaltung so einfach wie möglich zu halten, gibt es kein Berechtigungskonzept. Jeder kann für jeden alles eintragen. Nur das Löschen von Events, Teilnahmen und Bewertungen und die Anlage von Benutzern, Abteilungen und Räumen ist einem Admin überlassen, der Zugriff auf das Admininterface erhält.

### Setup
#### docker-compose
```yaml
version: "3"

services:
  wwtool:
    image: ignitedpotato/wems
    volumes:
      - ./static:/app/static
      - ./db:/app/db
    ports:
      - "127.0.0.1:8000:8000"
    environment:
      - SECRET_KEY=<insert_key_here>
      - WWEMS_URL="http://localhost:8000"
    restart: always
```

```bash
# Run
docker-compose up -d

# Create superuser
docker-compose exec wwtool python manage.py createsuperuser
```

#### Static Files
Static files müssen von einem Reverse-Proxy ausgeliefert werden. Dieser muss also entsprechend konfiguriert werden.
Im Repository liegen Beispielkonfigurationen für Caddy v1 und v2.

#### Cron-Jobs
Damit das Weißwurst-Event Management System automatisch Erinnerungsmails verschickt, muss ein Cron-Job eingerichtet werden.  
Hier ein Beispiel, das stündlich (jeweils 5 Minuten nach der vollen Stunde) prüft, ob Emails zu verschicken sind:
```
05 * * * *      cd /path/to/WEMS/ && docker-compose exec wwtool python manage.py cronjobs
```

### Konfiguration
#### ENV-Variablen
* `DEBUG`: Aktiviert den Debugmodus und ermöglicht das direkte Hosten mittels `python manage.py runserver`
* `SECRET_KEY`: Muss gesetzt werden, dient der Absicherung von Admin-Sitzungen
* `WWEMS_URL`: Vollständige öffentliche URL des Systems (z. B. `https://wwtool.test.de/ww`); wird in Emails verwendet und zum Festlegen der ALLOWED_HOSTS
* `USE_X_FORWARDED_HOST`: Nutze `X-Forwarded-Host`-Header anstelle dem `Host`-Header zur Prüfung der ALLOWED_HOSTS

#### E-Mail
Für den Versand von E-Mails existieren die Variablen, die Django zum Mailversand nutzt:
https://docs.djangoproject.com/en/3.1/topics/email/#smtp-backend


### Entwicklung
#### Verwendete Frameworks:
* django (https://www.djangoproject.com/)
* Fomantic UI (https://fomantic-ui.com/)
* Chart.js (https://www.chartjs.org/)
* jQuery (https://jquery.com/)
* jQuery DateTimePicker (https://github.com/xdan/datetimepicker)

#### Setup
Um das Weißwurst-Event Management System ausführen zu können, werden folgende Pakete benötigt:
* python >= 3.8
* django >= 3.0
* django-environ
* yarn

#### Erster Start
Beim ersten Start müssen die Datenbank und ein Administratoraccount angelegt werden:
```bash
yarn
yarn build
mkdir db
export SECRET_KEY=changeme
python manage.py migrate
python manage.py createsuperuser
```

Im Anschluss kann das System wie folgt gestartet werden:
```bash
export SECRET_KEY=changeme
export DEBUG=True
python manage.py runserver 127.0.0.1:8000
```

Das Weißwurst-Event Management System ist im Anschluss unter der Adresse http://localhost:8000 verfügbar.

#### Docker
```bash
# Prepare
yarn
yarn build

# Build
docker build -t wwtool .

# Run
docker run -d -p 127.0.0.1:8000:8000 --name wwtool --restart always -v /srv/static:/app/static -v /srv/db:/app/db -e SECRET_KEY=<insert_key_here> -e WWEMS_URL="http://localhost:8000" wwtool:latest

# Create superuser
docker exec -it wwtool python manage.py createsuperuser
```

#### settings.py
Die Datei `WeissWurstTool/settings.py` enthält weitere Möglichkeiten zur Konfiguration des Systems:
* `EMAIL_NEW_EVENT_SUBJECT`: Betreff der Email, die einen neuen zukünftigen Event ankündigt
* `EMAIL_NEW_EVENT_BODY`: Text der Email, die einen neuen zukünftigen Event ankündigt
* `EMAIL_MOD_EVENT_SUBJECT`: Betreff der Email, die die Änderung eines zukünftigen Events ankündigt
* `EMAIL_MOD_EVENT_BODY`: Text der Email, die die Änderung eines zukünftigen Events ankündigt
* `EMAIL_REMINDER_SUBJECT`: Betreff der Email, die das Anlegen eines neuen Events fordert
* `EMAIL_REMINDER_BODY`: Text der Email, die das Anlegen eines neuen Events fordert
* `EMAIL_RATING_SUBJECT`: Betreff der Email, die nach einem Event alle Teilnehmer auffordert eine Bewertung abzugeben
* `EMAIL_RATING_BODY`: Text der Email, die nach einem Event alle Teilnehmer auffordert eine Bewertung abzugeben
* `ICS_TEMPLATE`: Template der .ics-Datei, die das System für zukünftige Events zum Download anbietet und auch an Emails hängt.

#### Email-Platzhalter
Folgende Platzhalter stehen für Email-Templates zur Verfügung:
* `<User Name>`: Voller Name des aktuellen Empfängers
* `<Host Name>`: Voller Name des Hosts des Events
* `<Event Date>`: Datum des Events
* `<Event Time>`: Zeit des Events
* `<Event Room>`: Raum des Events
* `<Event Link>`: Link zum Event
* `<Next Name>`: Nächster Host
* `<Add Link>`: Link zur Anlage-Seite

## Danksagung
Danke an [Takeaway](https://commons.wikimedia.org/wiki/User:Takeaway) für das [Bild](https://de.wikipedia.org/wiki/Datei:Weisswurst_close-up.jpg) im Header (CC BY-SA 3.0).

Food-Icons erstellt von [Those Icons](https://www.flaticon.com/authors/those-icons) auf Flaticon.