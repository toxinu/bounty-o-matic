# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bounties', '0017_bounty_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bounty',
            name='slug',
            field=models.UUIDField(unique=True, default=uuid.uuid4),
        ),
    ]
