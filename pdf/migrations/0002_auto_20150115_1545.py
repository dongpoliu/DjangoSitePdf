# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pdf', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdfdocument',
            name='created_at',
            field=models.DateTimeField(default=b'2015-01-15', auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pdfdocument',
            name='created_by',
            field=models.ForeignKey(default=b'1', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pdfdocument',
            name='rating_score',
            field=models.IntegerField(default=0, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pdfdocument',
            name='rating_votes',
            field=models.PositiveIntegerField(default=0, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pdfdocument',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 7, 45, 6, 172494, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
