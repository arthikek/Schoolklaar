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

## Superuser aanmaken
    ```
    python manage.py createsuperuser
    ```