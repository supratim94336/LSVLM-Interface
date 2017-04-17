# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lm', '0003_auto_20150331_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='lm',
            name='status',
            field=models.IntegerField(default=1, choices=[(1, b'Untrained'), (2, b'Trained'), (3, b'Training')]),
            preserve_default=True,
        ),
    ]
