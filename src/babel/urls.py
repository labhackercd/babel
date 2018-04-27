from django.urls import path, include
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework.authtoken import views
from apps.core.router import BabelRouter
from apps.core.api import (ChannelViewSet, CollectViewSet, AuthorViewSet,
                           ProfileViewSet, ManifestationViewSet,
                           ManifestationTypeViewSet,
                           CollectManifestationViewSet,
                           RelationshipProfileViewSet)

router = BabelRouter(trailing_slash=False)
router.register(r'channels', ChannelViewSet)
router.register(r'manifestation-types', ManifestationTypeViewSet)
router.register(r'collects', CollectViewSet)
router.register(r'manifestations', ManifestationViewSet)
router.register(r'collect-manifestations', CollectManifestationViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'relationship-profiles', RelationshipProfileViewSet)

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html')),
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('nested_admin/', include('nested_admin.urls')),
    path('api-token-auth/', views.obtain_auth_token),
]

admin.site.site_header = 'Babel'
