from rest_framework import serializers
from apps.core import models


def validate_attrs(domain_attrs, attrs):
    domain_list = domain_attrs.values_list('name', flat=True)
    domain_mandatory_list = domain_attrs.filter(
        is_mandatory=True).values_list('name', flat=True)
    attrs_keys = []
    for odict in attrs:
        attrs_keys.append(odict['field'])
    for attr in attrs_keys:
        if attr not in domain_list:
            raise serializers.ValidationError(
                "%s is not a domain attribute." % attr)
    for mandatory_attr in domain_mandatory_list:
        if mandatory_attr not in attrs_keys:
            raise serializers.ValidationError(
                "Attribute '%s' is required." % mandatory_attr)
    return True


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
        write_only=True, source='author', required=False)
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
        domain_attrs = models.ProfileDomainAttribute.objects.filter(
            channel=validated_data['channel'])
        if validate_attrs(domain_attrs, attrs_data):
            channel = validated_data.pop('channel')
            id_in_channel = validated_data.pop('id_in_channel')
            profile, created = models.Profile.objects.update_or_create(
                channel=channel, id_in_channel=id_in_channel,
                defaults=validated_data)
            for attr_data in attrs_data:
                if created:
                    models.ProfileAttribute.objects.create(
                        profile=profile, **attr_data)
                else:
                    attr = models.ProfileAttribute.objects.get_or_create(
                        profile=profile,
                        field=attr_data['field']
                    )[0]
                    attr.value = attr_data['value']
                    attr.save()
            return profile

    def update(self, instance, validated_data):
        attrs_data = validated_data.pop('attrs')
        domain_attrs = models.ProfileDomainAttribute.objects.filter(
            channel=validated_data['channel'])

        for field in instance._meta.fields:
            if not field.primary_key:
                setattr(instance, field.name, validated_data[field.name])

        if validate_attrs(domain_attrs, attrs_data):
            for attr_data in attrs_data:
                attr = models.ProfileAttribute.objects.get_or_create(
                    profile=instance,
                    field=attr_data['field']
                )[0]
                attr.value = attr_data['value']
                attr.save()
        return instance


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
        write_only=True, source='collect', required=False)
    attrs = ManifestationAttributeSerializer(many=True)

    class Meta:
        model = models.Manifestation
        fields = ('id', 'id_in_channel', 'manifestation_type', 'profile',
                  'version', 'content', 'timestamp', 'url', 'attrs', 'collect',
                  'manifestation_type_id', 'profile_id', 'collect_id')

    def validate(self, attrs):
        manifestation = models.Manifestation.objects.filter(
            id_in_channel=attrs['id_in_channel']).order_by('-version').first()
        attrs['version'] = 1
        if manifestation:
            versioned_attrs = models.ManifestationDomainAttribute.objects.filter(
                manifestation_type=manifestation.manifestation_type,
                is_versioned=True).values_list('name', flat=True)
            data_attrs = attrs['attrs']
            for attr in manifestation.attrs.all():
                for data_attr in data_attrs:
                    if (attr.field == data_attr['field'] and
                            attr.value != data_attr['value']):
                        if attr.field in versioned_attrs:
                            attrs['version'] = manifestation.version + 1
                        else:
                            attr.value = data_attr['value']
                            attr.save()
            if attrs['content'] != manifestation.content:
                attrs['version'] = manifestation.version + 1
        return attrs

    def create(self, validated_data):
        attrs_data = validated_data.pop('attrs')
        domain_attrs = models.ManifestationDomainAttribute.objects.filter(
            manifestation_type=validated_data['manifestation_type'])
        if validate_attrs(domain_attrs, attrs_data):
            manifestation, created = models.Manifestation.objects.get_or_create(
                id_in_channel=validated_data['id_in_channel'],
                manifestation_type=validated_data['manifestation_type'],
                version=validated_data['version'],
                defaults={
                    'content': validated_data['content'],
                    'timestamp': validated_data['timestamp'],
                    'url': validated_data['url'],
                    'profile': validated_data['profile']
                })
            for attr in attrs_data:
                models.ManifestationAttribute.objects.update_or_create(
                    manifestation=manifestation,
                    field=attr['field'],
                    defaults={
                        'value': attr['value'],
                    },)
            if 'collect' in validated_data:
                collect = validated_data.pop('collect')
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


class RelationshipProfileAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RelationshipProfileAttribute
        fields = ('field', 'value')


class RelationshipProfileSerializer(serializers.HyperlinkedModelSerializer):
    manifestation = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='manifestation-detail'
    )
    manifestation_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Manifestation.objects.all(),
        write_only=True, source='manifestation')
    profile = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='profile-detail'
    )
    profile_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Profile.objects.all(),
        write_only=True, source='profile')
    attrs = RelationshipProfileAttributeSerializer(many=True)

    class Meta:
        model = models.RelationshipProfile
        fields = ('id', 'profile', 'manifestation', 'relationship_type',
                  'attrs', 'manifestation_id', 'profile_id')

    def create(self, validated_data):
        attrs_data = validated_data.pop('attrs')
        domain_attrs = models.RelationshipProfileDomainAttribute.objects.filter(
            manifestation_type=validated_data['manifestation'].manifestation_type)
        if validate_attrs(domain_attrs, attrs_data):
            relationship_profile = models.RelationshipProfile.objects.create(
                **validated_data)
            for attr in attrs_data:
                models.RelationshipProfileAttribute.objects.create(
                    relationship_profile=relationship_profile, **attr)
            return relationship_profile
