# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bounties', '0002_bountyimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bountyimage',
            name='bounty',
            field=models.OneToOneField(to='bounties.Bounty'),
            preserve_default=True,
        ),
    ]
