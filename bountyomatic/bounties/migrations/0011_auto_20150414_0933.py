# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def set_default_language(apps, schema_editor):
    BountyImage = apps.get_model("bounties", "BountyImage")
    for bounty_image in BountyImage.objects.all():
        bounty_image.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('bounties', '0010_bountyimage_language'),
    ]

    operations = [
        migrations.RunPython(set_default_language)
    ]
