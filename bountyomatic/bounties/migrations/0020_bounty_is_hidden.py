# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bounties', '0019_auto_20150507_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='bounty',
            name='is_hidden',
            field=models.BooleanField(default=False, verbose_name='Hidden'),
        ),
    ]
