import csv
import logging
import os.path
from datetime import datetime, timedelta

import requests
import xmltodict

from django_banking.models import Currency, CurrencyValue
from django_banking.settings import EXR_ENDPOINT, CSV_RESOURCE_DIR, ACCEPTED_CURRENCIES

logger = logging.getLogger(__name__)


def populate_currencies_tables(start: str = '2019-12-15', end: str = '2021-01-15'):
    # Tutorial: https://www.datacareer.de/blog/accessing-ecb-exchange-rate-data-in-python/
    key = 'D..EUR.SP00.A'

    parameters = {
        'startPeriod': start,
        'endPeriod': end
    }

    currency_names = get_currency_names()

    request_url = f"{EXR_ENDPOINT}{key}"
    response = requests.get(request_url, params=parameters)
    logger.info('Fetching currency data from EXR')
    if response.ok:
        populate_eur_currency(datetime.strptime(start, '%Y-%m-%d'), datetime.strptime(end, '%Y-%m-%d'))

        data = xmltodict.parse(response.content)
        for series in data['message:GenericData']['message:DataSet']['generic:Series']:
            iso_code = series['generic:SeriesKey']['generic:Value'][1]['@value']
            if iso_code not in ACCEPTED_CURRENCIES:
                logger.info('Skipping %s', iso_code)
                continue

            label = currency_names.get(iso_code, iso_code)
            logger.info('Populating %s', iso_code)

            obs_list = series['generic:Obs']
            currency, _ = Currency.objects.get_or_create(label=label, iso_code=iso_code)
            previous_day = None
            rate = None
            for obs in obs_list:
                day = datetime.strptime(obs['generic:ObsDimension']['@value'], '%Y-%m-%d')
                while previous_day and previous_day < day:
                    # Fill gaps in rate history
                    previous_day = previous_day + timedelta(hours=1)
                    upsert_currency_value(currency=currency, day=previous_day, rate=rate)

                rate = obs['generic:ObsValue']['@value']
                upsert_currency_value(currency=currency, day=day, rate=rate)
                previous_day = day
        logger.info('Currencies successfully populated')
    else:
        logger.info('Error fetching EXR data %s', response.text)


def upsert_currency_value(currency: Currency, day: datetime, rate: int) -> CurrencyValue:
    try:
        currency_value = CurrencyValue.objects.get(currency=currency, day=day)
        currency_value.rate = rate
        currency_value.save()
    except CurrencyValue.DoesNotExist:
        currency_value = CurrencyValue.objects.create(currency=currency, day=day, rate=rate)
    return currency_value


def populate_eur_currency(start_date: datetime, end_date: datetime):
    # This takes some thinking away from the CSV import by simply making the EUR worth 1 EUR.
    logger.info('Populating EUR')
    currency, _ = Currency.objects.get_or_create(label='Euro', iso_code='EUR')
    day = start_date
    while day <= end_date:
        CurrencyValue.objects.get_or_create(currency=currency, day=day, rate=1)
        day = day + timedelta(days=1)


def get_currency_names() -> dict:
    curencies = {}
    with open(os.path.join(CSV_RESOURCE_DIR, 'currencies.csv')) as f:
        csv_reader = csv.reader(f)
        next(csv_reader, None)  # skip the headers
        for row in csv_reader:
            curencies[row[2]] = row[1]
    return curencies
