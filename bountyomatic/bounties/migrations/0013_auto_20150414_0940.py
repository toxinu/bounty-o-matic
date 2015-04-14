# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import bountyomatic.storage


class Migration(migrations.Migration):

    dependencies = [
        ('bounties', '0012_auto_20150414_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bountyimage',
            name='image',
            field=models.ImageField(upload_to='bounties', storage=bountyomatic.storage.OverwriteStorage()),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='bountyimage',
            unique_together=set([('bounty', 'language')]),
        ),
    ]
