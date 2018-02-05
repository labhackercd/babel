from django.contrib import admin
from apps.core import models
import nested_admin


class ProfileDomainAttributeInline(nested_admin.NestedTabularInline):
    model = models.ProfileDomainAttribute
    extra = 1


class CollectDomainAttributeInline(nested_admin.NestedTabularInline):
    model = models.CollectDomainAttribute
    extra = 1


class ManifestationDomainAttributeInline(nested_admin.NestedTabularInline):
    model = models.ManifestationDomainAttribute
    extra = 1


class ManifestationTypeInline(nested_admin.NestedStackedInline):
    model = models.ManifestationType
    extra = 1

    inlines = [
        ManifestationDomainAttributeInline,
    ]


class ChannelAdmin(nested_admin.NestedModelAdmin):

    inlines = [
        ManifestationTypeInline,
        ProfileDomainAttributeInline,
        CollectDomainAttributeInline,
    ]


admin.site.register(models.Channel, ChannelAdmin)
admin.site.register(models.Manifestation)
admin.site.register(models.Profile)
admin.site.register(models.Author)
admin.site.register(models.Collect)
