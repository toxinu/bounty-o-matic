# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bounties', '0002_bounty_is_private'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='is_hidden',
            field=models.BooleanField(default=False, verbose_name='Hidden'),
            preserve_default=True,
        ),
    ]
