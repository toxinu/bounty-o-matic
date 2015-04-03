# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bounties', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='updated_date',
            field=models.DateTimeField(verbose_name='Latest update', null=True, auto_now=True, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bounty',
            name='is_private',
            field=models.BooleanField(default=False, verbose_name='Is private'),
            preserve_default=True,
        ),
    ]
