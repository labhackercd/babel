from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class TimestampedMixin(models.Model):
    created = models.DateTimeField(_('created'), editable=False,
                                   blank=True, auto_now_add=True)
    modified = models.DateTimeField(_('modified'), editable=False,
                                    blank=True, auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(TimestampedMixin, self).save(*args, **kwargs)


class AttributeMixing(models.Model):
    field = models.CharField(max_length=200)
    value = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = _("Attribute Mixing")
        verbose_name_plural = _("Attribute Mixings")
        abstract = True

    def __str__(self):
        return '%s <%s>' % (self.field, self.value)


class DomainAttributeMixing(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    is_mandatory = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Domain Attribute")
        verbose_name_plural = _("Domain Attributes")
        abstract = True

    def __str__(self):
        return self.name
