# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bounties', '0011_auto_20150414_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bountyimage',
            name='language',
            field=models.CharField(choices=[('en_US', 'English'), ('fr_FR', 'French')], max_length=5),
            preserve_default=True,
        ),
    ]
