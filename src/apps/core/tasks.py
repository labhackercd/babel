from __future__ import absolute_import, unicode_literals
from babel import celery_app
from apps.core.models import Channel
import subprocess


@celery_app.task
def get_channel_data(channel_id):
    channel = Channel.objects.get(id=channel_id)
    subprocess.run(channel.command, shell=True)
