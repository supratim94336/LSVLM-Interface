# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corpora', '0004_corpus_label'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='corpus',
            options={'verbose_name_plural': 'corpora'},
        ),
    ]
