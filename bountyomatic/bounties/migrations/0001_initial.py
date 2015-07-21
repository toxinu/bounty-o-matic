# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import bountyomatic.storage
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bounty',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('reward', models.TextField(verbose_name='Reward')),
                ('description', models.TextField(verbose_name='Description')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Open'), (2, 'Closed'), (3, 'Cancelled')], default=1, verbose_name='Status')),
                ('region', models.CharField(max_length=2, choices=[('eu', 'Europe'), ('us', 'US')], default='eu', verbose_name='Region')),
                ('added_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Latest update')),
                ('is_private', models.BooleanField(default=False, verbose_name='Private')),
                ('comments_closed', models.BooleanField(default=False, verbose_name='Comments closed')),
                ('comments_closed_by_staff', models.BooleanField(default=False, verbose_name='Comments closed by staff')),
                ('is_target_guild', models.BooleanField(default=False, verbose_name='Target guild')),
                ('slug', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('is_hidden', models.BooleanField(default=False, verbose_name='Hidden')),
                ('source_realm', models.CharField(max_length=50, verbose_name='Source realm')),
                ('source_character', models.CharField(max_length=50, verbose_name='Source character')),
                ('destination_realm', models.CharField(max_length=50, verbose_name='Target realm', null=True)),
                ('destination_character', models.CharField(max_length=50, verbose_name='Target name', null=True)),
                ('destination_faction', models.PositiveSmallIntegerField(null=True, choices=[(0, 'Alliance'), (1, 'Horde'), (2, 'Neutral')], verbose_name='Faction')),
                ('winner_realm', models.CharField(max_length=50, blank=True, null=True, verbose_name='Winner realm')),
                ('winner_character', models.CharField(max_length=50, blank=True, null=True, verbose_name='Winner character')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_date'],
                'verbose_name_plural': 'bounties',
            },
        ),
        migrations.CreateModel(
            name='BountyImage',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('updated_date', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Latest update')),
                ('image', models.ImageField(storage=bountyomatic.storage.OverwriteStorage(), upload_to='bounties')),
                ('language', models.CharField(max_length=5, choices=[('en-us', 'English'), ('fr-fr', 'French')])),
                ('bounty', models.ForeignKey(to='bounties.Bounty')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Comment')),
                ('character_realm', models.CharField(max_length=50, verbose_name='Character realm')),
                ('character_name', models.CharField(max_length=50, verbose_name='Character name')),
                ('added_date', models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='Creation date')),
                ('updated_date', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Latest update')),
                ('is_hidden', models.BooleanField(default=False, verbose_name='Hidden')),
                ('user_ip', models.GenericIPAddressField(blank=True, unpack_ipv4=True, null=True, verbose_name='IP address')),
                ('bounty', models.ForeignKey(to='bounties.Bounty')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-added_date'],
                'verbose_name_plural': 'comments',
            },
        ),
        migrations.AlterUniqueTogether(
            name='bountyimage',
            unique_together=set([('bounty', 'language')]),
        ),
        migrations.AlterUniqueTogether(
            name='bounty',
            unique_together=set([('user', 'source_realm', 'source_character', 'destination_realm', 'destination_character')]),
        ),
    ]
