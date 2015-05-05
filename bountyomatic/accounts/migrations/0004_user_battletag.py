# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_default_battletag(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    for user in User.objects.all():
        user.clean()
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_user_timezone'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='battletag',
            field=models.CharField(max_length=20, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.RunPython(add_default_battletag)
    ]
