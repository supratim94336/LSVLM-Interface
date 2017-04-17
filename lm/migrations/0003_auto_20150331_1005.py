# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lm', '0002_auto_20150331_0926'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lm',
            name='left_coordinate',
        ),
        migrations.RemoveField(
            model_name='lm',
            name='top_coordinate',
        ),
    ]
