
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Strips time from date field in the Sessie model"

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE Login_sessie SET datum = DATE(datum);")
        self.stdout.write(self.style.SUCCESS('Successfully updated date fields.'))
