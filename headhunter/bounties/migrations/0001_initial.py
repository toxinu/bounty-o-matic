# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bounty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reward', models.TextField()),
                ('description', models.TextField()),
                ('status', models.PositiveSmallIntegerField(default=1, choices=[(1, 'Open'), (2, 'Closed')])),
                ('region', models.CharField(default='eu', choices=[('eu', 'Europe'), ('us', 'US'), ('kr', 'Korea'), ('tw', 'Taiwan')], max_length=2)),
                ('source_realm', models.CharField(max_length=50)),
                ('source_character', models.CharField(max_length=50)),
                ('destination_realm', models.CharField(max_length=50)),
                ('destination_character', models.CharField(max_length=50)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'bounties',
                'ordering': ['-updated_date'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='bounty',
            unique_together=set([('user', 'source_realm', 'source_character', 'destination_realm', 'destination_character')]),
        ),
    ]
