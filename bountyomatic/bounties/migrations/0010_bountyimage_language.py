# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bounties', '0009_auto_20150411_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='bountyimage',
            name='language',
            field=models.CharField(choices=[('en_US', 'English'), ('fr_FR', 'French')], max_length=5, null=True),
            preserve_default=True,
        ),
    ]
