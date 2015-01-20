# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('thumbnail', models.ImageField(null=True, upload_to=b'categories', blank=True)),
                ('help_text', models.CharField(max_length=255, null=True, blank=True)),
                ('official_website', models.URLField(null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FeaturedPDFDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.ForeignKey(to='pdf.Category')),
            ],
            options={
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
                ('created_at', models.DateTimeField(default=b'2015-01-15', auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('thumbnail', models.ImageField(null=True, upload_to=b'PDFDocuments', blank=True)),
                ('local_document', models.FileField(upload_to=b'/root/dev/DjangoSitePdf/DjangoSitePdf/media/uploads', null=True, verbose_name='Local Document', blank=True)),
                ('pages', models.IntegerField(null=True, verbose_name='Number of Pages in Document', blank=True)),
                ('show', models.BooleanField(default=True)),
                ('rating_votes', models.PositiveIntegerField(default=0, editable=False, blank=True)),
                ('rating_score', models.IntegerField(default=0, editable=False, blank=True)),
                ('categories', models.ManyToManyField(to='pdf.Category')),
                ('created_by', models.ForeignKey(default=b'1', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
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
            model_name='pdfdocument',
            name='pdfdocument_type',
            field=models.ForeignKey(to='pdf.PDFDocumenttype'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='featuredpdfdocument',
            name='pdfdocument',
            field=models.ForeignKey(to='pdf.PDFDocument'),
            preserve_default=True,
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
