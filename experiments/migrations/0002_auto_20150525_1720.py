# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lm', '0005_lm_default_corpus'),
        ('corpora', '0002_auto_20150505_1149'),
        ('experiments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExperimentSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_run', models.DateTimeField(verbose_name=b'date published')),
                ('experiment_type', models.IntegerField(default=1, choices=[(1, b'Test corpora'), (2, b'Input text')])),
                ('corpora', models.ManyToManyField(to='corpora.Corpus')),
                ('lms', models.ManyToManyField(to='lm.LM')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='experiment',
            name='experiment_set',
            field=models.ForeignKey(blank=True, to='experiments.ExperimentSet', null=True),
            preserve_default=True,
        ),
    ]
