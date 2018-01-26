from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField


class Channel(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    means_of_access = models.CharField(max_length=200, null=True, blank=True)
    manifestation_attrs = JSONField()
    author_attrs = JSONField()
    collect_attrs = JSONField()

    class Meta:
        verbose_name = _('channel')
        verbose_name_plural = _('channels')

    def __str__(self):
        return self.name


class Collect(models.Model):
    initial_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    channel = models.ForeignKey(Channel, related_name='collects',
                                on_delete=models.CASCADE)
    data = JSONField()

    class Meta:
        verbose_name = _('collect')
        verbose_name_plural = _('collects')

    def __str__(self):
        return '%s <%s>' % (self.attrs, self.channel.name)


class Author(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    author_type = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=200, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    CEP = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = _('author')
        verbose_name_plural = _('authors')

    def __str__(self):
        return '%s <%s>' % (self.attrs, self.channel.name)


class Profile(models.Model):
    url = models.CharField(max_length=200, null=True, blank=True)
    author = models.ForeignKey(Author, related_name='profiles', null=True,
                               blank=True, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, related_name='profiles',
                                on_delete=models.CASCADE)
    is_reference = models.BooleanField(default=False)
    data = JSONField()

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def __str__(self):
        return '%s <%s>' % (self.author.name, self.channel.name)


class Manifestation(models.Model):
    channel = models.ForeignKey(Channel, related_name='manifestations',
                                on_delete=models.CASCADE)
    id_in_channel = models.CharField(max_length=200)
    version = models.IntegerField(default=1)
    content = models.TextField()
    timestamp = models.DateTimeField(null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)
    data = JSONField()
    profile = models.ForeignKey(Profile, related_name='manifestations',
                                on_delete=models.CASCADE)
    collect = models.ManyToManyField(Collect, through='CollectManifestation')

    class Meta:
        verbose_name = _('manifestation')
        verbose_name_plural = _('manifestations')
        unique_together = ("id_in_channel", "version")

    def __str__(self):
        return '%s <%s>' % (self.attrs, self.channel.name)


class CollectManifestation(models.Model):
    collect = models.ForeignKey(Collect, on_delete=models.CASCADE)
    manifestation = models.ForeignKey(Manifestation, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
