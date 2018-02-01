from rest_framework import serializers
from apps.core.models import Channel, Collect, Author, Profile, Manifestation


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('id', 'name', 'description', 'means_of_access',
                  'manifestation_attrs', 'author_attrs', 'collect_attrs')


class CollectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collect
        fields = ('id', 'initial_time', 'end_time', 'data')


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name', 'author_type', 'gender', 'birthdate', 'cep')


class ProfileSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    channel = ChannelSerializer()

    class Meta:
        model = Profile
        fields = ('id', 'author', 'channel', 'url', 'is_reference', 'data')


class ManifestationSerializer(serializers.ModelSerializer):
    channel = ChannelSerializer()
    profile = ProfileSerializer()
    collect = CollectSerializer(many=True)

    class Meta:
        model = Manifestation
        fields = ('id', 'channel', 'id_in_channel', 'version', 'content',
                  'timestamp', 'url', 'data', 'profile', 'collect')
