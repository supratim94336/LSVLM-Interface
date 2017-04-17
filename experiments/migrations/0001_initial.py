# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lm', '0005_lm_default_corpus'),
        ('corpora', '0002_auto_20150505_1149'),
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text_path', models.CharField(max_length=300)),
                ('date_run', models.DateTimeField(verbose_name=b'date published')),
                ('experiment_type', models.IntegerField(default=1, choices=[(1, b'Running'), (2, b'Finished')])),
                ('status', models.IntegerField(default=1, choices=[(1, b'Test corpus'), (2, b'Input text')])),
                ('lm', models.ForeignKey(to='lm.LM')),
                ('test_corpus', models.ForeignKey(blank=True, to='corpora.Corpus', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
