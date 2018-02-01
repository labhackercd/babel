from rest_framework import viewsets
from apps.core.models import Channel, Collect, Author, Profile, Manifestation
from apps.core.serializers import (ChannelSerializer, CollectSerializer,
                                   AuthorSerializer, ProfileSerializer,
                                   ManifestationSerializer)


class ChannelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer


class CollectViewSet(viewsets.ModelViewSet):
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ManifestationViewSet(viewsets.ModelViewSet):
    queryset = Manifestation.objects.all()
    serializer_class = ManifestationSerializer
