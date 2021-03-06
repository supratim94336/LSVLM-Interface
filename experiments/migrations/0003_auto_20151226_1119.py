# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-26 11:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0002_auto_20150525_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='date_run',
            field=models.DateTimeField(verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='experiment_type',
            field=models.IntegerField(choices=[(1, 'Running'), (2, 'Finished')], default=1),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='status',
            field=models.IntegerField(choices=[(1, 'Test corpus'), (2, 'Input text')], default=1),
        ),
        migrations.AlterField(
            model_name='experimentset',
            name='date_run',
            field=models.DateTimeField(verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='experimentset',
            name='experiment_type',
            field=models.IntegerField(choices=[(1, 'Test corpora'), (2, 'Input text')], default=1),
        ),
    ]
