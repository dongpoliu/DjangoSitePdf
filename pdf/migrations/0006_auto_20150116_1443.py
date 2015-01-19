# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pdf', '0005_pdfdocument_pdfdocument_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name']},
        ),
        migrations.RemoveField(
            model_name='category',
            name='display_order',
        ),
        migrations.RemoveField(
            model_name='category',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='category',
            name='pic',
        ),
        migrations.RemoveField(
            model_name='category',
            name='tags',
        ),
        migrations.AddField(
            model_name='category',
            name='help_text',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='official_website',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to=b'categories', blank=True),
            preserve_default=True,
        ),
    ]
