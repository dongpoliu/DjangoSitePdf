# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pdf', '0005_pdfdocument_pdfdocument_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryFollow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('followed_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(to='pdf.Category')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=60)),
                ('description', models.TextField(null=True, blank=True)),
                ('url', models.URLField()),
                ('source_url', models.URLField(null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SavedPDFDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('saved_at', models.DateTimeField(auto_now_add=True)),
                ('pdfdocument', models.ForeignKey(to='pdf.PDFDocument')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bio', models.TextField(default=b'', blank=True)),
                ('gravatar_email', models.EmailField(max_length=75, null=True, blank=True)),
                ('github', models.CharField(max_length=30, null=True, verbose_name=b'Github Username', blank=True)),
                ('twitter', models.CharField(max_length=30, null=True, verbose_name=b'Twitter Username', blank=True)),
                ('stackoverflow', models.CharField(max_length=30, null=True, verbose_name=b'Stackoverflow Profile', blank=True)),
                ('facebook', models.CharField(max_length=30, null=True, verbose_name=b'Facebook Username', blank=True)),
                ('website', models.URLField(null=True, verbose_name=b'Your Website/Blog', blank=True)),
                ('receive_email', models.BooleanField(default=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='savedpdfdocument',
            unique_together=set([('user', 'pdfdocument')]),
        ),
        migrations.AlterUniqueTogether(
            name='categoryfollow',
            unique_together=set([('user', 'category')]),
        ),
    ]
