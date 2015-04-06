# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bounties', '0005_auto_20150404_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='bounty',
            name='destination_faction',
            field=models.PositiveSmallIntegerField(null=True, choices=[(0, 'Alliance'), (1, 'Horde'), (2, 'Neutral')], verbose_name='Faction'),
            preserve_default=True,
        ),
    ]
