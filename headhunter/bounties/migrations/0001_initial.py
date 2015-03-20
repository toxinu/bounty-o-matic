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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('amount', models.PositiveIntegerField()),
                ('region', models.CharField(max_length=2, default='eu', choices=[('eu', 'Europe'), ('us', 'US'), ('kr', 'Korea'), ('tw', 'Taiwan')])),
                ('source', models.CharField(max_length=200)),
                ('destination', models.CharField(max_length=200)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
