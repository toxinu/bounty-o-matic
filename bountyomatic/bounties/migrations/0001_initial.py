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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('reward', models.TextField(verbose_name='Reward')),
                ('description', models.TextField(verbose_name='Description')),
                ('status', models.PositiveSmallIntegerField(default=1, choices=[(1, 'Open'), (2, 'Closed'), (3, 'Cancelled')], verbose_name='Status')),
                ('region', models.CharField(default='eu', choices=[('eu', 'Europe'), ('us', 'US'), ('kr', 'Korea'), ('tw', 'Taiwan')], max_length=2, verbose_name='Region')),
                ('source_realm', models.CharField(max_length=50, verbose_name='Source realm')),
                ('source_character', models.CharField(max_length=50, verbose_name='Source character')),
                ('destination_realm', models.CharField(max_length=50, verbose_name='Target realm')),
                ('destination_character', models.CharField(max_length=50, verbose_name='Target character')),
                ('added_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updated_date', models.DateTimeField(verbose_name='Latest update', auto_now=True)),
                ('is_private', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_date'],
                'verbose_name_plural': 'bounties',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Comment')),
                ('character_realm', models.CharField(max_length=50, verbose_name='Character realm')),
                ('character_name', models.CharField(max_length=50, verbose_name='Character name')),
                ('added_date', models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='Creation date')),
                ('is_hidden', models.BooleanField(default=False, verbose_name='Hidden')),
                ('user_ip', models.GenericIPAddressField(null=True, blank=True, verbose_name='IP address', unpack_ipv4=True)),
                ('bounty', models.ForeignKey(to='bounties.Bounty')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-added_date'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='bounty',
            unique_together=set([('user', 'source_realm', 'source_character', 'destination_realm', 'destination_character')]),
        ),
    ]
