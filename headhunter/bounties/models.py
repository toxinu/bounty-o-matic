from django.db import models
from django.contrib.auth.models import User


class Bounty(models.Model):
    REGION_EU = 'eu'
    REGION_US = 'us'
    REGION_KR = 'kr'
    REGION_TW = 'tw'
    REGION_CHOICES = (
        (REGION_EU, 'Europe'),
        (REGION_US, 'US'),
        (REGION_KR, 'Korea'),
        (REGION_TW, 'Taiwan'),)

    amount = models.PositiveIntegerField()
    user = models.ForeignKey(User)
    region = models.CharField(
        max_length=2, choices=REGION_CHOICES, default=REGION_EU)

    source = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)

    added_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
