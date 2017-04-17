# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corpora', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='countfile',
            unique_together=set([('corpus', 'm')]),
        ),
    ]
