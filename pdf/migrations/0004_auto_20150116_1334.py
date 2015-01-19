# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pdf', '0003_auto_20150116_1304'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeaturedPDFDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.ForeignKey(to='pdf.Category')),
                ('pdfdocument', models.ForeignKey(to='pdf.PDFDocument')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PDFDocumenttype',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=60)),
                ('slug', models.SlugField(max_length=255)),
                ('help_text', models.CharField(max_length=255, null=True, blank=True)),
                ('color', models.CharField(default=b'purple', unique=True, max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='featuredpdfdocument',
            name='pdfdocument_type',
            field=models.ForeignKey(to='pdf.PDFDocumenttype'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='featuredpdfdocument',
            unique_together=set([('category', 'pdfdocument_type')]),
        ),
    ]
