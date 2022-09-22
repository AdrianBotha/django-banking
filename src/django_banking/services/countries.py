import csv
import logging
import os

from django_banking.models import Country
from django_banking.settings import CSV_RESOURCE_DIR


logger = logging.getLogger(__name__)


def import_countries():
    logger.info('Importing countries')
    with open(os.path.join(CSV_RESOURCE_DIR, 'countries.csv')) as f:
        csv_reader = csv.reader(f)
        next(csv_reader, None)  # skip the headers
        for row in csv_reader:
            Country.objects.get_or_create(label=row[0], slug=row[1])
    logger.info('Countries imported')
