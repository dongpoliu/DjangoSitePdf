# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pdf', '0004_auto_20150116_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdfdocument',
            name='pdfdocument_type',
            field=models.ForeignKey(default=1, to='pdf.PDFDocumenttype'),
            preserve_default=False,
        ),
    ]
