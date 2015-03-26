from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from ..battlenet.api import get_character
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
    STATUS_CANCELLED = 3
    STATUS_CHOICES = (
        (STATUS_OPEN, 'Open'),
        (STATUS_CLOSE, 'Closed'),
        (STATUS_CANCELLED, 'Cancelled'),)

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

    @property
    def source_detail(self):
        return get_character(self.region, self.source_realm, self.source_character)

    @property
    def destination_detail(self):
        return get_character(
            self.region, self.destination_realm, self.destination_character)

    @property
    def source_thumbnail(self):
        return self._get_thumbnail('source')

    @property
    def destination_thumbnail(self):
        return self._get_thumbnail('destination')

    @property
    def destination_gender(self):
        return self.destination_detail.get('gender')

    @property
    def source_gender(self):
        return self.source_detail.get('gender')

    def _get_thumbnail(self, who):
        base_url = "http://%s.battle.net/static-render/%s/" % (self.region, self.region)
        if self.region == "cn":
            base_url = "http://www.battlenet.com.cn/static-render/cn/"
        if who == 'source':
            return base_url + self.source_detail.get('thumbnail')
        return base_url + self.destination_detail.get('thumbnail')
