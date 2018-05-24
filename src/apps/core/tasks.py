from __future__ import absolute_import, unicode_literals
from babel import celery_app
from apps.core.models import Channel
from django_celery_beat.models import PeriodicTask
import subprocess


@celery_app.task
def get_channel_data(channel_id):
    channel = Channel.objects.get(id=channel_id)
    subprocess.run(channel.command, shell=True)


@celery_app.task
def start_periodic_task(periodic_id):
    periodic = PeriodicTask.objects.get(id=periodic_id)
    periodic.enabled = True
    periodic.save()
