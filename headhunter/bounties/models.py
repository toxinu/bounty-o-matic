from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from ..battlenet.api import get_pretty_realm
from ..battlenet.api import is_player_character
from ..battlenet.api import is_character_exists


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

    STATUS_OPEN = 1
    STATUS_CLOSE = 2
    STATUS_CHOICES = (
        (STATUS_OPEN, 'Open'),
        (STATUS_CLOSE, 'Closed'),)

    reward = models.TextField()
    description = models.TextField()
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES, default=STATUS_OPEN)

    user = models.ForeignKey(User)
    region = models.CharField(
        max_length=2, choices=REGION_CHOICES, default=REGION_EU)

    source_realm = models.CharField(max_length=50)
    source_character = models.CharField(max_length=50)
    destination_realm = models.CharField(max_length=50)
    destination_character = models.CharField(max_length=50)

    added_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'bounties'
        ordering = ['-updated_date']
        unique_together = ((
            'user', 'source_realm', 'source_character',
            'destination_realm', 'destination_character'),)

    def clean(self):
        if self.source_realm == self.destination_realm:
            if self.source_character == self.destination_character:
                raise ValidationError(
                    "source and destination characters must be different")

        exists, destination = is_character_exists(
            self.region, self.destination_realm, self.destination_character)
        if not exists:
            raise ValidationError("destination does not exists")

        if not is_player_character(
                self.user, self.source_character, self.source_realm, self.region):
            raise ValidationError("source is not owned by user")

    def get_source_realm_display(self):
        return get_pretty_realm(self.source_realm)

    def get_destination_realm_display(self):
        return get_pretty_realm(self.destination_realm)
