# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def set_destination_faction(apps, schema_editor):
    Bounty = apps.get_model("bounties", "Bounty")
    for bounty in Bounty.objects.all():
        bounty.clean()
        bounty.save()


class Migration(migrations.Migration):

    dependencies = [
        ('bounties', '0006_bounty_destination_faction'),
    ]

    operations = [
        migrations.RunPython(set_destination_faction)
    ]
