# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('pic', models.ImageField(null=True, upload_to=b'images/catalog/categories', blank=True)),
                ('tags', models.CharField(help_text=b'Comma-delimited set of SEO keywords for meta tag', max_length=100, null=True, blank=True)),
                ('display_order', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('display_order', 'id'),
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PDFDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=60)),
                ('slug', models.SlugField(max_length=255)),
                ('url', models.URLField(unique=True)),
                ('help_text', models.CharField(max_length=255, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('thumbnail', models.ImageField(null=True, upload_to=b'PDFDocuments', blank=True)),
                ('local_document', models.FileField(upload_to=b'/root/dev/DjangoSitePdf/DjangoSitePdf/media/uploads', null=True, verbose_name='Local Document', blank=True)),
                ('pages', models.IntegerField(null=True, verbose_name='Number of Pages in Document', blank=True)),
                ('show', models.BooleanField(default=True)),
                ('categories', models.ForeignKey(to='pdf.Category')),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model,),
        ),
    ]
