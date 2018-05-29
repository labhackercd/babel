from django.core.management.base import BaseCommand
from django.db.models import Q
from django.db import transaction
from apps.nlp import models as nlp_models
from apps.core import models as core_models
from dateutil.rrule import rrule, MONTHLY
from calendar import monthrange
from collections import Counter
from click import progressbar, secho
import datetime


class Command(BaseCommand):
    help = 'Tokenize data and persist analysis'

    def handle(self, *args, **options):
        secho('Selecting data on database...')
        man_tokens = nlp_models.ManifestationToken.objects.all().order_by(
            'manifestation__timestamp'
        )
        start_date = man_tokens.first().manifestation.timestamp
        end_date = man_tokens.last().manifestation.timestamp
        secho('Done!', bold=True)

        for date in rrule(MONTHLY, dtstart=start_date, until=end_date):
            days = monthrange(date.year, date.month)[1]
            start_date = datetime.datetime(date.year, date.month, 1)
            end_date = datetime.datetime(date.year, date.month, days)

            self.token_analysis(man_tokens, start_date, end_date)

    def get_time_filter(self, start_date, end_date):
        return Q(manifestation__timestamp__gte=start_date,
                 manifestation__timestamp__lte=end_date)

    @transaction.atomic
    def token_analysis(self, queryset, start_date, end_date):
        queryset = queryset.filter(self.get_time_filter(start_date, end_date))
        secho('Processing data from ', nl=False)
        secho('{} to {}'.format(start_date, end_date), bold=True)

        for man_type in core_models.ManifestationType.objects.all():
            secho('Processing ', nl=False)
            secho(man_type.name, bold=True)
            man_tokens = queryset.filter(
                manifestation__manifestation_type=man_type
            )

            bow = Counter()
            with progressbar(man_tokens) as bar:
                for man_token in bar:
                    bow.update({man_token.token.stem: man_token.occurrences})

            if len(bow) > 0:
                analysis = nlp_models.Analysis.objects.get_or_create(
                    manifestation_type=man_type,
                    start_date=start_date,
                    end_date=end_date,
                    analysis_type=nlp_models.Analysis.TOKEN
                )[0]
                analysis.data = bow
                analysis.save()
