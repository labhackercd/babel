from apps.core import models


def manifestation_types(context):
    return {'manifestation_types': models.ManifestationType.objects.all()}
