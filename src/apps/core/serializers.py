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


class ProfileAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProfileAttribute
        fields = ('field', 'value')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='author-detail'
    )
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Author.objects.all(),
        write_only=True, source='author')
    channel = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='channel-detail'
    )
    channel_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Channel.objects.all(),
        write_only=True, source='channel')
    attrs = ProfileAttributeSerializer(many=True)

    class Meta:
        model = models.Profile
        fields = ('id', 'author', 'channel', 'url', 'id_in_channel',
                  'is_reference', 'attrs', 'author_id', 'channel_id')

    def create(self, validated_data):
        attrs_data = validated_data.pop('attrs')
        profile = models.Profile.objects.create(**validated_data)
        for attr in attrs_data:
            models.ProfileAttribute.objects.create(
                profile=profile, **attr)
        return profile


class ManifestationAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ManifestationAttribute
        fields = ('field', 'value')


class ManifestationSerializer(serializers.HyperlinkedModelSerializer):
    manifestation_type = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='manifestationtype-detail'
    )
    manifestation_type_id = serializers.PrimaryKeyRelatedField(
        queryset=models.ManifestationType.objects.all(),
        write_only=True, source='manifestation_type')
    profile = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='profile-detail'
    )
    profile_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Profile.objects.all(),
        write_only=True, source='profile')
    collect = serializers.HyperlinkedRelatedField(
        read_only=True,
        many=True,
        view_name='collect-detail'
    )
    collect_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Collect.objects.all(),
        write_only=True, source='collect')
    attrs = ManifestationAttributeSerializer(many=True)

    class Meta:
        model = models.Manifestation
        fields = ('id', 'id_in_channel', 'manifestation_type', 'profile',
                  'version', 'content', 'timestamp', 'url', 'attrs', 'collect',
                  'manifestation_type_id', 'profile_id', 'collect_id')

    def create(self, validated_data):
        attrs_data = validated_data.pop('attrs')
        collect = validated_data.pop('collect')
        manifestation = models.Manifestation.objects.create(**validated_data)
        for attr in attrs_data:
            models.ManifestationAttribute.objects.create(
                manifestation=manifestation, **attr)
        models.CollectManifestation.objects.create(
            manifestation=manifestation, collect=collect)
        return manifestation


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
