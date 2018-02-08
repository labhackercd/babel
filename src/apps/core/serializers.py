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


class ManifestationDomainAttributeSerializer(
        serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.ManifestationDomainAttribute
        fields = ('id', 'name', 'description', 'is_mandatory')


class RelationshipProfileDomainAttributeSerializer(
        serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.RelationshipProfileDomainAttribute
        fields = ('id', 'name', 'description', 'is_mandatory')


class ManifestationTypeSerializer(serializers.HyperlinkedModelSerializer):
    channel = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='channel-detail'
    )
    manifestation_domain_attrs = ManifestationDomainAttributeSerializer(
        many=True, read_only=True)
    relationship_profile_domain_attrs = RelationshipProfileDomainAttributeSerializer(
        many=True, read_only=True)

    class Meta:
        model = models.ManifestationType
        fields = ('id', 'channel', 'name', 'manifestation_domain_attrs',
                  'relationship_profile_domain_attrs')


class ChannelSerializer(serializers.HyperlinkedModelSerializer):
    collect_domain_attrs = CollectDomainAttributeSerializer(
        many=True, read_only=True)
    profile_domain_attrs = ProfileDomainAttributeSerializer(
        many=True, read_only=True)
    manifestation_types = ManifestationTypeSerializer(
        many=True, read_only=True)

    class Meta:
        model = models.Channel
        fields = ('id', 'name', 'description', 'command',
                  'collect_domain_attrs', 'profile_domain_attrs',
                  'manifestation_types')


class CollectAttributeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.CollectAttribute
        fields = ('id', 'field', 'value')


class CollectSerializer(serializers.HyperlinkedModelSerializer):
    channel = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='channel-detail'
    )
    attrs = CollectAttributeSerializer(many=True)

    class Meta:
        model = models.Collect
        fields = ('id', 'channel', 'initial_time', 'end_time', 'periodicity',
                  'attrs')


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    profiles = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='profile-detail'
    )

    class Meta:
        model = models.Author
        fields = ('id', 'profiles', 'name', 'author_type', 'gender',
                  'birthdate', 'cep')


class ProfileAttributeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.ProfileAttribute
        fields = ('id', 'field', 'value')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='author-detail'
    )
    channel = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='channel-detail'
    )
    attrs = ProfileAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = models.Profile
        fields = ('id', 'author', 'channel', 'url', 'is_reference', 'attrs')


class ManifestationAttributeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.ManifestationAttribute
        fields = ('id', 'field', 'value')


class ManifestationSerializer(serializers.HyperlinkedModelSerializer):
    manifestation_type = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='manifestationtype-detail'
    )
    profile = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='profile-detail'
    )
    collect = serializers.HyperlinkedRelatedField(
        read_only=True,
        many=True,
        view_name='collect-detail'
    )
    attrs = ManifestationAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = models.Manifestation
        fields = ('id', 'manifestation_type', 'profile', 'id_in_channel',
                  'version', 'content', 'timestamp', 'url', 'attrs', 'collect')


class CollectManifestationSerializer(serializers.HyperlinkedModelSerializer):
    manifestation = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='manifestation-detail'
    )
    collect = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='collect-detail'
    )

    class Meta:
        model = models.CollectManifestation
        fields = ('id', 'collect', 'manifestation', 'timestamp')


class RelationshipProfileAttributeSerializer(
        serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.RelationshipProfileAttribute
        fields = ('id', 'field', 'value')


class RelationshipProfileSerializer(serializers.HyperlinkedModelSerializer):
    manifestation = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='manifestation-detail'
    )
    profile = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='profile-detail'
    )
    attrs = RelationshipProfileAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = models.RelationshipProfile
        fields = ('id', 'profile', 'manifestation', 'relationship_type',
                  'attrs')
