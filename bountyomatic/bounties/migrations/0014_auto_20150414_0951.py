# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bounties', '0013_auto_20150414_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bountyimage',
            name='bounty',
            field=models.ForeignKey(to='bounties.Bounty'),
            preserve_default=True,
        ),
    ]
