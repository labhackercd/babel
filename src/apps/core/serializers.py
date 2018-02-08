from rest_framework import serializers
from apps.core import models


class ProfileDomainAttributeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.ProfileDomainAttribute
        fields = ('id', 'name', 'description', 'is_mandatory')


class CollectDomainAttributeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.CollectDomainAttribute
        fields = ('id', 'name', 'description', 'is_mandatory')


class ChannelSerializer(serializers.HyperlinkedModelSerializer):
    collect_domain_attrs = CollectDomainAttributeSerializer(
        many=True, read_only=True)
    profile_domain_attrs = ProfileDomainAttributeSerializer(
        many=True, read_only=True)

    class Meta:
        model = models.Channel
        fields = ('id', 'name', 'description', 'command',
                  'collect_domain_attrs', 'profile_domain_attrs')


class ManifestationDomainAttributeSerializer(
        serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.ManifestationDomainAttribute
        fields = ('id', 'name', 'description', 'is_mandatory')


class ManifestationTypeSerializer(serializers.HyperlinkedModelSerializer):
    channel = ChannelSerializer()
    manifestation_domain_attrs = ManifestationDomainAttributeSerializer(
        many=True, read_only=True)

    class Meta:
        model = models.ManifestationType
        fields = ('id', 'name', 'channel', 'manifestation_domain_attrs')


class CollectAttributeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.CollectAttribute
        fields = ('id', 'field', 'value')


class CollectSerializer(serializers.HyperlinkedModelSerializer):
    channel = ChannelSerializer()
    attrs = CollectAttributeSerializer(many=True)

    class Meta:
        model = models.Collect
        fields = ('id', 'initial_time', 'end_time', 'periodicity', 'channel',
                  'attrs')


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    profiles = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='profile-detail'
    )

    class Meta:
        model = models.Author
        fields = ('id', 'name', 'author_type', 'gender', 'birthdate', 'cep',
                  'profiles')


class ProfileAttributeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.ProfileAttribute
        fields = ('id', 'field', 'value')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    author = AuthorSerializer()
    channel = ChannelSerializer()
    attrs = ProfileAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = models.Profile
        fields = ('id', 'author', 'channel', 'url', 'is_reference', 'attrs')


class ManifestationAttributeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.ManifestationAttribute
        fields = ('id', 'field', 'value')


class ManifestationSerializer(serializers.HyperlinkedModelSerializer):
    manifestation_type = ManifestationTypeSerializer()
    profile = ProfileSerializer()
    collect = CollectSerializer(many=True)
    attrs = ManifestationAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = models.Manifestation
        fields = ('id', 'manifestation_type', 'id_in_channel', 'version',
                  'content', 'timestamp', 'url', 'profile', 'collect', 'attrs')


class CollectManifestationSerializer(serializers.HyperlinkedModelSerializer):
    manifestation = ManifestationSerializer()
    collect = CollectSerializer()

    class Meta:
        model = models.CollectManifestation
        fields = ('id', 'timestamp', 'collect', 'manifestation')
