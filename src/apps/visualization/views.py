from django.db.models import Q
from apps.nlp import models
from datetime import datetime
from collections import Counter
from django.http import JsonResponse


def tokens(request):
    date_filter = Q()
    initial_date = request.GET.get('initial_date', None)
    final_date = request.GET.get('final_date', None)

    if initial_date:
        initial_date = datetime.strptime(initial_date, '%d-%m-%Y')
        date_filter = date_filter & Q(
            manifestation__timestamp__gte=initial_date
        )

    if final_date:
        final_date = datetime.strptime(final_date, '%d-%m-%Y')
        date_filter = date_filter & Q(manifestation__timestamp__gte=final_date)

    man_tokens = models.ManifestationToken.objects.filter(date_filter)
    bow = Counter()
    for mt in man_tokens:
        bow.update({mt.token.stem: mt.occurrences})

    tokens = models.Token.objects.all()
    final_dict = []
    for i, stem in enumerate(bow.most_common(20)):
        token = tokens.get(stem=stem[0])

        obj = {}
        obj['id'] = token.id
        obj['token'] = token.original

        if i > 0:
            previous = final_dict[i - 1]
            obj['size'] = previous['size'] * 0.7
        else:
            obj['size'] = 1
        final_dict.append(obj)

    return JsonResponse(final_dict, safe=False)
