# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lm', '0004_lm_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='lm',
            name='default_corpus',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
