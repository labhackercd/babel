from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from apps.core.api import (ChannelViewSet, CollectViewSet, AuthorViewSet,
                           ProfileViewSet, ManifestationViewSet)

router = DefaultRouter(trailing_slash=False)
router.register(r'channels', ChannelViewSet)
router.register(r'collects', CollectViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'manifestations', ManifestationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
]
