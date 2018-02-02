from rest_framework import viewsets, filters
from django_filters import rest_framework as django_filters, FilterSet
from apps.core.models import Channel, Collect, Author, Profile, Manifestation
from apps.core.serializers import (ChannelSerializer, CollectSerializer,
                                   AuthorSerializer, ProfileSerializer,
                                   ManifestationSerializer)

DATE_LOOKUPS = ['lt', 'lte', 'gt', 'gte']


class ChannelViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'name'
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_fields = ('id', 'name', 'means_of_access',)
    search_fields = ('name', 'means_of_access', 'description')
    ordering_fields = '__all__'


class CollectFilter(FilterSet):
    class Meta:
        model = Collect
        fields = {
            'initial_time': DATE_LOOKUPS,
            'end_time': DATE_LOOKUPS,
            'id': ['exact'],
        }


class CollectViewSet(viewsets.ModelViewSet):
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.OrderingFilter
    )
    filter_class = CollectFilter
    ordering_fields = '__all__'


class AuthorFilter(FilterSet):
    class Meta:
        model = Author
        fields = {
            'birthdate': DATE_LOOKUPS,
            'id': ['exact'],
            'name': ['exact', 'contains'],
            'author_type': ['exact'],
            'gender': ['exact'],
            # 'cep': ['startswith'],
        }


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = AuthorFilter
    search_fields = ('name', 'means_of_access', 'description')
    ordering_fields = '__all__'


class ProfileFilter(FilterSet):
    class Meta:
        model = Profile
        fields = {
            'author__birthdate': DATE_LOOKUPS,
            'author__id': ['exact'],
            'author__name': ['exact', 'contains'],
            'author__author_type': ['exact'],
            'author__gender': ['exact'],
            # 'author__cep': ['startswith'],
            'channel__id': ['exact'],
            'channel__name': ['exact', 'contains'],
            'id': ['exact'],
            'url': ['exact', 'contains'],
            'is_reference': ['exact'],
        }


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = ProfileFilter
    search_fields = ('author__name', 'author__gender', 'url')
    ordering_fields = '__all__'


class ManifestationFilter(FilterSet):
    class Meta:
        model = Manifestation
        fields = {
            'profile__id': ['exact'],
            'profile__author__birthdate': DATE_LOOKUPS,
            'profile__author__id': ['exact'],
            'profile__author__name': ['exact', 'contains'],
            'profile__author__author_type': ['exact'],
            'profile__author__gender': ['exact'],
            # 'profile__author__cep': ['startswith'],
            'channel__id': ['exact'],
            'channel__name': ['exact', 'contains'],
            'collect__id': ['exact'],
            'id': ['exact'],
            'id_in_channel': ['exact'],
            'version': ['exact'],
            'content': ['exact', 'contains'],
            'timestamp': DATE_LOOKUPS,
            'url': ['exact', 'contains'],
        }


class ManifestationViewSet(viewsets.ModelViewSet):
    queryset = Manifestation.objects.all()
    serializer_class = ManifestationSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = ManifestationFilter
    search_fields = ('profile__author__name', 'channel__name', 'content', 'url')
    ordering_fields = '__all__'
