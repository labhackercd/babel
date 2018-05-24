from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.core import model_mixings
from django.template.defaultfilters import truncatechars
from django_celery_beat.models import (PeriodicTask, IntervalSchedule,
                                       CrontabSchedule)
import json


class Channel(models.Model):
    name = models.CharField(verbose_name=_("channel"), max_length=200)
    description = models.TextField(null=True, blank=True)
    command = models.TextField()

    class Meta:
        verbose_name = _('channel')
        verbose_name_plural = _('channels')

    def __str__(self):
        return self.name


class ProfileDomainAttribute(model_mixings.DomainAttributeMixing):
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        related_name='profile_domain_attrs'
    )

    class Meta:
        verbose_name = _("Profile Domain Attribute")
        verbose_name_plural = _("Profile Domain Attributes")


class ManifestationType(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE,
                                related_name='manifestation_types')
    name = models.CharField(verbose_name=_("manifestation type"), max_length=100)

    class Meta:
        verbose_name = _("Manifestation Type")
        verbose_name_plural = _("Manifestation Types")

    def __str__(self):
        return '%s <%s> id:%d' % (self.name, self.channel.name, self.id)


class CollectDomainAttribute(model_mixings.DomainAttributeMixing):
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        related_name='collect_domain_attrs'
    )

    class Meta:
        verbose_name = _("Collect Domain Attribute")
        verbose_name_plural = _("Collect Domain Attributes")


class ManifestationDomainAttribute(model_mixings.DomainAttributeMixing):
    manifestation_type = models.ForeignKey(
        ManifestationType,
        on_delete=models.CASCADE,
        related_name='manifestation_domain_attrs'
    )
    is_versioned = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Manifestation Domain Attribute")
        verbose_name_plural = _("Manifestation Domain Attributes")


class RelationshipProfileDomainAttribute(model_mixings.DomainAttributeMixing):
    manifestation_type = models.ForeignKey(
        ManifestationType,
        on_delete=models.CASCADE,
        related_name='relationship_profile_domain_attrs'
    )

    class Meta:
        verbose_name = _("Relationship Profile Domain Attribute")
        verbose_name_plural = _("Relationship Profile Domain Attributes")


class Collect(models.Model):
    channel = models.ForeignKey(
        Channel,
        related_name='collects',
        on_delete=models.CASCADE
    )
    initial_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    periodicity = models.IntegerField(
        default=0,
        help_text=_('Run script every X seconds')
    )

    class Meta:
        verbose_name = _('collect')
        verbose_name_plural = _('collects')

    def __str__(self):
        return self.channel.name


class CollectAttribute(model_mixings.AttributeMixing):
    collect = models.ForeignKey(Collect, related_name='attrs',
                                on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('collect attribute')
        verbose_name_plural = _('collect attributes')


class Author(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    author_type = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=200, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    cep = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = _('author')
        verbose_name_plural = _('authors')

    def __str__(self):
        return self.name


class Profile(models.Model):
    id_in_channel = models.CharField(max_length=200)
    url = models.TextField(null=True, blank=True)
    author = models.ForeignKey(Author, related_name='profiles', null=True,
                               blank=True, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, related_name='profiles',
                                on_delete=models.CASCADE)
    is_reference = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def __str__(self):
        return '%s <%s>' % (self.author.name, self.channel.name)


class ProfileAttribute(model_mixings.AttributeMixing):
    profile = models.ForeignKey(Profile, related_name='attrs',
                                on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('profile attribute')
        verbose_name_plural = _('profile attributes')


class Manifestation(models.Model):
    manifestation_type = models.ForeignKey(
        ManifestationType,
        related_name='manifestations',
        on_delete=models.CASCADE
    )
    id_in_channel = models.CharField(max_length=200)
    version = models.IntegerField(default=1)
    content = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    profile = models.ForeignKey(Profile, related_name='manifestations',
                                on_delete=models.CASCADE)
    collect = models.ManyToManyField(Collect, through='CollectManifestation')

    class Meta:
        verbose_name = _('manifestation')
        verbose_name_plural = _('manifestations')

    def __str__(self):
        return '%s <%s>' % (self.id_in_channel,
                            self.manifestation_type.channel.name)

    @property
    def short_content(self):
        return truncatechars(self.content, 150)


class ManifestationAttribute(model_mixings.AttributeMixing):
    manifestation = models.ForeignKey(Manifestation, related_name='attrs',
                                      on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('manifestation attribute')
        verbose_name_plural = _('manifestation attributes')


class CollectManifestation(models.Model):
    collect = models.ForeignKey(Collect, on_delete=models.CASCADE)
    manifestation = models.ForeignKey(Manifestation, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)


class RelationshipProfile(models.Model):
    manifestation = models.ForeignKey(Manifestation,
                                      related_name='relationships',
                                      on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, related_name='relationships',
                                on_delete=models.CASCADE)
    relationship_type = models.CharField(max_length=200)

    class Meta:
        verbose_name = _('relationship profile')
        verbose_name_plural = _('relationship profiles')

    def __str__(self):
        return '%s <%s>' % (self.manifestation.manifestation_type.name,
                            self.manifestation.manifestation_type.channel.name)


class RelationshipProfileAttribute(model_mixings.AttributeMixing):
    relationship_profile = models.ForeignKey(RelationshipProfile,
                                             related_name='attrs',
                                             on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('relationship profile attribute')
        verbose_name_plural = _('relationship profile attributes')


def collect_post_save(sender, instance, created, **kwargs):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=instance.periodicity,
        period=IntervalSchedule.SECONDS,
    )
    periodic_task = PeriodicTask.objects.create(
        interval=schedule,
        name='Get %s data' % (instance.channel.name),
        task='apps.core.tasks.get_channel_data',
        kwargs=json.dumps({'channel_id': instance.id}),
        # start_time=instance.initial_time,   ## available in next version
        last_run_at=instance.end_time,
        enabled=False
    )
    crontab_schedule, crontab_created = CrontabSchedule.objects.get_or_create(
        minute=instance.initial_time.minute,
        hour=instance.initial_time.hour,
        day_of_month=instance.initial_time.day,
        month_of_year=instance.initial_time.month,
    )
    PeriodicTask.objects.create(
        crontab=crontab_schedule,
        name='Start crawl %s at' % (instance.channel.name),
        task='apps.core.tasks.start_periodic_task',
        kwargs=json.dumps({
            'periodic_id': periodic_task.id,
        })
    )


models.signals.post_save.connect(collect_post_save, sender=Collect)
