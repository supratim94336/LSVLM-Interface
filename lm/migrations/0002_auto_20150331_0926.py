# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lm',
            name='last_trained',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lm',
            name='left_coordinate',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lm',
            name='top_coordinate',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
