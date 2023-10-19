# Django Project README

## Omschrijving
Deze Django-applicatie is opgezet met verschillende pakketten, inclusief ondersteuning voor authenticatie via django-allauth en een API-opzet met djangorestframework. De gedetailleerde lijst van pakketten en versies is te vinden in het requirements.txt bestand.

## Vereisten
- Python (Zorg ervoor dat je de correcte versie geïnstalleerd hebt die compatibel is met de pakketten in requirements.txt).
- pip (Python pakket installer)

## Setup & Installatie
1. Kloon de repository:
    ```
    git clone [JOUW_REPOSITORY_URL]
    cd [JOUW_REPOSITORY_NAAM]
    ```
2. Zet een virtuele omgeving op (optioneel maar aanbevolen):
    ```
    python -m venv venv
    source venv/bin/activate  # Op Windows, gebruik `venv\Scripts\activate`
    ```
3. Installeer de vereiste pakketten:
    ```
    pip install -r requirements.txt
    ```
4. Voer migraties uit:
    ```
    python manage.py migrate
    ```
5. Stel omgevingsvariabelen in (als je python-dotenv gebruikt, kun je deze toevoegen aan een .env bestand):
    - Zorg ervoor dat je alle noodzakelijke API-sleutels, geheime sleutels of andere configuraties instelt die vereist zijn door de geïnstalleerde pakketten.
6. Start de ontwikkelingsserver:
    ```
    python manage.py runserver
    ```
    Standaard start dit de ontwikkelingsserver op http://127.0.0.1:8000/. Je kunt de beheersite bereiken op http://127.0.0.1:8000/admin/.

## Sites Framework Configuratie
Voor het instellen van domeinen en sitenamen in Django, navigeer naar:
[http://localhost:8000/admin/sites/site/](http://localhost:8000/admin/sites/site/)

Vervang example.com door:

http://localhost:8000

## Superuser aanmaken
    ```
    python manage.py createsuperuser
    ```

## Probleemoplossing
Foutmelding met Site matching query does not exist.
Als je deze foutmelding tegenkomt, kan dit te maken hebben met een verkeerd geconfigureerd SITE_ID in settings.py.

Oplossing:

Inspecteer de django_site tabel in je database. Je kunt hiervoor gebruik maken van een database management tool afhankelijk van de database die je gebruikt (bijv. pgAdmin voor PostgreSQL, DBeaver, sqlite3, etc.). sqlite viewer in VS CODE.
Zoek naar de id waarde van de site die je gebruikt. Noteer deze id.
Open settings.py en stel de SITE_ID variabele in op de genoteerde id uit stap 2.
Voorbeeld:

Als je django_site tabel een site heeft met de id waarde 3, stel dan SITE_ID = 3 in settings.py.