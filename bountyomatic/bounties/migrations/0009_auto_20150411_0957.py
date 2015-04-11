# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bounties', '0008_auto_20150406_1006'),
    ]

    operations = [
        migrations.AddField(
            model_name='bounty',
            name='comments_closed',
            field=models.BooleanField(default=False, verbose_name='Comments closed'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bounty',
            name='comments_closed_by_staff',
            field=models.BooleanField(default=False, verbose_name='Comments closed by staff'),
            preserve_default=True,
        ),
    ]
