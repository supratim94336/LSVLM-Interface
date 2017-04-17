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
            name='Corpus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_added', models.DateTimeField(verbose_name=b'date published')),
                ('name', models.CharField(unique=True, max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('process_steps', models.CharField(max_length=500)),
                ('location', models.CharField(max_length=300)),
                ('file_name', models.CharField(max_length=200)),
                ('metadata_url', models.CharField(max_length=300)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CountFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('m', models.IntegerField()),
                ('corpus', models.ForeignKey(to='corpora.Corpus')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lang',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='corpus',
            name='lang',
            field=models.ForeignKey(to='corpora.Lang'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='corpus',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
