from django.contrib import admin
from apps.core import models
import nested_admin


class ProfileDomainAttributeInline(nested_admin.NestedTabularInline):
    model = models.ProfileDomainAttribute
    extra = 1


class CollectDomainAttributeInline(nested_admin.NestedTabularInline):
    model = models.CollectDomainAttribute
    extra = 1


class RelationshipProfileDomainAttributeInline(nested_admin.NestedTabularInline):
    model = models.RelationshipProfileDomainAttribute
    extra = 1


class ManifestationDomainAttributeInline(nested_admin.NestedTabularInline):
    model = models.ManifestationDomainAttribute
    extra = 1


class ManifestationTypeInline(nested_admin.NestedStackedInline):
    model = models.ManifestationType
    extra = 1

    inlines = [
        ManifestationDomainAttributeInline,
        RelationshipProfileDomainAttributeInline,
    ]


class ChannelAdmin(nested_admin.NestedModelAdmin):

    inlines = [
        ManifestationTypeInline,
        ProfileDomainAttributeInline,
        CollectDomainAttributeInline,
    ]


class CollectAttributeInline(nested_admin.NestedStackedInline):
    model = models.CollectAttribute
    extra = 1


class CollectAdmin(nested_admin.NestedModelAdmin):

    inlines = [
        CollectAttributeInline,
    ]


class ProfileAttributeInline(nested_admin.NestedStackedInline):
    model = models.ProfileAttribute
    extra = 1


class ProfileAdmin(nested_admin.NestedModelAdmin):

    inlines = [
        ProfileAttributeInline,
    ]


class ManifestationAttributeInline(nested_admin.NestedStackedInline):
    model = models.ManifestationAttribute
    extra = 1


class ManifestationAdmin(nested_admin.NestedModelAdmin):

    inlines = [
        ManifestationAttributeInline,
    ]


class RelationshipProfileAttributeInline(nested_admin.NestedStackedInline):
    model = models.RelationshipProfileAttribute
    extra = 1


class RelationshipProfileAdmin(nested_admin.NestedModelAdmin):

    inlines = [
        RelationshipProfileAttributeInline,
    ]


admin.site.register(models.Channel, ChannelAdmin)
admin.site.register(models.Manifestation, ManifestationAdmin)
admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.Author)
admin.site.register(models.Collect, CollectAdmin)
admin.site.register(models.RelationshipProfile, RelationshipProfileAdmin)
