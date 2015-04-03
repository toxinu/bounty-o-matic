# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def set_added_date_to_updated_date(apps, schema_editor):
    Comment = apps.get_model("bounties", "Comment")
    for comment in Comment.objects.all():
        comment.update_date = comment.added_date
        comment.save()


class Migration(migrations.Migration):

    dependencies = [
        ('bounties', '0002_auto_20150403_1234'),
    ]

    operations = [
        migrations.RunPython(set_added_date_to_updated_date)
    ]
