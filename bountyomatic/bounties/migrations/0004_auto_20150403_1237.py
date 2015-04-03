# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bounties', '0003_auto_20150403_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='updated_date',
            field=models.DateTimeField(db_index=True, auto_now=True, verbose_name='Latest update'),
            preserve_default=True,
        ),
    ]
