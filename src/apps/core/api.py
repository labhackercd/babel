from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django_filters import rest_framework as django_filters, FilterSet
from apps.core.models import (Channel, Collect, Author, Profile, Manifestation,
                              ManifestationType, CollectManifestation,
                              RelationshipProfile)
from apps.core.serializers import (ChannelSerializer, CollectSerializer,
                                   AuthorSerializer, ProfileSerializer,
                                   ManifestationSerializer,
                                   ManifestationTypeSerializer,
                                   CollectManifestationSerializer,
                                   RelationshipProfileSerializer)

DATE_LOOKUPS = ['lt', 'lte', 'gt', 'gte']


class BabelModelViewSet(viewsets.ModelViewSet):

    def destroy(self, request, *args, **kwargs):
        if 'pk' not in kwargs.keys():
            filtered_qs = self.filter_queryset(self.get_queryset())
            filtered_qs.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return super().destroy(request, *args, **kwargs)


class ChannelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_fields = ('id', 'name',)
    search_fields = ('name', 'command', 'description')
    ordering_fields = '__all__'


class ManifestationTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ManifestationType.objects.all()
    serializer_class = ManifestationTypeSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_fields = ('id', 'channel__id', 'channel__name')
    search_fields = ('name', 'channel__name', 'channel__description')
    ordering_fields = '__all__'


class CollectFilter(FilterSet):
    class Meta:
        model = Collect
        fields = {
            'initial_time': DATE_LOOKUPS,
            'end_time': DATE_LOOKUPS,
            'id': ['exact'],
            'channel__id': ['exact'],
            'channel__name': ['exact', 'contains'],
        }


class CollectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = CollectFilter
    search_fields = ('channel__name', 'channel__description')
    ordering_fields = '__all__'


class AuthorFilter(FilterSet):
    class Meta:
        model = Author
        fields = {
            'birthdate': DATE_LOOKUPS,
            'id': ['exact'],
            'name': ['exact', 'contains'],
            'author_type': ['exact', 'contains'],
            'gender': ['exact', 'contains'],
            'cep': ['exact', 'startswith', 'contains'],
        }


class AuthorViewSet(BabelModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = AuthorFilter
    search_fields = ('name', 'author_type', 'gender', 'cep')
    ordering_fields = '__all__'


class ProfileFilter(FilterSet):
    class Meta:
        model = Profile
        fields = {
            'author__birthdate': DATE_LOOKUPS,
            'author__id': ['exact'],
            'author__name': ['exact', 'contains'],
            'author__author_type': ['exact', 'contains'],
            'author__gender': ['exact', 'contains'],
            'author__cep': ['exact', 'startswith', 'contains'],
            'channel__id': ['exact'],
            'channel__name': ['exact', 'contains'],
            'id': ['exact'],
            'id_in_channel': ['exact'],
            'url': ['exact', 'contains'],
            'is_reference': ['exact'],
        }


class ProfileViewSet(BabelModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = ProfileFilter
    search_fields = ('author__name', 'author__gender', 'channel__name', 'url')
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
            'profile__author__cep': ['startswith'],
            'manifestation_type__channel__id': ['exact'],
            'manifestation_type__channel__name': ['exact', 'contains'],
            'manifestation_type__name': ['exact', 'contains'],
            'manifestation_type__id': ['exact'],
            'collect__id': ['exact'],
            'id': ['exact'],
            'id_in_channel': ['exact'],
            'version': ['exact'],
            'content': ['exact', 'contains'],
            'timestamp': DATE_LOOKUPS,
            'url': ['exact', 'contains'],
        }


class ManifestationViewSet(BabelModelViewSet):
    queryset = Manifestation.objects.all()
    serializer_class = ManifestationSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = ManifestationFilter
    search_fields = ('profile__author__name', 'content', 'url',
                     'manifestation_type__channel__name',
                     'profile__author__author_type', 'profile__author__gender',
                     'manifestation_type__name')
    ordering_fields = '__all__'


class CollectManifestationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CollectManifestation.objects.all()
    serializer_class = CollectManifestationSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_fields = ('id', 'manifestation__content', 'manifestation__url',
                     'collect__channel__name')
    search_fields = ('manifestation__content', 'manifestation__url',
                     'collect__channel__name')
    ordering_fields = '__all__'


class RelationshipProfileFilter(FilterSet):
    class Meta:
        model = RelationshipProfile
        fields = {
            'profile__id': ['exact'],
            'profile__author__birthdate': DATE_LOOKUPS,
            'profile__author__id': ['exact'],
            'profile__author__name': ['exact', 'contains'],
            'profile__author__author_type': ['exact'],
            'profile__author__gender': ['exact'],
            'profile__author__cep': ['startswith'],
            'manifestation__id': ['exact'],
            'manifestation__manifestation_type__channel__id': ['exact'],
            'manifestation__manifestation_type__channel__name': ['exact', 'contains'],
            'manifestation__manifestation_type__name': ['exact', 'contains'],
            'manifestation__manifestation_type__id': ['exact'],
        }


class RelationshipProfileViewSet(BabelModelViewSet):
    queryset = RelationshipProfile.objects.all()
    serializer_class = RelationshipProfileSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.OrderingFilter
    )
    filter_class = RelationshipProfileFilter
    search_fields = ('manifestation__content', 'manifestation__url',
                     'profile__author__name')
    ordering_fields = '__all__'
