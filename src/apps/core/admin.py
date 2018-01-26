from django.contrib import admin
from apps.core import models


admin.site.register(models.Channel)
admin.site.register(models.Manifestation)
admin.site.register(models.Profile)
admin.site.register(models.Author)
admin.site.register(models.Collect)
admin.site.register(models.CollectManifestation)
