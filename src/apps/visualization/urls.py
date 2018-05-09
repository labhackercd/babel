from django.urls import path
from apps.visualization import views

urlpatterns = [
    path('tokens/', views.tokens, name="tokens"),
]
