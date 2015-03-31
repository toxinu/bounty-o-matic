# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bounties', '0003_auto_20150331_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bountyimage',
            name='updated_date',
            field=models.DateTimeField(verbose_name='Latest update', db_index=True, auto_now=True),
            preserve_default=True,
        ),
    ]
