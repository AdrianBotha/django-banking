from django.core.management import BaseCommand

from django_banking.services import currency


class Command(BaseCommand):
    help = 'Update Currencies'

    def handle(self, *args, **options):
        currency.populate_currencies_tables()
