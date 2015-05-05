from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    battletag = models.CharField(max_length=20, null=True, blank=True, unique=True)

    def clean(self):
        from ..battlenet.api import get_player_battletag

        super().clean()
        battletag, _ = get_player_battletag(self)
        if battletag:
            self.battletag = battletag
