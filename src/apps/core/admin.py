from django.contrib import admin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
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
    list_display = ('name', 'manifestation_types')
    search_fields = ('name', 'description')
    ordering = ('name',)

    def manifestation_types(self, instance):
        return format_html_join(
            mark_safe('<br/>'),
            '{}',
            ((mtype,) for mtype in instance.manifestation_types.all()),
        )

    inlines = [
        ManifestationTypeInline,
        ProfileDomainAttributeInline,
        CollectDomainAttributeInline,
    ]


class CollectAttributeInline(nested_admin.NestedStackedInline):
    model = models.CollectAttribute
    extra = 1


class CollectAdmin(nested_admin.NestedModelAdmin):
    list_display = ('channel', 'periodicity', 'initial_time', 'end_time')
    list_filter = ('channel__name',)
    search_fields = ('channel__name',)
    ordering = ('channel__name',)

    inlines = [
        CollectAttributeInline,
    ]


class ProfileAttributeInline(nested_admin.NestedStackedInline):
    model = models.ProfileAttribute
    extra = 1


class ProfileAdmin(nested_admin.NestedModelAdmin):
    list_display = ('author', 'id_in_channel', 'url', 'channel', 'is_reference')
    list_filter = ('author__gender', 'channel__name', 'is_reference',
                   'author__name')
    search_fields = ('id_in_channel', 'url', 'channel__name', 'author__name')
    ordering = ('author__name',)

    inlines = [
        ProfileAttributeInline,
    ]


class ManifestationAttributeInline(nested_admin.NestedStackedInline):
    model = models.ManifestationAttribute
    extra = 1


class ManifestationAdmin(nested_admin.NestedModelAdmin):
    list_display = ('short_content', 'manifestation_type', 'version', 'profile')
    list_filter = ('manifestation_type__channel__name',
                   'manifestation_type__name', 'profile__author',)
    search_fields = ('id_in_channel', 'url', 'timestamp', 'content',
                     'profile__author__name', 'manifestation_type__name',
                     'manifestation_type__channel__name')
    ordering = ('timestamp',)
    inlines = [
        ManifestationAttributeInline,
    ]


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'profiles', 'author_type', 'gender', 'birthdate',
                    'cep')
    list_filter = ('gender', 'birthdate', 'author_type')
    search_fields = ('name', 'author_type', 'gender', 'cep')
    ordering = ('name',)

    def profiles(self, instance):
        return format_html_join(
            mark_safe('<br/>'),
            '{}',
            ((profile,) for profile in instance.profiles.all()),
        )


class CollectManifestationAdmin(admin.ModelAdmin):
    list_display = ('collect', 'manifestation', 'timestamp')
    list_filter = ('collect__channel__name',
                   'manifestation__manifestation_type__name', 'timestamp')
    search_fields = ('collect__channel__name', 'manifestation__content',
                     'manifestation__manifestation_type__name')
    ordering = ('timestamp',)


class RelationshipProfileAttributeInline(nested_admin.NestedStackedInline):
    model = models.RelationshipProfileAttribute
    extra = 1


class RelationshipProfileAdmin(nested_admin.NestedModelAdmin):
    list_display = ('profile', 'manifestation', 'relationship_type')
    list_filter = ('profile__channel__name',
                   'manifestation__manifestation_type__name',
                   'relationship_type', 'profile__author__name')
    search_fields = ('profile__author__name', 'profile__channel__name',
                     'manifestation__manifestation_type__name')
    ordering = ('profile__author__name',)

    inlines = [
        RelationshipProfileAttributeInline,
    ]


admin.site.register(models.Channel, ChannelAdmin)
admin.site.register(models.Manifestation, ManifestationAdmin)
admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.Collect, CollectAdmin)
admin.site.register(models.CollectManifestation, CollectManifestationAdmin)
admin.site.register(models.RelationshipProfile, RelationshipProfileAdmin)
