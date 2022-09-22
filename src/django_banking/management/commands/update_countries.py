from django.core.management import BaseCommand

from django_banking.services import countries


class Command(BaseCommand):
    help = 'Update Countries'

    def handle(self, *args, **options):
        countries.import_countries()
