# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-26 11:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lm', '0005_lm_default_corpus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lm',
            name='date_added',
            field=models.DateTimeField(verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='lm',
            name='status',
            field=models.IntegerField(choices=[(1, 'Untrained'), (2, 'Trained'), (3, 'Training')], default=1),
        ),
    ]
