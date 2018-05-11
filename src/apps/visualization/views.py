from django.db.models import Q
from django.shortcuts import get_object_or_404
from apps.nlp import models
from apps.core.models import Manifestation
from datetime import datetime
from collections import Counter
from django.http import JsonResponse


def get_date_filter(field_name, request):
    date_filter = Q()
    initial_date = request.GET.get('initial_date', None)
    final_date = request.GET.get('final_date', None)

    if initial_date:
        initial_date = datetime.strptime(initial_date, '%d-%m-%Y')
        kwargs = {"{field_name}__timestamp__gte": initial_date}
        date_filter = date_filter & Q(**kwargs)

    if final_date:
        final_date = datetime.strptime(final_date, '%d-%m-%Y')
        kwargs = {"{field_name}__timestamp__lte": final_date}
        date_filter = date_filter & Q(**kwargs)

    return date_filter


def tokens(request):
    date_filter = get_date_filter('manifestation', request)
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
        obj['stem'] = token.stem

        if i > 0:
            previous = final_dict[i - 1]
            obj['size'] = previous['size'] * 0.7
        else:
            obj['size'] = 1
        final_dict.append(obj)

    return JsonResponse(final_dict, safe=False)


def token_authors(request, token):
    date_filter = get_date_filter('manifestation', request)
    token_filter = Q(token__stem=token) & date_filter
    man_tokens = models.ManifestationToken.objects.filter(token_filter)
    bow = Counter()
    for mt in man_tokens:
        bow.update({mt.manifestation.profile: mt.occurrences})

    final_dict = []
    for i, profile in enumerate(bow.most_common()):
        profile = profile[0]
        obj = {
            'token': profile.author.name,
            'id': profile.id,
        }

        if i > 0:
            previous = final_dict[i - 1]
            obj['size'] = previous['size'] * 0.7
        else:
            obj['size'] = 1

        final_dict.append(obj)

    return JsonResponse(final_dict, safe=False)


def token_author_manifestations(request, token, author_id):
    date_filter = get_date_filter('manifestation', request)
    token_filter = Q(token__stem=token) & date_filter
    token_filter = token_filter & Q(manifestation__profile__id=author_id)
    man_tokens = models.ManifestationToken.objects.filter(token_filter)

    bow = Counter()
    for mt in man_tokens:
        bow.update({mt.manifestation: mt.occurrences})

    final_dict = []
    for i, manifestation in enumerate(bow.most_common()):
        manifestation = manifestation[0]
        obj = {
            'id': manifestation.id,
            'date': manifestation.timestamp.strftime('%d/%m/%Y'),
            'time': manifestation.timestamp.strftime('%H:%M'),
            'preview': manifestation.content[:70] + '...',
        }
        final_dict.append(obj)
    return JsonResponse(final_dict, safe=False)


def manifestation(request, manifestation_id):
    manifestation = get_object_or_404(Manifestation, pk=manifestation_id)
    return JsonResponse(
        {
            'date': manifestation.timestamp.strftime('%d/%m/%Y'),
            'time': manifestation.timestamp.strftime('%H:%M'),
            'content': manifestation.content,
        }
    )
