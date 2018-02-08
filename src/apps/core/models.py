from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.core import model_mixings


class Channel(models.Model):
    name = models.CharField(max_length=200)
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


class ManifestationType(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE,
                                related_name='manifestation_types')
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = _("Manifestation Type")
        verbose_name_plural = _("Manifestation Types")

    def __str__(self):
        return self.name


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

    class Meta:
        verbose_name = _("Manifestation Domain Attribute")
        verbose_name_plural = _("Manifestation Domain Attributes")


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
        return '%s <%s>' % (self.data, self.channel.name)


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
    url = models.CharField(max_length=200, null=True, blank=True)
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
    content = models.TextField()
    timestamp = models.DateTimeField(null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)
    profile = models.ForeignKey(Profile, related_name='manifestations',
                                on_delete=models.CASCADE)
    collect = models.ManyToManyField(Collect, through='CollectManifestation')

    class Meta:
        verbose_name = _('manifestation')
        verbose_name_plural = _('manifestations')
        unique_together = ("id_in_channel", "version")

    def __str__(self):
        return '%s <%s>' % (self.attrs, self.channel.name)


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
