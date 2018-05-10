from django.db import models
from collections import Counter
import json


class Token(models.Model):
    stem = models.CharField(max_length=255, unique=True)
    _originals = models.TextField(default="{}")

    class Meta:
        verbose_name = "Token"
        verbose_name_plural = "Tokens"

    def __str__(self):
        return self.stem

    @property
    def original(self):
        originals = Counter(json.loads(self._originals))
        if len(originals) > 0:
            return originals.most_common(1)[0][0]
        else:
            return None

    def add_original_word(self, value, times=1):
        originals = Counter(json.loads(self._originals))
        originals.update({value: times})
        self._originals = json.dumps(originals)


class ManifestationToken(models.Model):
    manifestation = models.ForeignKey('core.Manifestation',
                                      related_name='tokens',
                                      on_delete=models.CASCADE)
    token = models.ForeignKey('nlp.Token', related_name='manifestations',
                              on_delete=models.CASCADE)
    occurrences = models.IntegerField(default=0)
    frequency = models.FloatField(default=0)

    class Meta:
        verbose_name = "Manifestation Token"
        verbose_name_plural = "Manifestation Tokens"
        ordering = ['-occurrences']

    def __str__(self):
        return '{} in {}'.format(self.token.stem, self.manifestation.__str__())