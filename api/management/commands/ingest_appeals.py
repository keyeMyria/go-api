import os
import requests
from django.core.management.base import BaseCommand
from api.models import Appeal, Country, DisasterType, Event


class Command(BaseCommand):
    help = 'Add new entries from Access database file'

    def handle(self, *args, **options):
        # get latest
        url = 'http://go-api.ifrc.org/api/appeals'

        auth = (os.getenv('APPEALS_USER'), os.getenv('APPEALS_PASS'))
        response = requests.get(url, auth=auth)
        if response.status_code != 200:
            raise Exception('Error querying Appeals API')
        results = response.json()

        # read from static file for development
        # with open('appeals.json') as f:
        #     results = json.loads(f.read())

        ids = [r.aid for r in Appeal.objects.all()]

        print('%s appeals in database' % len(results))
        for i, r in enumerate(results):
            if r['APP_Id'] in ids:
                continue

            # create an Event for this
            dtype = DisasterType.objects.filter(name=r['ADT_name']).first()
            if dtype is None:
                dtype = DisasterType.objects.filter(name='Other').first()

            fields = {
                'name': r['APP_name'],
                'dtype': dtype,
                'status': r['APP_status'],
                'region': r['OSR_name'],
                'code': r['APP_code'],
            }
            event, created = Event.objects.get_or_create(eid=r['APP_Id'], defaults=fields)

            country = Country.objects.filter(name=r['OSC_name'])
            if country.count() == 0:
                country = None

            for appeal in r['Details']:
                amount_funded = 0 if appeal['ContributionAmount'] is None else appeal['ContributionAmount']
                fields = {
                    'event': event,
                    'country': country,
                    'sector': r['OSS_name'],
                    'start_date': appeal['APD_startDate'],
                    'end_date': appeal['APD_endDate'],
                    'num_beneficiaries': appeal['APD_noBeneficiaries'],
                    'amount_requested': appeal['APD_amountCHF'],
                    'amount_funded': amount_funded
                }
                item, created = Appeal.objects.get_or_create(aid=appeal['APD_code'], defaults=fields)

        items = Appeal.objects.all()
        print('%s items' % items.count())
