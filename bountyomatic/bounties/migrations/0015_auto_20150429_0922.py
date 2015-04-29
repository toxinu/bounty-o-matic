# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bounties', '0014_auto_20150414_0951'),
    ]

    operations = [
        migrations.AddField(
            model_name='bounty',
            name='is_target_guild',
            field=models.BooleanField(verbose_name='Is target guild', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bounty',
            name='destination_character',
            field=models.CharField(verbose_name='Target name', max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bounty',
            name='destination_realm',
            field=models.CharField(verbose_name='Target realm', max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bountyimage',
            name='language',
            field=models.CharField(max_length=5, choices=[('en-us', 'English'), ('fr-fr', 'French')]),
            preserve_default=True,
        ),
    ]
