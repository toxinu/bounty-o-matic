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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reward', models.TextField(verbose_name='Reward')),
                ('description', models.TextField(verbose_name='Description')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Open'), (2, 'Closed'), (3, 'Cancelled')], verbose_name='Status', default=1)),
                ('region', models.CharField(choices=[('eu', 'Europe'), ('us', 'US'), ('kr', 'Korea'), ('tw', 'Taiwan')], verbose_name='Region', max_length=2, default='eu')),
                ('source_realm', models.CharField(verbose_name='Source realm', max_length=50)),
                ('source_character', models.CharField(verbose_name='Source character', max_length=50)),
                ('destination_realm', models.CharField(verbose_name='Target realm', max_length=50)),
                ('destination_character', models.CharField(verbose_name='Target character', max_length=50)),
                ('added_date', models.DateTimeField(verbose_name='Creation date', auto_now_add=True)),
                ('updated_date', models.DateTimeField(verbose_name='Latest update', auto_now=True)),
                ('is_private', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'bounties',
                'ordering': ['-updated_date'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(verbose_name='Comment')),
                ('character_realm', models.CharField(verbose_name='Character realm', max_length=50)),
                ('character_name', models.CharField(verbose_name='Character name', max_length=50)),
                ('added_date', models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='Creation date')),
                ('is_hidden', models.BooleanField(verbose_name='Hidden', default=False)),
                ('user_ip', models.GenericIPAddressField(null=True, verbose_name='IP address', blank=True, unpack_ipv4=True)),
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
