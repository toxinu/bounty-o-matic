# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bounties', '0004_auto_20150331_0947'),
    ]

    operations = [
        migrations.AddField(
            model_name='bounty',
            name='winner_character',
            field=models.CharField(verbose_name='Winner character', null=True, blank=True, max_length=50),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bounty',
            name='winner_realm',
            field=models.CharField(verbose_name='Winner realm', null=True, blank=True, max_length=50),
            preserve_default=True,
        ),
    ]
