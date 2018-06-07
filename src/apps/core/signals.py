from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from rest_framework.authtoken.models import Token
from apps.core.models import Manifestation
from apps.nlp import models, pre_processing


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=Manifestation)
@transaction.atomic
def process_manifestation(sender, instance, created, **kwargs):
    if not created:
        models.ManifestationToken.objects.filter(
            manifestation=instance
        ).delete()

    bow, stem_reference = pre_processing.bow(instance.content)
    if len(bow) > 0:
        max_value = max(bow.values())
        for stem, occurrences in bow.items():
            token = models.Token.objects.get_or_create(stem=stem)[0]
            for original_word, occurrences in stem_reference[stem].items():
                token.add_original_word(original_word, times=occurrences)
            token.save()

            mt = models.ManifestationToken()
            mt.manifestation = instance
            mt.token = token
            mt.occurrences = occurrences
            mt.frequency = occurrences / max_value
            mt.save()
            print(mt)

    bigram_bow, stem_reference = pre_processing.bow(instance.content, ngrams=2)
    if len(bigram_bow) > 0:
        max_value = max(bigram_bow.values())
        for token, occurrences in bigram_bow.items():
            token = models.Token.objects.get_or_create(stem=token)[0]
            t1, t2 = token.stem.split()
            token.add_original_word(' '.join([
                stem_reference[t1].most_common(1)[0][0],
                stem_reference[t2].most_common(1)[0][0]
            ]))
            token.bigram = True
            token.save()
            mt = models.ManifestationToken()
            mt.manifestation = instance
            mt.token = token
            mt.occurrences = occurrences
            mt.frequency = occurrences / max_value
            mt.save()
            print(mt)
