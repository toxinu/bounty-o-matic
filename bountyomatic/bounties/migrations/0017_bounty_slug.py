# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bounties', '0016_auto_20150505_0835'),
    ]

    operations = [
        migrations.AddField(
            model_name='bounty',
            name='slug',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
