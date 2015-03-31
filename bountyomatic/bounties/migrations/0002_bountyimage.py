# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bounties', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BountyImage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('updated_date', models.DateTimeField(verbose_name='Latest update', auto_now=True)),
                ('image', models.ImageField(upload_to='bounties')),
                ('bounty', models.ForeignKey(to='bounties.Bounty')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
