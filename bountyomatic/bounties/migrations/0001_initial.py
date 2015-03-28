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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('reward', models.TextField(verbose_name='Reward')),
                ('description', models.TextField(verbose_name='Description')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Open'), (2, 'Closed'), (3, 'Cancelled')], verbose_name='Status', default=1)),
                ('region', models.CharField(choices=[('eu', 'Europe'), ('us', 'US'), ('kr', 'Korea'), ('tw', 'Taiwan')], verbose_name='Region', default='eu', max_length=2)),
                ('source_realm', models.CharField(verbose_name='Source realm', max_length=50)),
                ('source_character', models.CharField(verbose_name='Source character', max_length=50)),
                ('destination_realm', models.CharField(verbose_name='Target realm', max_length=50)),
                ('destination_character', models.CharField(verbose_name='Target character', max_length=50)),
                ('added_date', models.DateTimeField(verbose_name='Creation date', auto_now_add=True)),
                ('updated_date', models.DateTimeField(verbose_name='Latest update', auto_now=True)),
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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('text', models.TextField(verbose_name='Comment')),
                ('character_realm', models.CharField(verbose_name='Character realm', max_length=50)),
                ('character_name', models.CharField(verbose_name='Character name', max_length=50)),
                ('added_date', models.DateTimeField(db_index=True, verbose_name='Creation date', auto_now_add=True)),
                ('is_hidden', models.BooleanField(default=False)),
                ('user_ip', models.GenericIPAddressField(blank=True, verbose_name='IP address', unpack_ipv4=True, null=True)),
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
