# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.html import escape

from django.db import models, migrations


def set_destination_faction(apps, schema_editor):
    Bounty = apps.get_model("bounties", "Bounty")
    for bounty in Bounty.objects.all():
        bounty.reward = escape(bounty.reward)
        bounty.description = escape(bounty.description)
        bounty.clean()
        bounty.save()

    Comment = apps.get_model("bounties", "Comment")
    for comment in Comment.objects.all():
        comment.text = escape(comment.text)
        comment.clean()
        comment.save()


class Migration(migrations.Migration):

    dependencies = [
        ('bounties', '0009_auto_20150411_0957'),
    ]

    operations = [
    ]
