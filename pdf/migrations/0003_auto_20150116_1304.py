# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pdf', '0002_auto_20150115_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='pic',
            field=models.ImageField(null=True, upload_to=b'images/categories', blank=True),
            preserve_default=True,
        ),
    ]
