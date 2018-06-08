from django.db import models
from collections import Counter
import json


class Token(models.Model):
    stem = models.CharField(max_length=255, unique=True)
    bigram = models.BooleanField(default=False)
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


class Analysis(models.Model):
    TOKEN = 'token'
    AUTHOR = 'author'
    MANIFESTATION = 'manifestation'
    ANALYSIS_TYPE_CHOICES = (
        (TOKEN, 'Token'),
        (AUTHOR, 'Author'),
        (MANIFESTATION, 'Manifestation'),
    )

    UNIGRAM_BOW = 'unigram_bow'
    BIGRAM_BOW = 'bigram_bow'
    ALGORITHM_CHOICES = (
        (UNIGRAM_BOW, 'Unigram Bag of Words'),
        (BIGRAM_BOW, 'Bigram Bag of Words'),
    )

    manifestation_type = models.ForeignKey('core.ManifestationType',
                                           on_delete=models.CASCADE)
    analysis_type = models.CharField(max_length=13,
                                     choices=ANALYSIS_TYPE_CHOICES)
    algorithm = models.CharField(max_length=100, choices=ALGORITHM_CHOICES)
    stem = models.CharField(max_length=255, null=True, blank=True)
    profile_id = models.IntegerField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    _data = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Token Analysis"
        verbose_name_plural = "Token Analysiss"

    def __str__(self):
        return '{}: {} - {}'.format(self.analysis_type, self.start_date,
                                    self.end_date)

    @property
    def data(self):
        if self._data:
            return Counter(json.loads(self._data))
        else:
            return []

    @data.setter
    def data(self, value):
        self._data = json.dumps(value)
