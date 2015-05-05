# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bounties', '0015_auto_20150429_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bounty',
            name='is_private',
            field=models.BooleanField(default=False, verbose_name='Private'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bounty',
            name='is_target_guild',
            field=models.BooleanField(default=False, verbose_name='Target guild'),
            preserve_default=True,
        ),
    ]
